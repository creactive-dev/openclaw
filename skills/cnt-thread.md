# Thread — Skill de CreActive Studio

Genera posts de Threads para Oscar Vergara. Dos modos: autónomo (posts del día) o derivado (desde un reel o carrusel).

## Contexto obligatorio a cargar

Antes de generar, leer:
1. `content-engine/brand/voz.md` — voz y tono de Oscar
2. `content-engine/brand/pilares.md` — pilares de contenido
3. `content-engine/brand/hormozi-patterns.md` — patrones del CSV (estructura real, no inventada)

## Parámetros

- Sin parámetros → **Modo autónomo:** genera 2-3 posts del día
- `--from-reel=[slug]` → **Modo derivado desde reel:** lee `content-engine/reels/{slug}-guion.md`
- `--from-carrusel=[slug]` → **Modo derivado desde carrusel:** lee `content-engine/carrusel/ideas/{slug}.json`
- `--patron=[1-5]` → fuerza un patrón específico (1=Verdad Simple, 2=Paradoja, 3=Reencuadre, 4=Lista, 5=Verdad Incómoda)

## Modo autónomo (sin flags)

### Proceso

1. Elegir 2-3 pilares distintos para los posts del día (no repetir el mismo pilar)
2. Para cada post, elegir el patrón de mayor engagement según el objetivo:
   - Distribución/reposts → Patrón 1 (Verdad Simple) o Patrón 2 (Paradoja)
   - Conversación/replies → Patrón 4 (Lista) o Patrón 5 (Verdad Incómoda)
   - Validación social → Patrón 3 (Reencuadre)
3. Generar: 1 variante corta (single post) + 1 variante larga (thread de 3-5 posts) para el post más fuerte

### Output modo autónomo

```
══════════════════════════════════════════════════
THREADS DEL DÍA — [fecha]
══════════════════════════════════════════════════

POST 1 — [patrón usado]
Pilar: [1-5]
──────────────────────────────────────
"[texto completo — listo para copiar]"

──────────────────────────────────────
POST 2 — [patrón usado]
Pilar: [1-5]
──────────────────────────────────────
"[texto completo]"

──────────────────────────────────────
POST 3 (THREAD — variante larga del post más fuerte)
──────────────────────────────────────
Post 1/4: "[gancho — más corto que el single post]"
Post 2/4: "[desarrollo del punto central]"
Post 3/4: "[ejemplo o dato concreto]"
Post 4/4: "[conclusión + CTA suave]"

══════════════════════════════════════════════════
```

## Modo derivado desde reel (`--from-reel=[slug]`)

### Proceso

1. Leer `content-engine/reels/{slug}-guion.md`
2. Extraer: el hook, el punto central más fuerte, el CTA
3. Crear un thread de 3-4 posts que refuerce el mismo mensaje:
   - Post 1: versión Hormozi del hook (más corta, más provocadora)
   - Post 2: el punto central del reel en 2-3 líneas
   - Post 3: dato o ejemplo que sustenta el punto
   - Post 4: CTA que lleva a ver el reel (con link si está disponible)

### Output modo derivado desde reel

```
══════════════════════════════════════════════════
THREAD DERIVADO — Reel: [título]
══════════════════════════════════════════════════

Post 1/4 (hook — provocador):
"[texto]"

Post 2/4 (punto central):
"[texto]"

Post 3/4 (evidencia o ejemplo):
"[texto]"

Post 4/4 (CTA hacia el reel):
"[texto con link o instrucción para ver el reel]"

──────────────────────────────────────
VERSIÓN SINGLE POST (para publicar sin el thread):
"[versión comprimida en 1-3 líneas]"
══════════════════════════════════════════════════
```

## Modo derivado desde carrusel (`--from-carrusel=[slug]`)

### Proceso

1. Leer `content-engine/carrusel/ideas/{slug}.json`
2. Extraer el slide `quote` (la frase más fuerte) y el ángulo del carrusel
3. Crear posts de Threads que generen curiosidad y lleven a ver el carrusel:
   - Post principal: la frase del slide `quote` como single post Hormozi-style
   - Thread derivado: contexto del carrusel (3-4 posts)

### Output modo derivado desde carrusel

```
══════════════════════════════════════════════════
THREAD DERIVADO — Carrusel: [título]
══════════════════════════════════════════════════

POST PRINCIPAL (Hormozi-style):
"[frase del slide quote — sola, sin contexto adicional]"

──────────────────────────────────────
THREAD DE CONTEXTO (para publicar antes o después del carrusel):

Post 1/3 (setup):
"[contexto del problema que aborda el carrusel]"

Post 2/3 (punto clave):
"[el insight principal]"

Post 3/3 (CTA hacia el carrusel):
"[instrucción para ver el carrusel en Instagram]"
══════════════════════════════════════════════════
```

## Reglas generales de Threads

- **Sin hashtags.** Hormozi no los usa y sus métricas son las mejores del análisis.
- **Sin emojis decorativos.** Nunca.
- **Sin "Hilo:" o "Thread:" al inicio.** Arrancar directo en el contenido.
- Los posts de Threads se miden en 280 caracteres aproximados por post (Threads permite más, pero la brevedad es la estrategia).
- El post más corto suele ser el más reposteado — si duda entre versión corta y larga, preferir la corta.
- Nunca sonar como agencia. Siempre como Oscar hablando.
