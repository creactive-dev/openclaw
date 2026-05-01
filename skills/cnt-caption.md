# Caption — Skill de CreActive Studio

Genera captions listos para publicar en Instagram, LinkedIn y Threads, siguiendo la voz de Oscar Vergara y los patrones de Hormozi adaptados por plataforma.

## Contexto obligatorio a cargar

Antes de generar, leer:
1. `content-engine/brand/voz.md` — voz y tono de Oscar
2. `content-engine/brand/hormozi-patterns.md` — patrones de engagement (usar el patrón correcto según plataforma)
3. `content-engine/brand/pilares.md` — para identificar el pilar y ajustar el ángulo

## Parámetros

- `--carrusel=[slug]` — lee el JSON de `content-engine/carrusel/ideas/{slug}.json`
- `--topic="[descripción]"` — genera desde descripción libre
- Sin parámetros: preguntar de qué trata el post

---

## Diferenciación por plataforma

Antes de escribir una sola línea, interiorizar esta tabla. Cada plataforma necesita una pieza distinta, no una adaptación superficial.

| Dimensión | Instagram | LinkedIn | Threads |
|-----------|-----------|----------|---------|
| **Longitud** | 150–300 palabras | 100–180 palabras | 80–280 caracteres (1-3 posts) |
| **Tono** | Directo + aspiracional | Profesional + operacional | Crudo, sin pulir, como pensamiento en voz alta |
| **Primera línea** | Hook de atención — genera curiosidad o tensión | Observación B2B de negocio — problema o paradoja ejecutiva | Verdad simple o paradoja en 1 línea — no hay "ver más" |
| **Estructura** | Hook → desarrollo → insight → CTA | Observación → contexto → conclusión accionable | Una sola idea. Sin bloques. Sin estructura explícita. |
| **Hashtags** | 10-15 al final, separados por línea en blanco | 3-5, integrados o al final | **Ninguno. Nunca.** |
| **Emojis** | Funcionales con moderación (→ ✓) | Máx 1-2, solo si clarifican | Cero. El texto solo. |
| **CTA** | Explícito: "Comenta X", "Guarda esto" | Implícito o pregunta de debate | Sin CTA formal. La idea misma invita a responder. |
| **Carácter** | Educativo-autoritativo | Ejecutivo-estratégico | Conversacional-crudo |

**Regla de oro:** Si puedes copiar un caption de una plataforma a otra sin cambiar nada, está mal. Deben sentirse como tres escrituras distintas sobre el mismo tema.

---

## Proceso

### Paso 1: Entender el contenido

Si `--carrusel=[slug]`: leer el JSON y extraer tema, slide `quote` (la frase más fuerte), slide `cta`, pilar, y ángulo.

Si `--topic`: usar esa descripción directamente; determinar el pilar correspondiente.

Definir antes de escribir:
- ¿Qué pilar es? (1–5)
- ¿Cuál es la frase más fuerte del contenido? (candidata al hook de IG y al único post de Threads)
- ¿Cuál es el dato o insight más inesperado?

### Paso 2: Generar caption Instagram

**Estructura:**

```
[PRIMERA LÍNEA — el hook]
1 sola frase. Sin emojis decorativos. Sin "Hola", sin "Hoy te cuento".
Es lo que aparece antes del "ver más". Debe obligar a seguir leyendo.
Aplicar uno de los 5 patrones Hormozi: Verdad Simple, Paradoja, Reencuadre Social, Lista Con Fricción, o Verdad Incómoda.

[DESARROLLO — 2-3 párrafos cortos]
Máx 3 oraciones por párrafo.
Voz de Oscar: directo, con datos concretos, spanglish técnico cuando aplica.
Primera persona del plural si habla de proyectos ("lo hicimos", "entregamos").
Primera persona del singular si habla de aprendizajes ("aprendí", "me di cuenta").

[PUNTO CLAVE]
La observación más fuerte en 1-2 líneas.
La frase que alguien guarda o comparte.

[CTA — acción específica]
"Comenta [PALABRA] y te mando [recurso]."
"Guarda esto para cuando lo necesites."
"¿Cuál de estos pasos ya haces? Cuéntame abajo."
```

**Reglas:**
- Primera frase: sin 🚀💡✨🎯❤️ — prohibidos como decoración
- Emojis funcionales aceptables con moderación: → ✓
- 150-300 palabras
- Hashtags siempre al final, separados por una línea en blanco
- Nunca empezar con "¿Sabías que...?" — es el hook más usado y menos efectivo

### Paso 3: Generar caption LinkedIn

LinkedIn es donde los dueños de PyME y gerentes toman decisiones. El tono cambia: menos emoción, más criterio ejecutivo.

**Estructura:**

```
[PRIMERA LÍNEA — observación de negocio]
Una paradoja, un error operacional, o una realidad que el lector reconoce.
Sin emojis. Sin clickbait. Con peso.

[CONTEXTO — 2 párrafos]
Qué pasa cuando ese problema no se resuelve. Datos si existen.
Hablar de resultados concretos, no de conceptos.

[CONCLUSIÓN — 1 párrafo]
La tesis clara. Qué debería hacer alguien que lee esto.

[PREGUNTA O CTA suave]
"¿Lo has implementado en tu empresa?"
"¿Cuántas horas pierde tu equipo en esto?"
Preguntas abiertas generan más debate en LinkedIn que CTAs directos.
```

**Reglas:**
- 100-180 palabras
- Sin storytelling largo — ir directo al problema y la solución
- Voz más formal pero no corporativa: "implementamos", "el proceso", "el resultado"
- Máx 5 hashtags — solo los relevantes al sector y rol del lector
- Si el contenido es técnico (n8n, GHL, automatizaciones): agregar 1-2 hashtags técnicos que usarían los mismos profesionales
- No copiar el copy de IG. Reescribir desde el ángulo del operador que informa a otro operador.

### Paso 4: Generar post Threads

Threads es el lugar donde Oscar piensa en voz alta. Sin estructura. Sin formato. Sin performance.

**Reglas absolutas:**
- **Sin hashtags. Nunca.**
- Sin emojis
- Sin formato (sin negritas, sin listas numeradas)
- Máx 500 caracteres por post (ideal 150-280 para el primero)
- Si la idea necesita más espacio: 2-3 posts encadenados (reply-chain), no uno largo
- El primer post debe poder leerse completo — no hay "ver más"
- No escribir como si fuera un caption — escribir como si fuera un mensaje de voz transcrito

**Formato para posts encadenados:**

```
[Post 1 — la idea central, 150-280 caracteres]

[Post 2 — la prueba o el giro, como reply]

[Post 3 — la conclusión o pregunta, como reply — opcional]
```

**Cómo sonar como Oscar en Threads:**
- Empezar con la conclusión, no con el contexto
- Usar frases cortas y abruptas: "Eso no resultó." / "Y ahí fue donde aprendí."
- Admitir algo que salió mal antes de decir qué funcionó
- Terminar con una pregunta o dejarlo abierto — las respuestas son el punto
- "¿O no?" como validador informal
- Aplica el patrón Verdad Simple o Verdad Incómoda de hormozi-patterns.md: son los que más resuenan en el formato crudo de Threads

---

## Output completo

```
══════════════════════════════════════════════════
CAPTION — [título del post]
Pilar: [1-5] | Patrón: [nombre del patrón Hormozi usado]
══════════════════════════════════════════════════

INSTAGRAM:
──────────────────────────────────────
[primera línea — hook]

[párrafo 1]

[párrafo 2]

[punto clave]

[CTA]

#tag1 #tag2 #tag3 #tag4 #tag5
#tag6 #tag7 #tag8 #tag9 #tag10

──────────────────────────────────────
LINKEDIN:
──────────────────────────────────────
[primera línea — observación ejecutiva]

[contexto operacional]

[conclusión + pregunta de debate]

#tag1 #tag2 #tag3 #tag4

──────────────────────────────────────
THREADS:
──────────────────────────────────────
[Post 1]

→ [Post 2 — si aplica]

→ [Post 3 — si aplica]

──────────────────────────────────────
HOOK ALTERNATIVO (para probar A/B en Instagram):
"[variante del hook]"

──────────────────────────────────────
HASHTAGS POR CATEGORÍA (Instagram):
Nicho:     #automatizacionIA #n8n #sistemasdenegocios
Audiencia: #emprendedoreslatam #pyme #duenosdenegocios
General:   #inteligenciaartificial #marketing #negocios
Marca:     #creactivestudio #oscarvergara
══════════════════════════════════════════════════
```

---

## Reglas de hashtags

**Instagram (10-15):**
- 3-4 nicho específico (automatización, n8n, IA aplicada)
- 3-4 audiencia (emprendedores LatAm, PyME, dueños de negocio)
- 2-3 tema general (inteligencia artificial, marketing, negocios)
- 1-2 marca (creactivestudio, oscarvergara)

**LinkedIn (3-5):** solo alta relevancia profesional. Mezclar 1-2 técnicos + 2-3 de industria.

**Threads: ninguno.** Los hashtags en Threads matan el tono conversacional.

---

## Anti-patterns por plataforma

**Instagram:**
- ❌ "Hola, hoy quiero contarte sobre..."
- ❌ "¿Sabías que la IA puede...?"
- ❌ Emojis en la primera oración
- ❌ CTA genérico: "Sígueme para más contenido"

**LinkedIn:**
- ❌ Storytelling personal largo (eso es IG)
- ❌ Hooks de curiosidad clickbait
- ❌ Más de 5 hashtags
- ❌ Mismo texto que Instagram con hashtags cambiados

**Threads:**
- ❌ Hashtags (siempre)
- ❌ Listas numeradas o con bullets
- ❌ "Aquí te explico cómo..." (es IG)
- ❌ Post de más de 500 caracteres sin encadenar
- ❌ CTAs directos ("Comenta X", "Guarda esto")
