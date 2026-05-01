---
name: Agency OS — Skills internas CreActive
description: Estado de los skills y herramientas internas del workspace CreActive Studio (comandos .claude, plantillas, operaciones)
type: project
originSessionId: 29ef07b6-1b4c-40ba-8481-6147f577518b
---
Sistema operativo interno de CreActive Studio: skills, comandos slash, plantillas y estructura de workspace.

**Why:** Oscar opera como solopreneur — los skills son su "equipo". Mantenerlos actualizados y funcionales es infraestructura crítica.

**How to apply:** Al modificar cualquier skill o estructura del workspace, actualizar este archivo con lo hecho y el estado actual.

---

## Estado actual (2026-04-22)

21 comandos en `.claude/commands/`. 3 skills en `.claude/skills/` (doc-oficial, frontend-design, ui-ux-pro-max).
2 scrapers en `tools/`: `pedidosya_scraper.py` + `ubereats_scraper.py`.

## Completado

### 2026-04-22 (sesión 5 — scrapers + skill upgrade)
- **`tools/ubereats_scraper.py` creado** — scraper Playwright para Uber Eats. Estrategia: JSON-LD `schema.org/Restaurant` (mismo que PedidosYa) para catálogo + DOM `[data-testid^="store-item-"] img` para imágenes. Probado con Al Dente Antofagasta: 24 productos, 19/24 imágenes.
- **Skill `/kitcha-import-pedidosya` mejorado** (3 cambios):
  - Acepta URL directa (ubereats.com o pedidosya.cl) → detecta plataforma → corre scraper correcto automáticamente
  - Detecta fuente desde `menu_source_url` → usa `{fuente}` dinámico en SQL (no más "PedidosYa" hardcodeado)
  - Colores del SQL ahora vienen del JSON (`{color_primario}`, `{color_secundario}`) — no hardcodeados
- **Bug fix horarios demos**: `horarios_semana = NULL` en seed → restaurante siempre abierto. Antes generaba JSON con formato incorrecto (`activo`/`open`/`close`) que `useStoreStatus.ts` no leía y dejaba el restaurante cerrado.

### 2026-04-22 (sesión anterior)
- Skill `/kitcha-import-pedidosya` creado. Demo end-to-end con Hillfood (21 productos, 5 categorías).

### 2026-04-22 (sesión anterior)
- `skill-creator` instalado desde `anthropics/skills` → `~/.agents/skills/skill-creator`. Sirve para crear nuevos skills de forma estructurada. Disponible como `/skill-creator` en Claude Code.

### 2026-04-17
- Nueva plantilla `plantillas/presentacion-consultoria/template.html` — Reveal.js 12 slides dark mode CreActive, todas las variables `{{VARIABLE}}` marcadas con comentarios de patrón por slide. Sirve para consultoría, propuestas, diagnósticos y reportes.
- `plantillas/presentacion-consultoria/COMO-USAR.md` — guía de uso con flujo cp→rellenar→publicar, tabla de variables, referencia de clases CSS, y estructura `/public/propuestas/` para hostear desde creactivestudio.agency vía Vercel.

### 2026-04-16
- `/cierre-sesion` mejorado: agregada detección automática de tipo de sesión (🔧 Técnica / 🤝 Agencia / 🔀 Mixta)
- Agregada FASE 3D: creación/actualización de `clientes/{slug}/estado.md` para sesiones de agencia
- Eliminada generación de handoffs (ahorra tokens — solo actualiza documentos)
- El skill ahora cubre cualquier tipo de sesión, no solo proyectos técnicos con git

### 2026-04-27
- **MCP NotebookLM desinstalado** — removido con `claude mcp remove notebooklm`. Entradas de permisos `mcp__notebooklm__*` limpiadas del `.claude/settings.local.json`.
- **Gotcha MCP config**: Los MCPs añadidos con `claude mcp add` se guardan en `~/.claude.json` (project-scoped), NO en `settings.json` ni en `.mcp.json`. Para ver todos los MCPs activos: `claude mcp list`. Para remover: `claude mcp remove {nombre}`.

## Pendientes
- Testear flujo URL→scraper→import end-to-end (el PASO 0 del skill no se probó aún con URL directo)

## Próximo paso
Probar `/kitcha-import-pedidosya https://www.ubereats.com/cl/store/...` o `https://www.pedidosya.cl/restaurantes/...` directamente para validar el flujo completo con URL.

## Gotchas técnicos — scrapers

- **Uber Eats JSON-LD**: embebe `schema.org/Restaurant` con `hasMenu` igual que PedidosYa — mismo parser funciona
- **Uber Eats imágenes**: NOT en JSON-LD. Están en DOM renderizado, selector `[data-testid^="store-item-{uuid}"] img`. El `data-testid="item-image"` es solo para la sección de favoritos
- **Uber Eats `__REACT_QUERY_STATE__`**: JSON con `"` encoding que ni `JSON.parse` ni `eval` parsean correctamente (hay nested encoding en campo `metaJson`)
- **Horarios demos**: siempre usar `horarios_semana = NULL` — el hook `useStoreStatus.ts:50` devuelve `isOpen:true` inmediatamente cuando es NULL. Cualquier JSON de horarios con formato incorrecto deja el restaurante cerrado.
