#!/bin/bash

# ==============================================================================
# SCRIPT DE GENERACIÓN Y REGISTRO DE AGENTES HERMES - PERFIL: TLATOANI (v3.3)
# ==============================================================================
# Este script registra los 12 agentes especializados en el perfil 'tlatoani',
# vinculando sus modelos, endpoints, variables de entorno y system prompts.
# ==============================================================================

# Nombre del perfil
PROFILE="tlatoani"

# Directorio de prompts
PROMPTS_DIR="./prompts"

echo "🚀 Iniciando registro de agentes en el perfil: $PROFILE..."

# Crear el perfil si no existe
hermes profile create "$PROFILE" 2>/dev/null || echo "El perfil $PROFILE ya existe."

# --- TIER 1: Razonamiento Complejo ---
echo "Configurando Tier 1 ($PROFILE)..."

# otomig (Gemini Pro) - AGENTE PRINCIPAL DE RAZONAMIENTO
hermes --profile "$PROFILE" config set agents.tier1_complex_reasoning.otomig.model "gemini-3-pro-preview"
hermes --profile "$PROFILE" config set agents.tier1_complex_reasoning.otomig.endpoint "https://generativelanguage.googleapis.com/v1beta/openai/v1/chat/completions"
hermes --profile "$PROFILE" config set agents.tier1_complex_reasoning.otomig.api_key_env "GEMINI_KEY"
hermes --profile "$PROFILE" config set agents.tier1_complex_reasoning.otomig.system_prompt_path "$PROMPTS_DIR/SYSTEM_PROMPT_OTOMIG.md"

# otomid (DeepSeek Pro) - FALLBACK TIER 1
hermes --profile "$PROFILE" config set agents.tier1_complex_reasoning.otomid.model "deepseek-v4-pro"
hermes --profile "$PROFILE" config set agents.tier1_complex_reasoning.otomid.endpoint "https://api.deepseek.com/chat/completions"
hermes --profile "$PROFILE" config set agents.tier1_complex_reasoning.otomid.api_key_env "DEEPSEEK_KEY"
hermes --profile "$PROFILE" config set agents.tier1_complex_reasoning.otomid.system_prompt_path "$PROMPTS_DIR/SYSTEM_PROMPT_OTOMID.md"

# --- TIER 2: Uso Cotidiano ---
echo "Configurando Tier 2 ($PROFILE)..."

# jaguarg
hermes --profile "$PROFILE" config set agents.tier2_daily.jaguarg.model "gemini-3-flash-preview"
hermes --profile "$PROFILE" config set agents.tier2_daily.jaguarg.endpoint "https://generativelanguage.googleapis.com/v1beta/openai/v1/chat/completions"
hermes --profile "$PROFILE" config set agents.tier2_daily.jaguarg.api_key_env "GEMINI_KEY"
hermes --profile "$PROFILE" config set agents.tier2_daily.jaguarg.system_prompt_path "$PROMPTS_DIR/SYSTEM_PROMPT_JAGUARG.md"

# jaguarm
hermes --profile "$PROFILE" config set agents.tier2_daily.jaguarm.model "mistral-large-2512"
hermes --profile "$PROFILE" config set agents.tier2_daily.jaguarm.endpoint "https://api.mistral.ai/v1/chat/completions"
hermes --profile "$PROFILE" config set agents.tier2_daily.jaguarm.api_key_env "MISTRAL_KEY"
hermes --profile "$PROFILE" config set agents.tier2_daily.jaguarm.system_prompt_path "$PROMPTS_DIR/SYSTEM_PROMPT_JAGUARM.md"

# jaguargr
hermes --profile "$PROFILE" config set agents.tier2_daily.jaguargr.model "openai/gpt-oss-120b"
hermes --profile "$PROFILE" config set agents.tier2_daily.jaguargr.endpoint "https://api.groq.com/openai/v1/responses"
hermes --profile "$PROFILE" config set agents.tier2_daily.jaguargr.api_key_env "GROQ_KEY"
hermes --profile "$PROFILE" config set agents.tier2_daily.jaguargr.system_prompt_path "$PROMPTS_DIR/SYSTEM_PROMPT_JAGUARGR.md"

# jaguard
hermes --profile "$PROFILE" config set agents.tier2_daily.jaguard.model "deepseek-v4-pro"
hermes --profile "$PROFILE" config set agents.tier2_daily.jaguard.endpoint "https://api.deepseek.com/chat/completions"
hermes --profile "$PROFILE" config set agents.tier2_daily.jaguard.api_key_env "DEEPSEEK_KEY"
hermes --profile "$PROFILE" config set agents.tier2_daily.jaguard.system_prompt_path "$PROMPTS_DIR/SYSTEM_PROMPT_JAGUARD.md"

# --- TIER 3: Automatización ---
echo "Configurando Tier 3 ($PROFILE)..."

# tlamanil (Local)
hermes --profile "$PROFILE" config set agents.tier3_automation.tlamanil.model "qwen3.5-9b"
hermes --profile "$PROFILE" config set agents.tier3_automation.tlamanil.endpoint "http://localhost:1234/v1/chat/completions"
hermes --profile "$PROFILE" config set agents.tier3_automation.tlamanil.api_key_env "LM_STUDIO_KEY"
hermes --profile "$PROFILE" config set agents.tier3_automation.tlamanil.system_prompt_path "$PROMPTS_DIR/SYSTEM_PROMPT_TLAMANIL.md"

# tlamanig
hermes --profile "$PROFILE" config set agents.tier3_automation.tlamanig.model "gemini-3.1-flash-lite-preview"
hermes --profile "$PROFILE" config set agents.tier3_automation.tlamanig.endpoint "https://generativelanguage.googleapis.com/v1beta/openai/v1/chat/completions"
hermes --profile "$PROFILE" config set agents.tier3_automation.tlamanig.api_key_env "GEMINI_KEY"
hermes --profile "$PROFILE" config set agents.tier3_automation.tlamanig.system_prompt_path "$PROMPTS_DIR/SYSTEM_PROMPT_TLAMANIG.md"

# tlamanim
hermes --profile "$PROFILE" config set agents.tier3_automation.tlamanim.model "mistral-medium-latest"
hermes --profile "$PROFILE" config set agents.tier3_automation.tlamanim.endpoint "https://api.mistral.ai/v1/chat/completions"
hermes --profile "$PROFILE" config set agents.tier3_automation.tlamanim.api_key_env "MISTRAL_KEY"
hermes --profile "$PROFILE" config set agents.tier3_automation.tlamanim.system_prompt_path "$PROMPTS_DIR/SYSTEM_PROMPT_TLAMANIM.md"

# --- TIER 4: Codificación ---
echo "Configurando Tier 4 ($PROFILE)..."

# aguilal-coder (Local)
hermes --profile "$PROFILE" config set agents.tier4_coding.aguilal-coder.model "qwen3.5-9b"
hermes --profile "$PROFILE" config set agents.tier4_coding.aguilal-coder.endpoint "http://localhost:1234/v1/chat/completions"
hermes --profile "$PROFILE" config set agents.tier4_coding.aguilal-coder.api_key_env "LM_STUDIO_KEY"
hermes --profile "$PROFILE" config set agents.tier4_coding.aguilal-coder.system_prompt_path "$PROMPTS_DIR/SYSTEM_PROMPT_AGUILAL-CODER.md"

# aguilad-coder
hermes --profile "$PROFILE" config set agents.tier4_coding.aguilad-coder.model "deepseek-v4-pro"
hermes --profile "$PROFILE" config set agents.tier4_coding.aguilad-coder.endpoint "https://api.deepseek.com/chat/completions"
hermes --profile "$PROFILE" config set agents.tier4_coding.aguilad-coder.api_key_env "DEEPSEEK_KEY"
hermes --profile "$PROFILE" config set agents.tier4_coding.aguilad-coder.system_prompt_path "$PROMPTS_DIR/SYSTEM_PROMPT_AGUILAD-CODER.md"

# aguilaq-coder
hermes --profile "$PROFILE" config set agents.tier4_coding.aguilaq-coder.model "qwen3-coder-plus"
hermes --profile "$PROFILE" config set agents.tier4_coding.aguilaq-coder.endpoint "https://dashscope-us.aliyuncs.com/compatible-mode/v1/chat/completions"
hermes --profile "$PROFILE" config set agents.tier4_coding.aguilaq-coder.api_key_env "DASHSCOPE_KEY"
hermes --profile "$PROFILE" config set agents.tier4_coding.aguilaq-coder.system_prompt_path "$PROMPTS_DIR/SYSTEM_PROMPT_AGUILAQ-CODER.md"

# --- RUTEO INTELIGENTE ---
echo "Configurando ruteo inteligente en $PROFILE..."

hermes --profile "$PROFILE" config set routing.coding.simple "aguilal-coder"
hermes --profile "$PROFILE" config set routing.coding.complex "aguilaq-coder"
hermes --profile "$PROFILE" config set routing.coding.critical "aguilad-coder"
hermes --profile "$PROFILE" config set routing.coding.extreme "otomig"

hermes --profile "$PROFILE" config set routing.reasoning.primary "otomig"
hermes --profile "$PROFILE" config set routing.reasoning.secondary "otomid"
hermes --profile "$PROFILE" config set routing.automation.primary "tlamanil"

hermes --profile "$PROFILE" config set routing.daily.primary "jaguarg"
hermes --profile "$PROFILE" config set routing.daily.secondary "jaguard"
hermes --profile "$PROFILE" config set routing.daily.multilingual "jaguarm"
hermes --profile "$PROFILE" config set routing.daily.fast "jaguargr"

# Sincronizar archivo agents-config.json del perfil
# Nota: Hermes guarda su config en yaml, pero mantenemos tu json de referencia sincronizado
CONFIG_FILE_PATH="$HERMES_HOME/profiles/$PROFILE/agents-config.json"
echo "Generando copia de referencia en $CONFIG_FILE_PATH..."
mkdir -p "$(dirname "$CONFIG_FILE_PATH")"
cp "./agents-config.json" "$CONFIG_FILE_PATH"

echo "✅ Perfil '$PROFILE' configurado exitosamente con todos los agentes."
