---
name: swarm-collective-learning
description: "Protocolo maestro para la documentación de aprendizaje y creación de habilidades dentro de un enjambre especializado de Hermes."
version: 1.1.0
author: Hermes Agent
metadata:
  hermes:
    tags: [knowledge-management, documentation, workflow, collective-intelligence]
---

# 🧠 Protocolo de Aprendizaje Colectivo del Enjambre

Este documento define cómo los agentes especializados (Tier 1-4) deben capturar, documentar y persistir el conocimiento para que sea reutilizable por el resto del enjambre.

## 📋 Reglas de Oro para Agentes

1.  **Identificación de Oportunidad:** Si una tarea requiere más de 5 pasos manuales, soluciona un error crítico o descubre un endpoint de API no documentado, **DEBE** generarse una Skill.
2.  **Persistencia Centralizada:** Todas las skills deben guardarse en la ruta de conocimiento del perfil activo: `$HERMES_HOME/profiles/[PROFILE_NAME]/skills/`.
3.  **Lenguaje Técnico:** Escribe para otros agentes. Sé quirúrgico, usa comandos exactos y evita explicaciones redundantes.

## 🏗️ Estructura de una Nueva Skill

Al crear una skill usando `skill_manage(action='create')`, sigue este formato:

```markdown
---
name: [nombre-del-procedimiento]
description: "Breve resumen de qué resuelve esta skill."
metadata:
  created_by: "[tu-nombre-de-agente]"
  tier: [tu-tier]
---

# [Título del Procedimiento]

## 🛠️ Requisitos
- [Herramientas necesarias]
- [Variables de entorno]

## 🚀 Pasos de Ejecución
1. [Comando exacto]
2. [Validación esperada]

## ⚠️ Errores Comunes (Pitfalls)
- [Qué falló durante tu ejecución y cómo lo evitaste]
```

## 🔄 Colaboración entre Tiers

- **Agentes de Razonamiento (Tier 1):** Deben crear skills sobre arquitectura y decisiones lógicas complejas.
- **Agentes de Codificación (Tier 4):** Deben crear skills sobre patrones de código, configuraciones de linters y workflows de debugging.
- **Agentes de Automatización (Tier 3):** Deben crear skills sobre pipelines, comandos de terminal y trucos de infraestructura.

## 🧐 Validación
Antes de terminar una tarea, consulta: "¿He dejado este conocimiento disponible para mi sucesor?". Si la respuesta es no, ejecuta `skill_manage`.

---
"Un enjambre no solo ejecuta, transciende dejando el camino marcado."
