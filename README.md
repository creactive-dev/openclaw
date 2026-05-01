# OpenClaw — Agency OS de CreActive Studio

> Repositorio de contexto y operación del agente autónomo **CAS** (CreActive Assistant).

---

## Qué es esto

OpenClaw es el "cerebro" del Agency OS de CreActive Studio. Contiene todo el contexto que CAS necesita para operar la capa administrativa de la agencia de forma autónoma: clientes, proyectos, tareas, ideas y protocolos.

**Lo que NO está aquí:** el código de landings, SaaS y proyectos técnicos (eso vive en `creactive-dev/*`). OpenClaw solo tiene contexto y documentación.

---

## Estructura

```
SOUL.md              → Identidad y comportamiento base de CAS
HEARTBEAT.md         → Protocolo del cron diario (8 AM)

context/
  CLAUDE.md          → Master del Agency OS (identidad, stack, clientes, skills)
  memory/            → Memoria acumulada de sesiones anteriores

clients/
  activos/           → Clientes con retainer o rev share activo
  prospectos/        → Prospectos en evaluación o negociación
  archivo/           → Clientes inactivos o proyectos cerrados

internal-projects/
  kitchat/           → SaaS WhatsApp para restaurantes (white-cassini)
  contentops/        → SaaS de operaciones de contenido
  nutrisco/          → Plataforma nutricional (con Constanza)

tareas/
  activas.md         → Pendientes en curso (CAS mantiene este archivo)
  por-cliente/       → Tareas específicas por cliente

ideas/
  banco.md           → Ideas capturadas, sin desarrollar

inbox/               → Entradas sin procesar (CAS limpia cada día)

campaigns/
  exponor-2026/      → Campaña outreach B2B (342 empresas)

skills/              → Los 20 slash commands del Agency OS
content-engine/      → Voz, pilares, sistema de carruseles y posts
plantillas/          → Templates reutilizables (propuestas, presentaciones)
tools/               → Scrapers de PedidosYa y Uber Eats
docs/                → Auditorías y planes archivados
```

---

## Repos relacionados (código)

| Proyecto | Repo |
|---|---|
| KitChat (SaaS restaurantes) | `creactive-dev/white-cassini` |
| ContentOps | `creactive-dev/contentops` |
| Nutrisco landing | `creactive-dev/nutrisco-landing` |
| Web CreActive Studio | `creactive-dev/creactive` |

---

*CAS — CreActive Assistant v1.0 — Mayo 2026*
