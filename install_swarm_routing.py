import os
import shutil
import re
import json
import argparse

# Paths
HERMES_HOME = os.environ.get("HERMES_HOME", "/media/rommelmg/Hawk/Personal/Hermes/hermes-agent")
PROJECT_PATH = "."

def setup_environment(profile_name):
    print(f"Verifying environment for profile: {profile_name}...")
    profile_path = os.path.join(HERMES_HOME, "profiles", profile_name)
    
    # 1. Ensure profile directory exists
    os.makedirs(profile_path, exist_ok=True)
    for folder in ["sessions", "logs", "skills"]:
        os.makedirs(os.path.join(profile_path, folder), exist_ok=True)
    print(f"  - Profile directory ready at {profile_path}")

    # 2. Ensure agents-config.json exists
    config_dst = os.path.join(PROJECT_PATH, "agents-config.json")
    if not os.path.exists(config_dst):
        default_config = {
            "version": "3.0",
            "agents": {},
            "routing": {"automation": {"primary": "tlamanil"}, "reasoning": {"primary": "otomig"}}
        }
        with open(config_dst, 'w') as f:
            json.dump(default_config, f, indent=2)
        print(f"  - Created default agents-config.json")

def install_routing_layer():
    print("Installing/Updating Swarm Smart Routing internal layer...")
    
    src_agent_dir = os.path.join(PROJECT_PATH, "agent")
    dst_agent_dir = os.path.join(HERMES_HOME, "agent")
    
    os.makedirs(dst_agent_dir, exist_ok=True)
    
    # Copy router classes
    for filename in ["SwarmRouter.py", "PromptComplexityClassifier.py"]:
        src = os.path.join(src_agent_dir, filename)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(dst_agent_dir, filename))
            print(f"  - Overwritten {filename} in {dst_agent_dir}")

    # Patch run_agent.py (Idempotent)
    run_agent_path = os.path.join(HERMES_HOME, "run_agent.py")
    if os.path.exists(run_agent_path):
        with open(run_agent_path, 'r') as f:
            content = f.read()

        # Clean old tlatoani references if any
        content = content.replace("from agent.TlatoaniRouter import hook_tlatoani_routing", "")
        content = content.replace("hook_tlatoani_routing(self, user_message)", "")

        # Add new swarm import
        import_stmt = "from agent.SwarmRouter import hook_swarm_routing"
        if import_stmt not in content:
            content = content.replace(
                "from agent.trajectory import (",
                f"{import_stmt}\nfrom agent.trajectory import ("
            )
            print("  - Added SwarmRouter import to run_agent.py")

        # Add hook call in run_conversation
        hook_call = "        from agent.SwarmRouter import hook_swarm_routing\n        hook_swarm_routing(self, user_message)"
        if "hook_swarm_routing(self, user_message)" not in content:
            pattern = r"(def run_conversation\(.*?-> Dict\[str, Any\]:)"
            content = re.sub(pattern, r"\1\n" + hook_call, content, flags=re.DOTALL)
            print("  - Injected hook into AIAgent.run_conversation")

        with open(run_agent_path, 'w') as f:
            f.write(content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Install Swarm Routing Layer")
    parser.add_argument("--profile", required=True, help="The name of the master agent profile")
    args = parser.parse_args()

    setup_environment(args.profile)
    install_routing_layer()
    print(f"\nSwarm Ecosystem for '{args.profile}' is ready. Run with: hermes -p {args.profile}")
