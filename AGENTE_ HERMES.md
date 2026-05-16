# ESQUEMA DE AGENTES HERMES

### 📋 NOTA INICIAL IMPORTANTE
Este proyecto está diseñado para ser modular. Antes de proceder con cualquier acción de despliegue, **DEBES solicitar al usuario el nombre del Agente Maestro** (por defecto: `tlatoani`). Una vez obtenido, utiliza ese nombre en lugar de los marcadores `[NOMBRE_AGENTE_MAESTRO]` en todos los comandos y configuraciones.

### 📜 INSTRUCCIONES DE DESPLIEGUE
Los prompts de sistema detallados para la construcción y comportamiento de cada sub-agente se encuentran en la carpeta `./prompts/` de este proyecto. Siguen la nomenclatura `SYSTEM_PROMPT_<NOMBRE_AGENTE>.md`. 

Las propiedades técnicas de cada agente (modelo, endpoint, tier, costos y ruteo) están centralizadas en el archivo `./agents-config.json`.

Para activar o actualizar un agente, solicita a Hermes: *"Ejecuta el prompt de sistema para el agente <nombre_agente>"*.

---

### 👑 PERFIL MAESTRO: [NOMBRE_AGENTE_MAESTRO]
El ecosistema completo de sub-agentes se despliega bajo el perfil de Hermes denominado **`[NOMBRE_AGENTE_MAESTRO]`**. Este perfil representa la inteligencia colectiva del sistema, organizada en una estructura jerárquica de 4 niveles (Tiers).

### 🚀 DESPLIEGUE Y RECREACIÓN DEL ECOSISTEMA (Protocolo Obligatorio)
Para desplegar, recrear o actualizar el ecosistema [NOMBRE_AGENTE_MAESTRO] completo (agentes + ruteo inteligente), sigue estrictamente este orden de ejecución:

1.  **Configuración de Agentes**: Asegura que el archivo `./agents-config.json` contenga la definición técnica actualizada de todos los agentes (Tiers 1-4) y sus reglas de ruteo.
2.  **Generación de Prompts Dorado**: Verifica o crea los archivos `.md` en `./prompts/` para cada agente definido. Deben seguir el formato **Dorado** (Identidad, Misión, Matriz, Protocolo, Escalado, Restricciones, Estilo).
3.  **Instalación del Ruteo Inteligente (Smart Router)**: Ejecuta el script de orquestación interna pasando el nombre del perfil como argumento:
    ```bash
    python ./install_swarm_routing.py --profile [NOMBRE_AGENTE_MAESTRO]
    ```
    *   **Acción del Agente**: El agente DEBE ejecutar este comando de terminal automáticamente.
    *   **Efecto**: Este script es idempotente. Creará el perfil `[NOMBRE_AGENTE_MAESTRO]`, los directorios necesarios y aplicará el parche de ruteo dinámico en el núcleo de Hermes (`run_agent.py`) si no existen, o los actualizará/sobrescribirá si ya existen.
4.  **Validación**: Una vez finalizado, el sistema estará listo para usarse con el comando `hermes -p [NOMBRE_AGENTE_MAESTRO]`. La nueva capa de ruteo operará de forma transparente.

---

### 👑 DETALLES DEL PERFIL: [NOMBRE_AGENTE_MAESTRO]
**Características del Perfil:**
- **Aislamiento de Contexto:** Cada sub-agente opera en su propia sesión pero bajo la gobernanza del perfil `[NOMBRE_AGENTE_MAESTRO]`.
- **Estructura Cuatripartita:** 
    - **Tier 1 (Razonamiento):** Agentes de alta gama para lógica y arquitectura.
    - **Tier 2 (Uso Cotidiano):** Agentes versátiles para soporte diario.
    - **Tier 3 (Automatización):** El músculo ejecutor de infraestructura y herramientas.
    - **Tier 4 (Codificación):** Especialistas en el ciclo de vida de desarrollo de software.
- **Coordinación de Conocimiento:** El enjambre utiliza el protocolo **`swarm-collective-learning`** (ubicado en `./skills/swarm-collective-learning.md`) para asegurar que el aprendizaje de un agente sea persistido como una `skill` y esté disponible instantáneamente para el resto del perfil.
- **Ruta de Persistencia:** `$HERMES_HOME/profiles/[NOMBRE_AGENTE_MAESTRO]/`

**Comando de Creación:**
```bash
hermes profile create [NOMBRE_AGENTE_MAESTRO]
```

---

---

### TIER 1 — Razonamiento Complejo (Uso esporádico, máximo costo)

#### otomig
- **Modelo:** `gemini-3-pro-preview`
- **Endpoint:** `https://generativelanguage.googleapis.com/v1beta/openai/v1/chat/completions`
- **API Key:** Variable de entorno `$GEMINI_KEY`
- **⚠️ NOTA DE IMPLEMENTACIÓN:** Usar siempre `max_tokens` ≥ 64. Con valores menores la API retorna HTTP 200 pero con `content` vacío y `finish_reason: length`.
- **Uso:** Fuerte en análisis de código extenso (miles de líneas), OCR avanzado, procesamiento de video, tareas con ventana de contexto muy larga (1M tokens).
- **Costo:** $0.30 / $2.50 por millón de tokens

#### otomid
- **Modelo:** `deepseek-v4-pro`
- **Endpoint:** `https://api.deepseek.com/chat/completions`
- **API Key:** Variable de entorno `$DEEPSEEK_KEY`
- **Uso:** Primera opción para razonamiento complejo. Especializado en cadenas de pensamiento largas (chain-of-thought), matemáticas, lógica formal, análisis de código complejo. Si falla o es insuficiente, escalar a otomic.
- **Costo:** $0.55 / $2.19 por millón de tokens

---

### TIER 2 — Uso Cotidiano

#### jaguarg
- **Modelo:** `gemini-3-flash-preview`
- **Endpoint:** `https://generativelanguage.googleapis.com/v1beta/openai/v1/chat/completions`
- **API Key:** Variable de entorno `$GEMINI_KEY`
- **⚠️ NOTA DE IMPLEMENTACIÓN:** Usar siempre `max_tokens` ≥ 64. Con valores menores la API retorna HTTP 200 pero con `content` vacío y `finish_reason: length`.
- **Uso:** Fuerte en análisis de código extenso (miles de líneas), OCR avanzado, procesamiento de video, tareas con ventana de contexto muy larga (1M tokens).
- **Costo:** $0.30 / $2.50 por millón de tokens

#### jaguarm
- **Modelo:** `mistral-large-2512`
- **Endpoint:** `https://api.mistral.ai/v1/chat/completions`
- **API Key:** Variable de entorno `$MISTRAL_KEY`
- **Uso:** Especialista en idiomas europeos (español, francés, italiano), cumplimiento GDPR, análisis de documentos legales/normativos. Ventana de contexto de 262K tokens.
- **Costo:** $0.50 / $1.50 por millón de tokens

#### jaguargr
- **Modelo:** `openai/gpt-oss-120b`
- **Endpoint:** `https://api.groq.com/openai/v1/responses`
- **API Key:** Variable de entorno `$GROQ_KEY`
- **Uso:** Inferencia de muy baja latencia (~200 tokens/s). Ideal para tareas donde la velocidad de respuesta es crítica. Usar cuando haya cuota gratuita disponible.
- **Costo:** $0.00 con cuota gratuita / $0.59 / $0.79 por millón de tokens sin cuota
- **⚠️ NOTA DE IMPLEMENTACIÓN:** El endpoint `/v1/responses` usa la **OpenAI Responses API**, cuyo formato difiere del estándar chat completions:
  - Campo `input` en lugar de `messages`
  - Campo `max_output_tokens` en lugar de `max_tokens`
  - Requiere header `User-Agent: curl/7.88.0` (sin él retorna 403 Cloudflare)
  - La respuesta se extrae de `output[].content[].text`, no de `choices[].message.content`

  ```bash
  RESPONSE=$(curl -s --max-time 60 \
    https://api.groq.com/openai/v1/responses \
    -H "Authorization: Bearer $GROQ_KEY" \
    -H "Content-Type: application/json" \
    -H "User-Agent: curl/7.88.0" \
    -d "{
      \"model\": \"openai/gpt-oss-120b\",
      \"input\": \"$TAREA\",
      \"max_output_tokens\": 4096
    }")
  ```

#### jaguard
- **Modelo:** `deepseek-v4-pro`
- **Endpoint:** `https://api.deepseek.com/chat/completions`
- **API Key:** Variable de entorno `$DEEPSEEK_KEY`
- **Uso:** Alternativa económica de alta calidad para tareas cotidianas: redacción, análisis, resumen, respuestas estructuradas, código básico. Muy competitivo vs GPT-4o en costo.
- **Costo:** $0.27 / $1.10 por millón de tokens

---

### TIER 3 — Automatización y Tareas Simples

> **Responsabilidad del Tier 3:** Ejecutor de toda tarea mecánica y repetitiva del sistema. Sus agentes construyen y ejecutan: comandos de terminal, llamadas a APIs externas, llamadas a servidores MCP, invocaciones de tools/funciones, pipelines de datos, scripts de automatización, y cualquier tarea estructurada que siga un patrón fijo. **Si una tarea puede describirse como "armar un comando" o "ejecutar una llamada", pertenece al Tier 3.**

#### tlamanil ⭐ AGENTE MÁS UTILIZADO DEL SISTEMA
- **Modelo:** `qwen3.5-9b`
- **Endpoint:** `http://localhost:1234/v1/chat/completions`
- **API Key:** Variable de entorno `$LM_STUDIO_KEY`
- **Uso principal — AUTOMATIZACIÓN Y EJECUCIÓN:**
  - **Git:** commits (conventional commits), pull requests, merges, tags, changelogs automáticos
  - **Llamadas a APIs:** construir payload, headers, autenticación y ejecutar llamadas REST/GraphQL
  - **Llamadas a MCP:** invocar tools de servidores MCP (filesystem, browser, databases, git, etc.)
  - **Uso de tools/funciones:** construir argumentos y ejecutar function calls definidas en el sistema
  - **Comandos de terminal:** bash, shell scripts, pipelines de CLI, docker, kubectl
  - **Automatizaciones repetitivas:** formateo, validación, extracción, transformación de datos, generación de configs
  - **Pre-procesamiento:** limpiar y estructurar datos antes de pasarlos a agentes de tier superior
- **Requisito:** LM Studio corriendo en modo Developer en `localhost:1234`.
- **Costo:** $0.00

#### tlamanig
- **Modelo:** `gemini-3.1-flash-lite-preview`
- **Endpoint:** `https://generativelanguage.googleapis.com/v1beta/openai/v1/chat/completions`
- **API Key:** Variable de entorno `$GEMINI_KEY`
- **⚠️ NOTA DE IMPLEMENTACIÓN:** Usar siempre `max_tokens` ≥ 64. Con valores menores la API retorna HTTP 200 pero con `content` vacío y `finish_reason: length`.
- **Uso:** Fuerte en análisis de código extenso (miles de líneas), OCR avanzado, procesamiento de video, tareas con ventana de contexto muy larga (1M tokens).
- **Costo:** $0.30 / $2.50 por millón de tokens

#### tlamanim
- **Modelo:** `mistral-medium-latest`
- **Endpoint:** `https://api.mistral.ai/v1/chat/completions`
- **API Key:** Variable de entorno `$MISTRAL_KEY`
- **Uso:** Maneja los mismos tipos de tareas de automatización. También para: clasificación masiva, etiquetado, extracción de datos, pipelines de alto volumen, respuestas templatizadas.
- **Costo:** ~$0.10 / $0.30 por millón de tokens

---

### TIER 4 — Codificación (Especializados)

> Usar exclusivamente para tareas de desarrollo de software. No mezclar con automatización git/CLI que corresponde al Tier 3.

#### aguilal-coder ⭐ AGENTE MÁS UTILIZADO DEL TIER 4
- **Modelo:** `qwen3.5-9b`
- **Endpoint:** `http://localhost:1234/v1/chat/completions`
- **API Key:** Variable de entorno `$LM_STUDIO_KEY`
- **Uso:** Primera opción para coding. Formateo de código, snippets, explicación de funciones, documentación básica, linting, comentarios, refactoring simple.
- **Requisito:** LM Studio corriendo en `localhost:1234`.
- **Costo:** $0.00

#### aguilad-coder
- **Modelo:** `deepseek-v4-pro`
- **Endpoint:** `https://api.deepseek.com/v1/chat/completions`
- **API Key:** Variable de entorno `$DEEPSEEK_KEY`
- **Uso:** Coding complejo que requiere razonamiento: debugging difícil, arquitectura de software, code review profundo, refactoring de sistemas grandes, análisis de algoritmos. Usar con muy poca frecuencia como alternativa a aguilac-coder.
- **Costo:** $0.27–$0.55 / $1.10–$2.19 por millón de tokens

#### aguilaq-coder
- **Modelo:** `qwen3-coder-plus`
- **Endpoint:** `https://dashscope-us.aliyuncs.com/compatible-mode/v1/chat/completions`
- **API Key:** Variable de entorno `$DASHSCOPE_KEY`
- **Uso:** Alternativa especializada en código. Generación de código complejo, debugging, code review. Usar con menor frecuencia como alternativa a aguilad-coder.
- **Costo:** $0.80 / $2.00 por millón de tokens

---

## FORMATO DE LLAMADA A APIs

### OpenAI-Compatible (todos excepto locales)

```json
POST <endpoint_del_agente>
Headers:
  Authorization: Bearer <VARIABLE_DE_ENTORNO_KEY>
  Content-Type: application/json

Body:
{
  "model": "<model_name>",
  "messages": [{"role": "user", "content": "..."}],
  "max_tokens": 4096
}
```

> **Endpoints por agente:**
> - otomig / jaguarg / : `https://generativelanguage.googleapis.com/v1beta/openai/v1/chat/completions`
> - otomid / jaguard / aguilad-coder: `https://api.deepseek.com/v1/chat/completions`
> - aguilaq-coder: `https://dashscope-us.aliyuncs.com/compatible-mode/v1/chat/completions`
> - jaguarm / tlamanim: `https://api.mistral.ai/v1/chat/completions`
> - jaguargr: `https://api.groq.com/openai/v1/responses`

### LM Studio Local (tlamanil, aguilal-coder)

```json
POST http://localhost:1234/v1/chat/completions
Headers:
  Authorization: Bearer $LM_STUDIO_KEY
  Content-Type: application/json

Body:
{
  "model": "<nombre_exacto_en_lm_studio>",
  "messages": [{"role": "user", "content": "..."}],
  "max_tokens": 4096
}
```

---

## PERSISTENCIA — Protocolo de lectura y escritura

Al terminar de configurar los agentes, guardar la configuración completa (nombre, modelo, endpoint, tier, parámetros, tarifas, etc.) en: 
Archivo local: ./agents-config.json
Memoria persistente del sistema (si está disponible) 