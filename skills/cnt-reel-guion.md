# Reel Guion — Skill de CreActive Studio

Genera guiones de reels de 30-60 segundos para Oscar Vergara, optimizados para grabación con avatar HeyGen.

## Contexto obligatorio a cargar

Antes de generar, leer:
1. `content-engine/brand/voz.md` — voz y tono de Oscar
2. `content-engine/brand/pilares.md` — pilares de contenido

## Parámetros

- `--topic="[tema o idea]"` — descripción del tema (puede venir del plan semanal)
- Sin parámetros: preguntar el tema antes de continuar

## Proceso

### Paso 1: Definir la estructura

Con base en el tema y los frameworks de referencia:
- **3C de Ethan Shaw:** Cliffhanger (suspense) → Credibility (credibilidad) → Completion (promesa de valor)
- **ABT:** And (contexto) → But (problema o tensión) → Therefore (resolución)

El guión siempre tiene 3 partes:
1. Hook (0-3 seg) — la única razón por la que alguien se queda
2. Desarrollo (4-45 seg) — el valor real
3. CTA (45-60 seg) — la acción específica

### Paso 2: Escribir el guión

**Reglas del guión:**
- El hook es la frase más importante. Debe funcionar aunque no se escuche el resto.
- Sin intro ("hola soy Oscar...") — arrancar directo en el gancho
- Máx 3-5 puntos en el desarrollo. Cada uno con ejemplo o dato concreto.
- El CTA menciona el recurso adjunto si hay uno
- Lenguaje: voz de Oscar, directo, spanglish técnico natural
- Longitud objetivo: 30-60 segundos hablados (~70-150 palabras)

### Paso 3: Guardar el guión

Guardar en: `content-engine/reels/{slug}-guion.md`

### Paso 4: Output

```
══════════════════════════════════════════════════
GUIÓN REEL — [título]
Pilar: [1-5] | Duración estimada: [X] seg
══════════════════════════════════════════════════

HOOK (0-3 seg)
──────────────────────────────────────
Spoken: "[frase de apertura — impacto inmediato, sin intro]"
Visual: [qué se muestra en pantalla durante el hook]
Energía: [directo / urgente / conversacional]

DESARROLLO (4-[X] seg)
──────────────────────────────────────
Spoken:
"[texto completo del desarrollo — puntos naturalmente encadenados]"

Notas de ritmo:
- [pausa antes de revelar el punto clave]
- [énfasis en la palabra X]
- [bajar velocidad en la conclusión del punto Y]

Visual sugerido por momento:
- Punto 1: [qué mostrar — texto en pantalla / demo / captura]
- Punto 2: [...]
- Punto 3: [...]

CTA (últimos 10-15 seg)
──────────────────────────────────────
Spoken: "[acción específica + mención del recurso si hay uno]"
Visual: [recurso en pantalla / texto con CTA / handle]
Energía: [claro, sin apuro]

──────────────────────────────────────
GUIÓN COMPLETO (para copiar):
──────────────────────────────────────
[Hook] [Desarrollo] [CTA] — todo seguido, listo para pegar en HeyGen

──────────────────────────────────────
RECURSO ADJUNTO SUGERIDO:
  Tipo: [PDF tutorial / URL / demo / guía descargable]
  Contenido: [qué debe incluir para conectar con el ICP]
  Por qué: [razón estratégica — genera lead + engagement]

──────────────────────────────────────
SIGUIENTE PASO:
→ /cnt-video-brief --reel={slug}
══════════════════════════════════════════════════
```

## Notas

- El guión se escribe para HeyGen avatar, no para grabación en cámara. El avatar es Oscar. Tono natural, no locutor.
- Si el tema tiene datos reales de clientes, incluirlos en el desarrollo (siempre son más potentes que ejemplos hipotéticos).
- El pilar 1 (sistemas) y pilar 2 (IA práctica) funcionan bien con estructura ABT.
- El pilar 3 (operador vs soñador) funciona mejor con setup paradójico en el hook.
