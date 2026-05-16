import os
import json
from .PromptComplexityClassifier import PromptComplexityClassifier

class SmartRouter:
    """
    Internal two-layer router for Hermes Agent.
    Layer 1: Static (PromptComplexityClassifier)
    Layer 2: Dynamic (AI-based via otomig) if static result is ambiguous.
    """
    
    AMBIGUITY_RANGE = (5, 9)  # Scores in this range trigger dynamic routing
    
    def __init__(self, config_path="./agents-config.json"):
        self.classifier = PromptComplexityClassifier()
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return {}

    def get_agent_for_task(self, prompt):
        """
        Determines the best agent for the task.
        Returns: (agent_id, is_dynamic)
        """
        result = self.classifier.classify(prompt)
        score = result.score
        
        # Layer 1: Static Decision
        if score < self.AMBIGUITY_RANGE[0]:
            # Small task -> tlamanil
            return self.config.get("routing", {}).get("automation", {}).get("primary", "tlamanil"), False
        
        if score > self.AMBIGUITY_RANGE[1]:
            # Complex task -> otomig
            return self.config.get("orchestrator", {}).get("model", "otomig"), False
            
        # Layer 2: Ambiguous -> Dynamic Routing
        # We signal that dynamic routing is needed
        return "otomig", True

    def get_dynamic_routing_prompt(self, prompt):
        """
        Generates a prompt for the dynamic router (otomig) to decide.
        """
        agents = self.config.get("agents", {})
        agents_desc = "\n".join([f"- {name}: {info.get('mission', '')}" for name, info in agents.items()])
        
        return f"""Eres el Orquestador de Ruteo Dinámico de Hermes (Tlatoani).
Tu tarea es analizar la siguiente petición del usuario y seleccionar el agente especializado más apto de la lista.

AGENTES DISPONIBLES:
{agents_desc}

PETICIÓN DEL USUARIO:
"{prompt}"

RESPUESTA:
Responde únicamente con el nombre del agente seleccionado (ej. tlamanil, jaguarg, otomig, aguilal-coder). Sin explicaciones."""

if __name__ == "__main__":
    router = SmartRouter()
    # Test
    test_prompt = "Escribe un script de python para listar archivos"
    agent, dynamic = router.get_agent_for_task(test_prompt)
    print(f"Prompt: {test_prompt}\nAgent: {agent}\nDynamic: {dynamic}")
