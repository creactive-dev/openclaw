# Carrusel — Skill de CreActive Studio

Genera un carrusel completo para Oscar Vergara: brief JSON → slides HTML → PNGs listos para Instagram/LinkedIn.

## Contexto obligatorio a cargar

Antes de generar, leer:
1. `content-engine/brand/voz.md` — voz y tono de Oscar
2. `content-engine/brand/pilares.md` — pilares de contenido
3. `content-engine/brand/hormozi-patterns.md` — el patrón del hook del slide hero y del caption
4. `content-engine/carrusel/variedad.md` — tracker de variedad: qué pilar, patrón y posición de content-light se usaron en los últimos carruseles

## Parámetros

- `--topic="[tema o idea]"` — descripción del tema (puede venir del plan semanal)
- Sin parámetros: preguntar el tema antes de continuar

---

## Proceso

### Paso 1: Definir el ángulo

Con base en el tema + voz.md + pilares.md:
- Pilar al que pertenece (1–5)
- Ángulo específico: "cómo lo hicimos" / "error común" / "antes después" / "framework"
- Tipo de CTA: venta directa / acción / educativo
- Patrón Hormozi que aplicar al hook del slide hero

### Paso 2: Elegir la estructura según el pilar

**No todos los carruseles tienen la misma estructura.** El pilar determina el template y la secuencia de layouts. Seguir la matriz de abajo como punto de partida — no como regla fija — y adaptarla si el tema lo requiere.

---

#### Matriz pilar → estructura

**Pilar 1 — Sistemas que trabajan solos**
- Template: `minimalista`
- Eje narrativo: proceso → resultado medible
- Secuencia base: `hero-{start}` → `content` → `stat` → `content` → `quote` → `cta/cta-light`
- El `stat` es obligatorio si hay dato real. Si no, reemplazar por segundo `content`.
- El `quote` resume el antes/después en una frase.
- Hook del hero: Verdad Simple o Lista Con Fricción (de hormozi-patterns.md)

**Pilar 2 — IA práctica para negocios LatAm**
- Template: `minimalista`
- Eje narrativo: mito vs realidad → implementación concreta
- Secuencia base: `hero-{start}` → `content` (mito/problema) → `content` (lo que realmente funciona) → `stat` → `quote` → `cta/cta-light`
- El segundo `content` siempre contrasta con el primero. El lector debe sentir el giro.
- Hook del hero: Paradoja o Verdad Incómoda

**Pilar 3 — El operador vs el soñador**
- Template: `minimalista`
- Eje narrativo: historia personal → lección → aplicación
- Secuencia base: `hero-{start}` → `quote` → `content` → `quote` → `cta/cta-light`
- Más denso en `quote` que los otros pilares. El carrusel debe sonar como Oscar piensa, no como Oscar explica.
- Si hay historia de origen disponible (ver voz.md), usarla como base del `content`.
- Hook del hero: Reencuadre Social o Verdad Incómoda

**Pilar 4 — Construir sin equipo**
- Template: `tutorial` (para contenido de stack/herramientas) o `minimalista` (para contenido de decisiones)
- Eje narrativo: herramienta/decisión → criterio → resultado
- Secuencia base con tutorial: `hero` → `content` → `content` → `content` → `stat` → `cta`
- Secuencia base con minimalista: `hero-{start}` → `content` → `quote` → `content` → `cta/cta-light`
- Usar `tutorial` cuando el tema es técnico (stack, herramientas, integraciones). Usar `minimalista` cuando el tema es criterio o decisión.
- Hook del hero: Lista Con Fricción (para stack) o Verdad Simple (para criterios)

**Pilar 5 — Clientes reales, resultados reales**
- Template: `minimalista`
- Eje narrativo: problema del cliente → lo que implementamos → resultado concreto
- Secuencia base: `hero-{start}` → `content` (situación inicial) → `stat` → `content` (lo que hicimos) → `quote` (del cliente o de Oscar sobre el resultado) → `cta/cta-light`
- El `stat` es el corazón del carrusel. Sin dato real, el pilar 5 no funciona.
- Si no hay dato: usar Pilar 1 o 3 en cambio — no inventar métricas.
- Hook del hero: Verdad Simple (el resultado primero, sin rodeos)

---

### Paso 3: Leer variedad.md y aplicar reglas de rotación

Leer `content-engine/carrusel/variedad.md` (ya cargado como contexto #4). Revisar el estado actual del sistema y aplicar:

**Reglas:**
- **Pilar:** No repetir el pilar del carrusel anterior. Si el tema obliga al mismo pilar, cambiar el ángulo completamente (no dos "antes/después" seguidos, no dos "frameworks" seguidos).
- **Patrón hook:** No repetir el mismo patrón Hormozi en los últimos 3 carruseles. Usar uno de los disponibles que no aparezca en los últimos registros del log.
- **Posición content-light:** Rotar entre slides 2, 3 y 4. Ver "Última posición usada" en variedad.md y usar la siguiente diferente.
- **Quote:** Si el carrusel anterior tenía `quote`, no es obligatorio incluir otro. Puede reemplazarse por un segundo `stat` o un `content` adicional.

**Después de decidir la estructura**, anotar mentalmente los valores finales de pilar, patrón y posición de content-light — se usarán en el Paso 8 para actualizar variedad.md.

**El objetivo es que alguien que ve 5 carruseles seguidos sienta que está aprendiendo algo nuevo en cada uno, no que está viendo el mismo formato repetido con otro texto.**

---

### Paso 4: Generar el brief JSON

#### Regla de alternación dark/light (OBLIGATORIA)

**Dentro de un carrusel:** los slides de contenido se intercalan dark/light a partir del slide 2. El slide 1 (hero) puede ser dark o light según la regla entre posts (abajo).

**Entre posts (hero start):** cada nuevo carrusel alterna el color de inicio respecto al anterior. Verificar "Próximo hero start" en variedad.md antes de generar.

| Posición | Layout por defecto |
|----------|--------------------|
| Slide 1  | `hero-dark` o `hero-light` (según variedad.md) |
| Slide 2  | `content-light` (si hero fue dark) o `content` (si hero fue light) |
| Slide 3  | alterna respecto al slide 2 |
| Slide 4  | alterna respecto al slide 3 |
| Slide 5  | `content`, `stat` o `quote` — continúa alternación |
| Slide 6  | `cta` (dark, siempre cierra) |

- `stat` puede ir en posición light o dark según donde caiga en la secuencia.
- `quote` siempre dark (fondo oscuro con foto de Oscar).
- `cta` siempre dark.
- Si hay un `stat` en slide 3 (dark), el siguiente contenido va en slide 4 (light).

#### Campo `analysis` (opcional)
Cuando el slide tiene análisis o contexto narrativo además de bullets, usar el campo `analysis`:
```json
"analysis": "Texto de 1-3 oraciones que aparece entre el título y los bullets."
```
Regla: si hay `analysis`, reducir bullets a máximo 2. Los bullets complementan, no repiten el análisis.

#### Campo `mockup` (opcional)
Cuando el tema del slide puede ilustrarse visualmente, agregar:
```json
"mockup": "agent"
```
Tipos disponibles: `agent` (chat IA), `dashboard` (métricas + gráfico). El mockup aparece **inline entre el titular y los bullets** — no ocupa columna lateral, fluye dentro del contenido.
Cuándo usarlo: slides sobre herramientas, flujos, resultados, agentes IA, automatizaciones.

```json
{
  "titulo": "[título interno]",
  "slug": "[slug-sin-espacios]",
  "pilar": "[1-5]",
  "template_set": "minimalista",
  "patron_hormozi": "[nombre del patrón usado en el hero]",
  "palabras_clave": ["palabra1", "palabra2"],
  "slides": [
    {
      "layout": "hero-dark",
      "headline": "[hook fuerte — máx 6 palabras — aplicar patrón Hormozi]",
      "subheadline": "[contexto — 1 oración directa]",
      "etiqueta": "[pilar — máx 2 palabras]"
    },
    {
      "layout": "content-light",
      "etiqueta": "[subtema]",
      "titulo": "[título de sección]",
      "analysis": "[opcional — texto narrativo antes de bullets]",
      "bullets": ["Punto 1", "Punto 2"],
      "mockup": "dashboard"
    },
    {
      "layout": "content",
      "etiqueta": "[subtema]",
      "titulo": "[título de sección]",
      "bullets": ["Punto 1", "Punto 2", "Punto 3"]
    },
    {
      "layout": "stat",
      "etiqueta": "[contexto]",
      "number": "[número — ej: +300%]",
      "label": "[qué mide]",
      "context": "[de dónde viene el dato]"
    },
    {
      "layout": "quote",
      "quote": "[insight clave — frase reposteable en 1 línea]",
      "author": "Oscar Vergara"
    },
    {
      "layout": "cta",
      "texto": "[afirmación o pregunta que lleva a la acción]",
      "cta": "[acción específica — ej: Comenta AUDIT]",
      "nota": "[contexto adicional]"
    }
  ],
  "captions": {
    "instagram": "[caption IG]",
    "linkedin": "[versión LinkedIn]",
    "threads": "[versión cruda para Threads — sin hashtags, máx 280 chars]"
  }
}
```

**Reglas del JSON:**
- El primer slide es `hero-dark` o `hero-light` según "Próximo hero start" en variedad.md. No elegir por intuición — siempre consultar el tracker.
- La alternación D→L o L→D se aplica a TODOS los slides incluyendo `cta`. El CTA puede ser `cta` (dark) o `cta-light` según la posición que le corresponda en la secuencia.
- El slide `quote` debe ser una frase que Oscar diría sola en Threads — cruda, directa, sin contexto necesario.
- El slide `stat` solo si hay datos reales disponibles. Sin datos reales, no inventar.
- CTA específico: "Comenta AUDIT", "Agenda una llamada", "Guarda esto" — no genéricos.
- 6-8 slides máximo.
- El caption de Threads en el JSON es para el primer post del encadenado. Sin hashtags, sin emojis, máx 280 caracteres.

### Paso 5: Guardar JSON

`content-engine/carrusel/ideas/{slug}.json`

### Paso 6: Ejecutar generador

```bash
cd content-engine/carrusel && node generate.js ideas/{slug}.json
```

### Paso 7: Confirmar output

Listar PNGs generados en `output/{slug}/`.

### Paso 8: Actualizar variedad.md

Agregar una nueva fila al log de `content-engine/carrusel/variedad.md`:

```
| N | {slug} | {fecha YYYY-MM-DD} | {pilar} — {nombre} | {patrón hook} | {layout slide 2} | {posición content-light} | {layout último slide} |
```

Actualizar también la sección **Estado actual del sistema**:
- Total carruseles generados: incrementar en 1
- Último pilar usado: actualizar
- Último patrón hook: actualizar
- Último hero start: actualizar (dark/light)
- Última posición content-light: actualizar
- Próximo pilar sugerido: cualquiera excepto el que se acaba de usar
- Próximo patrón sugerido: cualquiera excepto los últimos 3 usados
- **Próximo hero start: invertir el último** (dark → light, light → dark)
- Próxima posición content-light: la siguiente en la rotación (2 → 3 → 4 → 2)

Si el log tiene más de 5 filas, eliminar la más antigua.

### Paso 9: Proponer siguiente paso

```
✓ {N} slides generados en output/{slug}/
✓ variedad.md actualizado

→ /cnt-caption --carrusel={slug}   (captions para los 3 canales)
→ /cnt-thread --from-carrusel={slug}   (thread expandido desde el quote)
```

---

## Notas de contenido

- Casos de clientes reales: usar datos reales cuando estén disponibles (Constanza, Rivas Legal, PH Labs, Pumpalcerro).
- Temas técnicos: el ángulo siempre es el resultado, no el tutorial. El "cómo" es el último slide, no el primero.
- Pilar 3 (operador vs soñador): funciona mejor con `quote` + `content` narrativo que con listas de bullets. Reducir bullets, aumentar frases.
- Los bullets deben ser consecuencias o pasos reales, no categorías abstractas. "Creamos formularios de seguimiento automático" > "Optimización de procesos".

## Layout disponibles en generate.js

- `hero-dark` — Apertura oscura (#050505). Headline 116px. Incluye bloque de autor (foto 68px + nombre + badge + handle) inline después del subheadline. Usar según variedad.md.
- `hero-light` — Apertura clara (#F8FAFC). Mismo schema y estructura que hero-dark. Usar según variedad.md.
- `content` — Dark (#0C0C0C). Título + analysis (opcional) + bullets. Soporta `mockup` (inline, entre título y bullets).
- `content-light` — Light (#F8FAFC). Mismo schema que content. Soporta `mockup`.
- `stat` — Métrica grande (número + label + contexto). Dark.
- `quote` — Cita de Oscar con foto y badge verificado. **Siempre dark.**
- `cta` — Cierre con botón de acción. Dark. Usar cuando el CTA cae en posición dark de la secuencia.
- `cta-light` — Cierre con botón de acción. Light (#F8FAFC). Usar cuando el CTA cae en posición light de la secuencia.
- `code` — Bloque de código (solo template `tutorial`).

## Tipos de mockup disponibles

- `agent` — Chat IA (2 mensajes usuario + respuestas IA + typing indicator). Úsalo cuando el tema sea: agentes, automatización, WhatsApp bot, servicio al cliente con IA.
- `dashboard` — Panel de métricas (4 KPIs + gráfico de barras). Úsalo cuando el tema sea: resultados, antes/después, crecimiento, datos.
