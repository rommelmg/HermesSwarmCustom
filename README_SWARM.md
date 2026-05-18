# Protocolo de Forzado de Ruteo en Swarm (Hermes)

Este documento describe el protocolo técnico para forzar el ruteo dinámico de sub-agentes dentro de la infraestructura del Swarm de Hermes.

## Introducción

El Smart Router de Hermes permite la delegación dinámica de tareas. En ciertos escenarios, el Orquestador (u otro agente) puede requerir que una tarea sea atendida por un perfil específico definido en \`agents-config.json\`. Para facilitar esto, se ha implementado un sistema de "tags" de ruteo.

## Protocolo de Tagging

Para forzar el ruteo a un agente específico, se debe incluir un tag al inicio del string del \`goal\` (objetivo) al invocar la función \`delegate_task\`.

### Formato del Tag

El formato obligatorio es:

\`[TARGET: nombre_agente]\`

Donde \`nombre_agente\` debe coincidir exactamente con la llave de un perfil configurado en \`agents-config.json\`.

### Ejemplo de Uso

Si se desea delegar una tarea de codificación específicamente al agente \`aguilal-coder\`, el string del goal debería comenzar de la siguiente manera:

\`\`\`python
delegate_task(
    goal="[TARGET: aguilal-coder] Crea el archivo README_SWARM.md con la documentación técnica...",
    # otros parámetros...
)
\`\`\`

## Funcionamiento Interno

1.  **Detección**: El Smart Router analiza el inicio del string \`goal\`.
2.  **Extracción**: Si detecta el patrón \`[TARGET: ...]\`, extrae el nombre del agente.
3.  **Mutación**: El sistema busca el perfil correspondiente en \`agents-config.json\` y configura al sub-agente con dicho perfil (incluyendo su System Prompt y herramientas asociadas) antes de procesar el resto del mensaje.
4.  **Ejecución**: El sub-agente ahora opera bajo la identidad forzada para cumplir con el resto del objetivo descrito tras el tag.

## Beneficios

-   **Precisión**: Asegura que el experto adecuado maneje la tarea sin depender únicamente de la clasificación heurística del router.
-   **Control**: Permite flujos de trabajo deterministas en sistemas complejos de multi-agentes.
-   **Flexibilidad**: Mantiene la capacidad dinámica del Swarm mientras proporciona un mecanismo de override manual.
