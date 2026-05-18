#!/bin/bash
# setup_swarm.sh - Configura el perfil Tlatoani tras una instalación limpia

PROFILE_NAME="tlatoani"
PROJECT_DIR=$(pwd)
HERMES_HOME="$HOME/.hermes"
PROFILE_DIR="$HERMES_HOME/profiles/$PROFILE_NAME"

echo ">>> Configurando perfil $PROFILE_NAME desde $PROJECT_DIR..."

# 1. Crear el perfil si no existe
hermes profile create $PROFILE_NAME --clone-all 2>/dev/null || echo "El perfil ya existe."

# 2. Copiar el Prompt de Sistema
mkdir -p "$PROFILE_DIR"
cp "$PROJECT_DIR/SYSTEM_PROMPT_TLATOANI.md" "$PROFILE_DIR/SOUL.md"

# 3. Aplicar configuración base
cp "$PROJECT_DIR/config_hermes_swarm.yaml" "$PROFILE_DIR/config.yaml"

# 4. Vincular el archivo de agentes
# Creamos un enlace simbólico para que el orquestador siempre encuentre el config del proyecto
ln -sf "$PROJECT_DIR/agents-config.json" "$PROFILE_DIR/agents-config.json"

echo ">>> ¡Listo! Ahora puedes iniciar con: hermes -p $PROFILE_NAME"
