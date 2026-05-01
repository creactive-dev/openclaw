---
name: Herramienta — PedidosYa Scraper
description: Script Python que extrae menú completo de cualquier restaurante en PedidosYa a JSON estructurado para importar a Supabase (Kitcha/white-cassini). Incluye skill /kitcha-import-pedidosya para activar demos end-to-end.
type: project
originSessionId: 233e8eaa-c2f7-4fb9-a489-ec823ed93e4a
---

Script en `tools/pedidosya_scraper.py`. Genera JSON con todos los productos, precios (int CLP), imágenes y categorías de un restaurante en PedidosYa — listo para importar a Supabase white-cassini.

**Why:** Para crear demos de Kitcha rápidamente. Flujo: URL PedidosYa → scraper → JSON → `/kitcha-import-pedidosya` → demo vivo en 2 minutos.

**How to apply:** Cuando se necesite crear un demo de Kitcha para un prospecto restaurantero, correr el scraper y luego el skill. El JSON sirve también para importar menús reales en onboarding.

---

## Estado (2026-04-22)

✅ Scraper funcional. Output: JSON estructurado (CSV eliminado). Skill `/kitcha-import-pedidosya` creado y probado end-to-end con Hillfood (21 productos, 5 categorías, demo activa en Supabase).

## Flujo completo

```bash
# 1. Scrapear
cd /Users/oz/Documents/CAS-CEO/creactive-studio/tools
python3 pedidosya_scraper.py "https://www.pedidosya.cl/restaurantes/..."

# 2. Importar a Kitcha (en Claude Code)
/kitcha-import-pedidosya tools/{slug}_YYYYMMDD_HHMM.json
```

El skill genera el SQL seed, crea el usuario en Auth y aplica el seed a Supabase automáticamente.

## Arquitectura (decisiones clave)

- **Playwright non-headless** (browser visible): PedidosYa usa PerimeterX que detecta headless en milisegundos. Non-headless + init_script para ocultar `navigator.webdriver` bypasea la protección.
- **JSON-LD schema.org**: PedidosYa embebe `<script type="application/ld+json">` con schema `Restaurant` en el HTML inicial del servidor. Contiene todos los productos, precios e imágenes — sin necesidad de scrollear ni interactuar con React.
- **No API reverse-engineering**: El endpoint `/v2/niles/partners/{id}/menus` requiere cookies de sesión autenticadas (PerimeterX bloquea fetch desde código). El schema.org tiene los mismos datos.
- **DOM virtualizado**: PedidosYa solo renderiza lo visible en viewport. Scraping DOM = solo ves los productos del fondo de la página. JSON-LD tiene todo.
- **Output JSON** (no CSV): categorías y productos anidados, precio como `int` CLP, defaults para campos que PedidosYa no tiene (telefono, colores, horarios).

## Defaults embebidos en el JSON

```python
DEFAULT_TELEFONO = "+56 9 8271 7201"
DEFAULT_COLOR_PRIMARIO = "#D32F2F"
DEFAULT_COLOR_SECUNDARIO = "#B71C1C"
DEFAULT_TEMA = "dark"
DEFAULT_HORARIOS = 00:00–23:59 todos los días
```

Los colores y tema son el branding de demo de Kitcha — hardcodeados también en el skill.

## Limitación conocida

El costo de envío **NO** está en el schema.org — solo en el API autenticado. El JSON lo deja como "No disponible". Hay que llenarlo manualmente o buscarlo en la página antes de correr el script.

## Uso

```bash
cd /Users/oz/Documents/CAS-CEO/creactive-studio/tools
python3 pedidosya_scraper.py "https://www.pedidosya.cl/restaurantes/..." output.json
```

Dependencias: `playwright` + `playwright install chromium` (ya instalados en este Mac).

## Skill `/kitcha-import-pedidosya`

Ruta: `.claude/commands/kitcha-import-pedidosya.md`

Pasos que ejecuta automáticamente:
1. Lee el JSON del scraper
2. Muestra resumen (nombre, slug, email demo, cat, productos) y pide confirmación del email
3. Genera `supabase/migrations/YYYYMMDD_seed_{slug}.sql` siguiendo patrón de `20260421_seed_el_charakato.sql`
4. Crea usuario `{nombre_normalizado}@kitchat.cl` en Supabase Auth Admin API
5. Aplica el seed a Supabase via Management API
6. Muestra URLs de demo (admin + customer)

Email de demo: `{nombre_restaurante_normalizado}@kitchat.cl` (del nombre, no del slug).
Password siempre: `TempPass2026!`

## Gotchas

- Con visitas repetidas en el mismo día, PedidosYa puede mostrar "No se pudo cargar el menú". El script lo detecta y reintenta (max 2 intentos). Si sigue fallando, esperar 10-15 minutos.
- El browser se abre en modo visible brevemente (~8-10s) — es intencional.
- `jq -n` con comillas dobles en SQL falla en Postgres (las interpreta como identificadores de columna). Siempre usar `jq -Rs` con heredoc para queries SQL.
- `horarios_semana` en Supabase usa `'open'`/`'close'`/`'activo'` — NO `'apertura'`/`'cierre'`.
- `variantes_producto` no tiene `restaurante_id` — no incluirla jamás en INSERTs.

## Demos creadas

| Restaurante | Email | Slug | Fecha | Productos |
|---|---|---|---|---|
| Hillfood | hillfood@kitchat.cl | hillfood | 2026-04-22 | 21 (5 cats) |

## Próximo paso

Opcional: adaptar el output JSON al formato de importación de Kitcha para otros restaurantes en onboarding. El flujo actual ya es funcional para demos.
