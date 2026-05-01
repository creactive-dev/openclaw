# Content Plan — Skill de CreActive Studio

Genera el plan de contenido semanal para Oscar Vergara en tres plataformas: Instagram, Reels/HeyGen y Threads.

## Contexto obligatorio a cargar

Antes de generar el plan, leer estos archivos en este orden:
1. `content-engine/brand/voz.md` — voz y tono de Oscar
2. `content-engine/brand/pilares.md` — 5 pilares de contenido
3. `content-engine/brand/hormozi-patterns.md` — patrones de engagement del CSV

## Parámetros

- `--contexto="[descripción]"` — (opcional, máxima prioridad editorial) proyectos, clientes o situaciones reales trabajadas esa semana. El contenido que nace del trabajo real convierte mejor.
- Sin parámetros: el plan se basa en tendencias web + pilares.

## Proceso en 3 pasos

### Paso 1: Búsqueda de tendencias reales

Usar `WebSearch` para buscar qué está trending relacionado con:
- IA + automatización para negocios (últimos 7 días)
- Operaciones y sistemas para PyMEs latinoamericanas
- Novedades en herramientas del stack de CreActive (n8n, GHL, Claude, Supabase)
- Keywords: "automatización WhatsApp", "IA para negocios LatAm", "n8n", "GoHighLevel"

Buscar en: Reddit, X/Twitter, Google. **No inventar tendencias. Solo las que aparezcan en la búsqueda.**

### Paso 2: Cruce con pilares y contexto

- Filtrar tendencias relevantes para el ICP de Oscar (dueño de PyME LatAm)
- Si se pasó `--contexto`, darle prioridad editorial: las ideas más fuertes nacen del trabajo real
- Distribuir ideas entre los 5 pilares evitando que el mismo pilar domine toda la semana

### Paso 3: Generación del plan

Volumen objetivo semanal:
- **Instagram:** 2-3 carruseles (al menos 2 con CTA de acción directa)
- **Reels/HeyGen:** 7 guiones (1 por día)
- **Threads:** 7-21 ideas (1-3 posts/día), incluyendo threads derivados de reels

## Output esperado

```
══════════════════════════════════════════════════
PLAN SEMANAL — SEMANA DEL [fecha] AL [fecha]
══════════════════════════════════════════════════

CONTEXTO DE LA SEMANA
[Resumir --contexto si se pasó]

TENDENCIAS ENCONTRADAS
[Lista de tendencias reales del WebSearch con fuentes]

─────────────────────────────────────────────────
INSTAGRAM — CARRUSELES (2-3)
─────────────────────────────────────────────────

CARRUSEL 1
  Título: ...
  Pilar: [1-5]
  Ángulo: ...
  Hook (slide 1): ...
  CTA tipo: [venta directa / acción / educativo]
  Fuente/tendencia: [si aplica]
  → /cnt-carrusel --topic="..."

CARRUSEL 2 / CARRUSEL 3
  [misma estructura]

─────────────────────────────────────────────────
REELS / HEYGEN (7 — uno por día)
─────────────────────────────────────────────────

REEL LUNES
  Título: ...
  Pilar: [1-5]
  Hook (primeros 3 seg): ...
  Idea central: ...
  Recurso adjunto sugerido: [PDF / URL / demo / guía]
  → /cnt-reel-guion --topic="..."
    → /cnt-video-brief --reel=[slug]

[REEL MARTES ... REEL DOMINGO — misma estructura]

─────────────────────────────────────────────────
THREADS (7 días × 1-3 posts/día)
─────────────────────────────────────────────────

DÍA 1 — LUNES
  Post A (patrón: Verdad Simple):
    "[texto completo — listo para copiar]"
  Post B (patrón: Paradoja):
    "[texto completo]"
  Thread derivado del Reel del lunes:
    Post 1: "[...]"
    Post 2: "[...]"
    Post 3 + CTA: "[...]"

[DÍA 2 ... DÍA 7 — misma estructura]

─────────────────────────────────────────────────
PRÓXIMOS PASOS
─────────────────────────────────────────────────
1. Carrusel 1 → /cnt-carrusel --topic="..."
2. Reel del lunes → /cnt-reel-guion --topic="..."
3. Posts de Threads del Día 1: listos para publicar.
══════════════════════════════════════════════════
```

## Reglas

- Posts de Threads: texto completo listo, no ideas.
- Al menos 2 carruseles con CTA de acción directa (agendar, DM, comentar palabra clave).
- No repetir el mismo pilar en más de 3 Threads seguidos.
- Tendencias encontradas: mencionar URL o plataforma junto a la pieza que las usa.
