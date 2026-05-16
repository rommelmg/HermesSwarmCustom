import json
import os
import sys
import argparse
from .PromptComplexityClassifier import PromptComplexityClassifier

class StaticRouter:
    def __init__(self, profile=None, config_path=None):
        self.classifier = PromptComplexityClassifier()
        
        # Priority: 1. Explicit path, 2. Profile path, 3. Default path
        if config_path:
            self.config_path = config_path
        elif profile:
            hermes_home = os.environ.get("HERMES_HOME", "/media/rommelmg/Hawk/Personal/Hermes/hermes-agent")
            self.config_path = f"{hermes_home}/profiles/{profile}/agents-config.json"
        else:
            self.config_path = "./agents-config.json"
            
        self.config = self._load_config()

    def _load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def route(self, prompt):
        result = self.classifier.classify(prompt)
        agent_id = result.model
        score = result.score
        signals = result.details
        
        # Decisions for small/local models
        # Mapping generic types to specific agents if needed, 
        # but the config-based approach is safer.
        if score < 5:
            agent = self.config.get("routing", {}).get("automation", {}).get("primary", "tlamanil")
        else:
            agent = self.config.get("orchestrator", {}).get("model", "otomig")
        
        return {
            "decision": "delegate",
            "agent": orchestrator,
            "score": score,
            "signals": signals
        }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", help="The user prompt to classify")
    parser.add_argument("--profile", help="Hermes profile name", default=None)
    parser.add_argument("--config", help="Path to agents-config.json", default=None)
    
    args = parser.parse_args()
    
    router = StaticRouter(profile=args.profile, config_path=args.config)
    print(json.dumps(router.route(args.prompt)))
