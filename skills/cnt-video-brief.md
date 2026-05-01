# Video Brief — Skill de CreActive Studio

Genera un brief estructurado por escenas para producción con avatar HeyGen a partir de un guión de reel.

**Nota:** El output es para pegar directamente en HeyGen UI. Integración via API = Phase 2.

## Contexto obligatorio a cargar

Leer `content-engine/brand/voz.md` para mantener coherencia de tono en las instrucciones del avatar.

## Parámetros

- `--reel=[slug]` — lee el guión de `content-engine/reels/{slug}-guion.md`
- Sin parámetros: pedir que se pegue el guión directamente

## Proceso

### Paso 1: Leer el guión

Si `--reel=[slug]`: leer `content-engine/reels/{slug}-guion.md`.
Si no: pedir que el usuario pegue el guión.

### Paso 2: Descomponer en escenas

Dividir el guión en escenas de 3-15 segundos cada una, agrupando por momento narrativo:
- Escena de HOOK
- Escenas de DESARROLLO (una por punto)
- Escena de CTA

Para cada escena definir:
- Texto exacto que dice el avatar
- Tono y energía del avatar en esa escena
- Qué mostrar en pantalla (texto, imagen, demo, captura)
- Duración estimada

### Paso 3: Definir recurso adjunto

El recurso adjunto no es siempre un PDF. Puede ser:
- **PDF tutorial** — para temas de proceso paso a paso
- **URL de landing** — cuando el CTA es agendar o conocer más
- **Demo interactiva** — cuando el tema es una herramienta
- **Guía descargable** — cuando el tema es educativo con framework
- **Thread de Threads** — cuando el CTA es continuar la conversación

Definir qué tipo aplica según el tema del reel y el ICP (dueño de PyME LatAm que quiere IA/automatización).

### Paso 4: Output

```
══════════════════════════════════════════════════
BRIEF HEYGEN — [título del reel]
Duración total estimada: [X] seg
Avatar: Oscar Vergara (CreActive Studio)
══════════════════════════════════════════════════

CONFIGURACIÓN GENERAL
──────────────────────────────────────
Avatar: [nombre del avatar HeyGen de Oscar]
Voz: [voz configurada]
Fondo: [color sólido negro / fondo de estudio / fondo de oficina]
Subtítulos: Activados — resaltar en rojo las palabras clave
Ratio: 9:16 vertical (Instagram/TikTok)

──────────────────────────────────────
ESCENA 1 (0-3 seg) — HOOK
──────────────────────────────────────
Texto avatar:
"[frase exacta]"

Tono/energía: Directo, sin intro, impacto inmediato. Sin pausa inicial.
Ritmo: Rápido. Sin "ehh" ni "bueno...".

Pantalla/B-roll:
[descripción exacta de qué mostrar]
Ejemplo: Texto en pantalla grande: "[frase del hook]" — aparece al mismo tiempo que se dice.

──────────────────────────────────────
ESCENA 2 (4-[X] seg) — PUNTO 1
──────────────────────────────────────
Texto avatar:
"[frase exacta]"

Tono/energía: [conversacional / énfasis en palabra X / pausa dramática antes de Y]

Pantalla/B-roll:
[descripción de visual]

──────────────────────────────────────
[ESCENAS 3, 4... — una por punto del desarrollo]
──────────────────────────────────────

──────────────────────────────────────
ESCENA FINAL ([X]-[Y] seg) — CTA
──────────────────────────────────────
Texto avatar:
"[frase exacta del CTA]"

Tono/energía: Claro, directo, sin apuro. Contacto visual fuerte.

Pantalla/B-roll:
[recurso adjunto en pantalla / handle @oscarvergara / texto del CTA]

──────────────────────────────────────
RECURSO ADJUNTO
──────────────────────────────────────
Tipo: [PDF / URL / demo / guía]
Título sugerido: "[nombre del recurso]"
Contenido que debe incluir:
  - [punto 1]
  - [punto 2]
  - [punto 3]
Por qué este recurso para este ICP:
  [explicación estratégica — qué problema resuelve para el dueño de PyME LatAm]
Cómo se entrega:
  [ManyChat trigger / link en bio / DM / comentar palabra clave]

──────────────────────────────────────
NOTAS DE PRODUCCIÓN
──────────────────────────────────────
- Velocidad de locución: [normal / ligeramente acelerada para mantener ritmo]
- Gestos: [manos visibles / expresión activa en punto clave X]
- Subtítulos: palabras a resaltar — [lista de palabras]
- Música de fondo: [sin música / ambient suave / no especificado]
══════════════════════════════════════════════════
```

## Notas

- El avatar habla como Oscar: directo, sin intro, spanglish técnico natural.
- Nada de "hola soy Oscar de CreActive Studio y hoy les voy a enseñar..." — prohibido.
- Las instrucciones de tono deben ser específicas: "pausa 1 segundo antes de decir X" es más útil que "hablar con emoción".
- Si el guión tiene más de 60 segundos, sugerir dividirlo en 2 reels antes de hacer el brief.
