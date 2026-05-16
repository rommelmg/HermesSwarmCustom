import os
import json
import logging
import re
from .PromptComplexityClassifier import PromptComplexityClassifier

logger = logging.getLogger(__name__)

class SwarmRouter:
    """
    Two-layer Smart Router for a specialized Hermes Swarm.
    Layer 1: Static Heuristics (Score-based).
    Layer 2: Dynamic AI routing (only for ambiguous scores).
    """
    
    AMBIGUITY_THRESHOLD_LOW = 5
    AMBIGUITY_THRESHOLD_HIGH = 10
    
    def __init__(self, profile=None, config_path=None):
        self.classifier = PromptComplexityClassifier()
        self.profile = profile or os.environ.get("HERMES_PROFILE", "default")
        
        if not config_path:
            # Default to the centralized config
            config_path = "./agents-config.json"
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading agents-config.json: {e}")
                return {}
        return {}

    def get_routing_decision(self, prompt):
        """
        Analyze prompt and return (agent_name, is_dynamic).
        """
        result = self.classifier.classify(prompt)
        score = result.score
        
        # Layer 1: Static Heuristics
        if score < self.AMBIGUITY_THRESHOLD_LOW:
            # Low complexity -> Automation (tlamanil)
            return self.config.get("routing", {}).get("automation", {}).get("primary", "tlamanil"), False
        
        if score > self.AMBIGUITY_THRESHOLD_HIGH:
            # High complexity -> Reasoning (otomig)
            return self.config.get("routing", {}).get("reasoning", {}).get("primary", "otomig"), False
            
        # Ambiguous -> Dynamic Routing signal
        # Use the primary reasoning agent as orchestrator
        orchestrator = self.config.get("routing", {}).get("reasoning", {}).get("primary", "otomig")
        return orchestrator, True

    def get_dynamic_prompt(self, prompt):
        """
        Generate a minimal prompt for dynamic classification.
        """
        agents = []
        for tier_name, tier_agents in self.config.get("agents", {}).items():
            for agent_name, info in tier_agents.items():
                agents.append(f"- {agent_name}: {info.get('use', '')}")
        
        agents_list = "\n".join(agents)
        
        return f"""[SISTEMA DE RUTEO DINÁMICO]
Analiza la petición del usuario y selecciona el agente más adecuado de la lista.

AGENTES DISPONIBLES:
{agents_list}

PETICIÓN:
"{prompt}"

Responde SOLO el nombre del agente. Ejemplo: jaguarg"""

    def apply_agent_config(self, agent_instance, agent_name):
        """
        Configures an AIAgent instance with the parameters of a specific specialized agent.
        """
        agent_data = None
        for tier in self.config.get("agents", {}).values():
            if agent_name in tier:
                agent_data = tier[agent_name]
                break
        
        if not agent_data:
            logger.warning(f"Agent {agent_name} not found in config.")
            return False
            
        # Update agent instance
        agent_instance.model = agent_data.get("model", agent_instance.model)
        agent_instance.base_url = agent_data.get("endpoint", agent_instance.base_url)
        
        # Handle API Key
        key_env = agent_data.get("api_key_env")
        if key_env:
            agent_instance.api_key = os.environ.get(key_env, agent_instance.api_key)
            
        # Load specialized system prompt
        prompt_path = f"./prompts/SYSTEM_PROMPT_{agent_name.upper()}.md"
        if os.path.exists(prompt_path):
            with open(prompt_path, 'r') as f:
                agent_instance.system_message = f.read()
        
        logger.info(f"Swarm Routing: Directed to {agent_name} (Model: {agent_instance.model})")
        return True

def hook_swarm_routing(agent, user_message):
    """
    To be called from AIAgent.run_conversation.
    Intervenes on the first turn of a session belonging to a specialized swarm.
    """
    # Skip routing if it's a command or internal call
    if user_message.startswith("/") or getattr(agent, "_is_routing", False):
        return

    # Skip if we are not in a specialized swarm profile 
    # (Detection can be based on existence of config or specific env var)
    profile = os.environ.get("HERMES_PROFILE")
    if not profile or profile == "default":
        return

    router = SwarmRouter(profile=profile)
    
    # We only route if the config for this swarm exists
    if not router.config:
        return

    agent_name, is_dynamic = router.get_routing_decision(user_message)
    
    if is_dynamic:
        # Perform a quick dynamic call
        logger.info(f"Ambiguity detected in {profile}. Performing dynamic routing...")
        dynamic_prompt = router.get_dynamic_prompt(user_message)
        
        agent._is_routing = True
        decision = agent.chat(dynamic_prompt).strip().lower()
        agent._is_routing = False
        
        match = re.search(r"(\w+)", decision)
        if match:
            agent_name = match.group(1)
            
    router.apply_agent_config(agent, agent_name)
