# Content Engine — CreActive Studio

> Sistema de producción de contenido para Oscar Vergara / CreActive Studio.
> Genera carruseles, captions, reels, threads y planes de contenido
> usando la voz, pilares y patrones de distribución de Oscar.

---

## Estructura

```
content-engine/
├── README.md              ← Este archivo
│
├── brand/                 ← Contexto de marca (cargar siempre antes de generar)
│   ├── voz.md             ← Quién es Oscar, cómo habla, qué evitar
│   ├── pilares.md         ← Los 5 pilares de contenido con subtemas y hooks
│   ├── hormozi-patterns.md ← 5 patrones de distribución analizados de @hormozi
│   └── design-system.md   ← Paleta, tipografía, componentes (web y slides)
│
└── carrusel/              ← Engine de generación de carruseles HTML → PNG
    ├── SISTEMA.md         ← Referencia técnica completa (setup, schema, diseño)
    ├── variedad.md        ← Tracker de producción (pilar, patrón, hero start)
    ├── generate.js        ← Motor principal (Node.js + Puppeteer)
    ├── ideas/             ← Briefs JSON por carrusel
    ├── templates/         ← Templates HTML por layout
    │   └── minimalista/   ← Template set de producción
    ├── public/brand/      ← Assets de marca (headshot.jpg, logo.png)
    ├── output/            ← PNGs generados listos para publicar
    └── slides/            ← HTMLs generados (para debug en browser)
```

---

## Archivos de marca — cargar siempre antes de generar

Antes de producir cualquier pieza de contenido, Claude debe leer estos archivos en este orden:

1. `brand/voz.md` — La voz de Oscar. Sin esto, el contenido suena genérico.
2. `brand/pilares.md` — Los 5 pilares. Define el eje temático de cada pieza.
3. `brand/hormozi-patterns.md` — Los 5 patrones de Hormozi. Define la estructura del hook.

Para carruseles, además:

4. `carrusel/variedad.md` — Estado actual del sistema. Define qué pilar, patrón y hero start usar.

---

## Skills disponibles

El content engine se opera principalmente a través de skills en `.claude/commands/`:

### Carruseles

| Skill | Descripción |
|-------|-------------|
| `/cnt-carrusel` | Genera brief JSON + PNGs desde tema o artículo fuente |

Flujo completo de un carrusel:
```
Artículo / tema
→ /cnt-carrusel   (brief JSON + generación de slides)
→ /cnt-caption    (captions para IG, LinkedIn y Threads)
→ /cnt-thread     (thread expandido desde el quote del carrusel)
```

### Contenido escrito

| Skill | Descripción |
|-------|-------------|
| `/cnt-caption` | Captions listos para IG, LinkedIn y Threads desde un carrusel o tema |
| `/cnt-thread` | Thread de Threads desde tema o carrusel existente |
| `/cnt-reel-guion` | Guión completo para reel / video HeyGen desde tema |
| `/cnt-video-brief` | Brief por escenas para producción con avatar HeyGen |
| `/cnt-content-plan` | Plan de contenido semanal (IG + Reels + Threads) |

---

## Pilares de contenido (resumen)

| # | Pilar | Eje | Formatos principales |
|---|-------|-----|---------------------|
| 1 | Sistemas que trabajan solos | Automatización real con resultados concretos | Carrusel, Reel, Thread |
| 2 | IA práctica para negocios LatAm | IA que genera resultados, sin hype, con contexto local | Reel, Thread, Carrusel |
| 3 | El operador vs. el soñador | Mindset de ejecución vs. planificación | Thread, Caption larga |
| 4 | Construir sin equipo | Stack del solopreneur moderno | Carrusel, Thread |
| 5 | Clientes reales, resultados reales | Social proof con antes/después medible | Carrusel, Thread |

Distribución semanal objetivo: 2-3 piezas de Pilar 1 y 2, 2-3 de Pilar 3 (principalmente Threads), 1-2 de Pilar 4, 1-2 de Pilar 5.

---

## Patrones de distribución (Hormozi)

| Patrón | Mecánica | Mejor para |
|--------|----------|------------|
| Verdad Simple | 1-2 líneas. Observación directa. La brevedad ES el mensaje. | Threads, máxima distribución |
| Paradoja | "Pensabas que X. En realidad es Y." | Hero de carrusel, reel |
| Reencuadre Social | "Normalize X / El que vale la pena hace Y." | Hero de carrusel con ángulo social |
| Lista Con Fricción | Condición → lista numerada de acciones concretas | IG educativo, replies |
| Verdad Incómoda | Afirma algo que todos saben pero nadie dice | Threads, genera debate |

---

## Variedad y tracker

`carrusel/variedad.md` lleva el registro de los últimos 5 carruseles producidos:
- Pilar usado
- Patrón Hormozi del hero
- Hero start (dark/light) — alterna entre carruseles
- Posición del primer `content-light` en la secuencia

**Regla de alternación entre posts:** si el carrusel anterior empezó con `hero-dark`, el siguiente usa `hero-light`, y viceversa. Consultar "Próximo hero start" en variedad.md antes de cada generación.

---

## Reglas de plataforma (resumen)

| Plataforma | Longitud | Hashtags | CTAs | Tono |
|------------|----------|----------|------|------|
| Instagram | 150-300 palabras | 10-15 al final | Explícito: "Comenta X" | Educativo-autoritativo |
| LinkedIn | 100-180 palabras | 3-5 integrados | Pregunta de debate | Ejecutivo-estratégico |
| Threads | 80-280 chars | **Ninguno** | Sin CTA formal | Crudo, conversacional |

Ver `cnt-caption.md` para la guía completa por plataforma.

---

*Última actualización: 2026-04-10*
