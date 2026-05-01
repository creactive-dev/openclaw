# Sistema de Carruseles — CreActive Studio

> Referencia técnica completa del engine de generación de carruseles.
> Leer antes de modificar templates, agregar layouts o generar carruseles en producción.

---

## 1. Qué hace este sistema

Toma un brief JSON → renderiza HTML con Puppeteer → exporta PNGs a 1080×1350px listos para Instagram/LinkedIn.

El flujo completo:

```
ideas/{slug}.json
  → generate.js (builders por layout)
  → templates/minimalista/{layout}.html (variables inyectadas)
  → slides/{slug}/ (HTMLs para debug)
  → output/{slug}/ (PNGs finales)
```

---

## 2. Estructura de archivos

```
content-engine/carrusel/
├── generate.js              ← Motor principal (ES module)
├── package.json             ← type: "module", dep: puppeteer
├── SISTEMA.md               ← Este archivo
├── variedad.md              ← Tracker de producción (pilar, patrón, hero start)
│
├── ideas/                   ← Briefs JSON de carruseles
│   ├── avatares-ia-big-tech.json
│   ├── china-ia-educacion.json
│   ├── chile-ia-llegar-tarde.json
│   └── claude-managed-agents.json
│
├── templates/
│   └── minimalista/         ← Template set de producción
│       ├── hero-dark.html
│       ├── hero-light.html
│       ├── content.html
│       ├── content-light.html
│       ├── quote.html
│       ├── cta.html
│       ├── cta-light.html
│       └── stat.html
│
├── public/
│   └── brand/
│       ├── headshot.jpg     ← Foto de perfil Oscar (inyectada en hero y quote)
│       └── logo.png         ← Logo CreActive (footer de slides)
│
├── slides/                  ← HTMLs generados (debug / previsualización browser)
│   └── {slug}/
│
└── output/                  ← PNGs finales (entregar o publicar)
    └── {slug}/
```

---

## 3. Setup y ejecución

### Entorno Cowork (sesión nueva)

El sistema **no puede correr directamente desde la carpeta montada** (`/mnt/...`) por limitaciones del sandbox. El workaround es copiar los archivos a la carpeta de trabajo local y ejecutar desde ahí:

```bash
# 1. Crear carpeta local de trabajo
mkdir -p /sessions/{session-id}/carrusel-run
cd /sessions/{session-id}/carrusel-run

# 2. Copiar archivos esenciales desde el workspace
cp -r /sessions/{session-id}/mnt/creactive-studio/content-engine/carrusel/generate.js .
cp -r /sessions/{session-id}/mnt/creactive-studio/content-engine/carrusel/templates .
cp -r /sessions/{session-id}/mnt/creactive-studio/content-engine/carrusel/public .
cp -r /sessions/{session-id}/mnt/creactive-studio/content-engine/carrusel/ideas .
mkdir -p slides output node_modules

# 3. Instalar dependencias (NO descargar Chrome de Google)
cd /sessions/{session-id}/carrusel-run
PUPPETEER_SKIP_DOWNLOAD=true npm install

# 4. Instalar Chromium vía Playwright (evita bloqueo de storage.googleapis.com)
python3 -m playwright install chromium

# 5. Generar carrusel con Chromium de Playwright
PUPPETEER_EXECUTABLE_PATH=/sessions/{session-id}/.cache/ms-playwright/chromium-*/chrome-linux/chrome \
  node generate.js ideas/{slug}.json

# 6. Copiar output de vuelta al workspace
cp -r output/{slug} /sessions/{session-id}/mnt/creactive-studio/content-engine/carrusel/output/
```

> **Nota:** El path de Chromium incluye un número de versión (ej. `chromium-1208`). Usar glob `chromium-*/` o verificar con `ls ~/.cache/ms-playwright/`.

### Ejecución rápida (si el entorno ya está configurado)

```bash
cd /sessions/{session-id}/carrusel-run
PUPPETEER_EXECUTABLE_PATH=$(ls -d /sessions/{session-id}/.cache/ms-playwright/chromium-*/chrome-linux/chrome | head -1) \
  node generate.js ideas/{slug}.json
```

---

## 4. Schema del brief JSON

```json
{
  "titulo": "Título interno del carrusel",
  "slug": "slug-sin-espacios",
  "pilar": "1",
  "template_set": "minimalista",
  "patron_hormozi": "Verdad Simple",
  "palabras_clave": ["palabra1", "palabra2"],
  "slides": [ ... ],
  "captions": {
    "instagram": "...",
    "linkedin": "...",
    "threads": "..."
  }
}
```

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `titulo` | string | ✅ | Nombre interno. No aparece en los slides. |
| `slug` | string | ✅ | Identificador. Define el nombre de la carpeta de output. |
| `pilar` | "1"–"5" | recomendado | Pilar de contenido. Se usa para variedad.md. |
| `template_set` | string | ✅ | Siempre `"minimalista"` para producción. |
| `patron_hormozi` | string | recomendado | Patrón usado en el hook del hero. |
| `palabras_clave` | array | opcional | Palabras que se envuelven en `<span class="accent">` automáticamente en headline/titulo. |
| `slides` | array | ✅ | Lista de slides. Ver schema por layout abajo. |
| `captions` | object | recomendado | Captions listos para las 3 plataformas. |

### `palabras_clave`

Las palabras en este array se detectan automáticamente en los campos `headline` y `titulo` de cada slide y se envuelven en el color de acento del template. Alternativa: usar `*palabra*` directamente en el texto para marcar acentos manualmente.

---

## 5. Schema de slides por layout

### `hero-dark` / `hero-light`

```json
{
  "layout": "hero-dark",
  "headline": "Texto del titular. Usar *palabra* para acento rojo.",
  "subheadline": "Subtítulo explicativo. 1-2 oraciones.",
  "etiqueta": "Etiqueta de categoría"
}
```

| Campo | Visible en | Notas |
|-------|------------|-------|
| `headline` | Texto grande 116px | Soporta `*acento*`. Máx ~6 palabras para impacto visual. |
| `subheadline` | Debajo del divider | Texto secundario, opacidad reducida. |
| `etiqueta` | Pill superior izquierdo | Mayúsculas automáticas. |

**Elementos fijos (no configurables via JSON):**
- Bloque de autor inline (foto 68px + "Oscar Vergara" + badge verificado + `@oscarvergarabarros · CreActive Studio`) — aparece siempre debajo del subheadline
- `@oscarvergarabarros` en el header superior izquierdo
- Grilla, glows y detalles de circuito según variante dark/light

---

### `content` / `content-light`

```json
{
  "layout": "content",
  "etiqueta": "Etiqueta del slide",
  "titulo": "Titular del slide. Soporta *acento*.",
  "analysis": "Párrafo narrativo opcional. Aparece entre el titular y los bullets.",
  "bullets": [
    "Primer punto del slide.",
    "Segundo punto del slide.",
    "Tercer punto (máx 4 bullets)."
  ],
  "mockup": "agent"
}
```

| Campo | Visible en | Notas |
|-------|------------|-------|
| `etiqueta` | Header izquierdo | Mayúsculas automáticas. |
| `titulo` | Titular grande 48px | Soporta `*acento*`. |
| `analysis` | Entre titular y bullets | Texto narrativo con borde izquierdo rojo. Opcional. Si existe, reducir bullets a 2. |
| `bullets` | Cards con numeración | Máximo 4. Soporta `<strong>` para negritas. |
| `mockup` | Inline entre titular y bullets | `"agent"` o `"dashboard"`. Opcional. |

**Diferencias dark vs light:**
- `content` → fondo `#0C0C0C`, texto blanco, bullets con borde `rgba(255,255,255,0.06)`
- `content-light` → fondo `#F8FAFC`, texto `#0F172A`, bullets con borde `#E2E8F0`

---

### `quote`

```json
{
  "layout": "quote",
  "quote": "La frase de Oscar. Sin comillas — el template las agrega.",
  "author": "Oscar Vergara"
}
```

| Campo | Visible en | Notas |
|-------|------------|-------|
| `quote` | Texto central grande | Soporta `*acento*`. Máx ~25 palabras para que respire. |
| `author` | Bloque de autor | Siempre "Oscar Vergara". |

**Elementos fijos:** foto de perfil 80px, badge verificado, `@oscarvergarabarros · CreActive Studio`. Siempre dark.

---

### `cta` / `cta-light`

```json
{
  "layout": "cta-light",
  "texto": "Pregunta o statement que invita a la acción.",
  "cta": "Comenta PALABRA",
  "nota": "Texto secundario explicando qué recibe el usuario."
}
```

| Campo | Visible en | Notas |
|-------|------------|-------|
| `texto` | Titular 68px | La pregunta o gancho principal. Soporta `*acento*`. |
| `cta` | Botón rojo pill | Texto corto. Ej: "Comenta SISTEMA", "Agenda aquí". |
| `nota` | Debajo del botón | Texto muted, promesa específica. Opcional. |

**`cta` vs `cta-light`:** elegir según la posición en la secuencia de alternación. Ver sección 6.

---

### `stat`

```json
{
  "layout": "stat",
  "etiqueta": "Categoría del dato",
  "number": "+300%",
  "label": "Crecimiento operacional",
  "context": "En 8 meses implementando sistemas de seguimiento en PedidosYa."
}
```

Siempre dark. Usar solo con datos reales — nunca inventar métricas.

---

## 6. Reglas de diseño (OBLIGATORIAS)

### Alternación dark/light

La regla es estricta: **cada slide alterna el color del anterior**. Se aplica a todos los layouts incluyendo CTA.

**Dentro de un carrusel:**

| Slide | Dark start | Light start |
|-------|-----------|-------------|
| 1 (hero) | `hero-dark` | `hero-light` |
| 2 | `content` (D) | `content-light` (L) |
| 3 | `content-light` (L) | `content` (D) |
| 4 | `content` (D) | `content-light` (L) |
| 5 | `quote` (D, siempre) | `quote` (D, siempre) |
| 6 (cta) | `cta-light` (L) | `cta` (D) |

> `quote` es siempre dark — no tiene versión light. Acepta la ruptura de 2 slides oscuros consecutivos cuando quote y CTA caen juntos.

**Entre carruseles (hero start):**

Cada nuevo carrusel invierte el color de inicio del anterior. Consultar "Próximo hero start" en `variedad.md` antes de generar. Nunca elegir por intuición.

---

### Mockups disponibles

El campo `mockup` inyecta una ilustración funcional **inline**, entre el titular y los bullets. No ocupa columna lateral — forma parte del flujo vertical del contenido.

| Tipo | CSS class | Usar cuando... |
|------|-----------|----------------|
| `"agent"` | `.mockup-agent-h` | Agentes IA, WhatsApp bots, automatización conversacional, servicio al cliente |
| `"dashboard"` | `.mockup-dashboard` | Resultados, métricas, antes/después, crecimiento, KPIs |

Cuando hay mockup: reducir bullets a 2 máximo. El mockup + análisis + 4 bullets colapsa el espacio.

---

### Sintaxis de acentos

Para resaltar palabras en rojo (`#FF3231`):

```
"headline": "El sistema que *nunca falla*."
```

Genera: `El sistema que <span class="accent">nunca falla</span>.`

Alternativa: listar en `palabras_clave` del brief (inyección automática en todos los slides).

---

## 7. Paleta de colores por template

### Dark (hero-dark, content, quote, cta)

| Rol | Valor |
|-----|-------|
| Fondo | `#050505` (hero) / `#0C0C0C` (content/cta) |
| Texto principal | `#ffffff` |
| Texto secundario | `rgba(255,255,255,0.64)` |
| Acento | `#FF3231` |
| Azul métrica | `#578BDE` |
| Teal IA | `#2FB8C5` |
| Borde bullet | `rgba(255,255,255,0.06)` |
| Grilla | `rgba(255,255,255,0.022)` — 48×48px |

### Light (hero-light, content-light, cta-light)

| Rol | Valor |
|-----|-------|
| Fondo | `#F8FAFC` |
| Texto principal | `#0F172A` |
| Texto secundario | `#475569` |
| Acento | `#FF3231` |
| Azul métrica | `#578BDE` |
| Borde bullet | `#E2E8F0` |
| Fondo bullet | `#FFFFFF` con `box-shadow: 0 2px 8px rgba(15,23,42,0.06)` |
| Grilla | `rgba(0,0,0,0.03)` — 48×48px |

### Tipografía (todos los templates)

| Elemento | Tamaño | Peso |
|----------|--------|------|
| Hero headline | 116px | 800 |
| Hero letter-spacing | -5.5px | — |
| Content titular | 48px | 800 |
| Content bullet | 22px | 400 |
| Analysis | 22px | 400 |
| Etiqueta | 14px | 700 + 2.5px letter-spacing |
| Handle/footer | 20px | 700 |
| Autor nombre (hero) | 22px | 700 |
| Autor handle (hero) | 16px | 400 |
| Foto autor (hero) | 68×68px | — |
| Foto autor (quote) | 80×80px | — |

Font: **Plus Jakarta Sans** (Google Fonts) — pesos 400, 600, 700, 800.

---

## 8. Variables de template por layout

Referencia de todas las variables `{{variable}}` que acepta cada template:

| Layout | Variables |
|--------|-----------|
| `hero-dark` / `hero-light` | `headshot_path`, `slide_num`, `progress_pct`, `etiqueta_html`, `headline_html`, `subheadline_html` |
| `content` / `content-light` | `slide_num`, `progress_pct`, `etiqueta`, `headline_html`, `analysis_html`, `bullets_html`, `mockup_html`, `mockup_class` |
| `quote` | `headshot_path`, `slide_num`, `progress_pct`, `quote_html`, `author` |
| `cta` / `cta-light` | `slide_num`, `progress_pct`, `headline_html`, `cta`, `nota_html` |
| `stat` | `slide_num`, `progress_pct`, `etiqueta`, `number`, `label`, `context` |

`progress_pct` se calcula automáticamente en `generate.js` (índice/total × 100) — no hace falta incluirlo en el JSON.

---

## 9. Output y sincronización

Después de cada generación, sincronizar con el workspace:

```bash
# Sincronizar output al workspace
cp -r output/{slug} /sessions/{session-id}/mnt/creactive-studio/content-engine/carrusel/output/

# Sincronizar JSON brief al workspace (si se creó localmente)
cp ideas/{slug}.json /sessions/{session-id}/mnt/creactive-studio/content-engine/carrusel/ideas/

# Sincronizar templates si se modificaron
cp templates/minimalista/*.html /sessions/{session-id}/mnt/creactive-studio/content-engine/carrusel/templates/minimalista/

# Sincronizar generate.js si se modificó
cp generate.js /sessions/{session-id}/mnt/creactive-studio/content-engine/carrusel/
```

Luego actualizar `variedad.md` con el nuevo registro.

---

## 10. Agregar un nuevo layout

1. Crear `templates/minimalista/{nombre}.html` con las variables `{{variable}}` necesarias
2. Crear `build{Nombre}(slide, num, set)` en `generate.js`
3. Registrar en el objeto `BUILDERS`: `'{nombre}': build{Nombre}`
4. Documentar en la tabla de layouts de este archivo (sección 5)
5. Documentar en `cnt-carrusel.md` en la sección "Layout disponibles"
6. Sincronizar `generate.js` y el nuevo template al workspace

---

## 11. Agregar un nuevo tipo de mockup

1. Agregar el CSS del mockup en `content.html` y `content-light.html` (versiones dark y light)
2. Agregar el HTML del mockup en la función `buildMockup(type)` de `generate.js`
3. Documentar en "Tipos de mockup disponibles" de `cnt-carrusel.md`

---

*Última actualización: 2026-04-10*
