#!/bin/bash

# ==============================================================================
# HERMES SMART DISPATCHER (Static + Dynamic Routing)
# ==============================================================================
# Capa 1: Clasificación Heurística (StaticRouter.py)
# Capa 2: Clasificación Dinámica (Si la Capa 1 delega al orquestador)
# ==============================================================================

PROMPT="$1"

if [ -z "$PROMPT" ]; then
    echo "Uso: ./hermes-smart-dispatch.sh \"tu pregunta aquí\""
    exit 1
fi

# Ejecutar Capa 1
RESULT=$(python3 -m agent.StaticRouter "$PROMPT")
DECISION=$(echo $RESULT | jq -r '.decision')
AGENT=$(echo $RESULT | jq -r '.agent')
SCORE=$(echo $RESULT | jq -r '.score')

if [ "$DECISION" == "direct" ]; then
    echo "⚡ [Static Route] Score: $SCORE -> Usando agente local: $AGENT"
    hermes chat -m "$AGENT" -q "$PROMPT"
else
    echo "🧠 [Dynamic Route] Score: $SCORE -> Delegando al orquestador: $AGENT"
    # El orquestador (otomig/claude) recibirá el prompt y decidirá a qué sub-agente delegar
    hermes chat -m "$AGENT" -q "$PROMPT"
fi
