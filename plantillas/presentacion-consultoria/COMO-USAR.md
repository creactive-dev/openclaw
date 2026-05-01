# Plantilla: Presentación de Consultoría CreActive

## Qué es esto

`template.html` es una presentación Reveal.js de 12 slides con el design system dark de CreActive (fondo #0F172A, gradiente signature, Plus Jakarta Sans + DM Sans). Se usa para sesiones de consultoría, propuestas comerciales y feedback de cliente.

**Navegación:** flechas ← → · Pantalla completa: `F` · PDF: añadir `?print-pdf` a la URL y `Cmd+P`

---

## Cómo crear una presentación nueva

### Paso 1 — Copiar el template al cliente

```bash
cp plantillas/presentacion-consultoria/template.html \
   clientes/{slug}/outputs/presentacion-{tipo}-{fecha}.html
```

Ejemplos de nombre:
- `presentacion-consultoria-2026-04-20.html`
- `presentacion-propuesta-onboarding-2026-05-01.html`
- `presentacion-diagnostico-2026-05-15.html`

### Paso 2 — Rellenar las variables

Buscar y reemplazar todos los `{{VARIABLE}}` con el contenido del cliente. Los nombres son descriptivos.

Variables de identidad (todas las slides):
| Variable | Qué va |
|----------|--------|
| `{{SESSION_TIPO}}` | "Sesión de Consultoría Estratégica" / "Propuesta Comercial" / "Diagnóstico" |
| `{{SESSION_NUMERO}}` | Número de sesión: 1, 2, 3… |
| `{{PITCH_TITULO_L1}}` | Primera línea del título grande de portada |
| `{{PITCH_TITULO_L2}}` | Segunda línea (se muestra en teal) |
| `{{PITCH_SUBTITULO}}` | Subtítulo de portada — una línea |
| `{{CLIENT_NOMBRE}}` | Empresa / Producto del cliente |
| `{{CLIENT_CONTACTO}}` | Nombre del contacto · Ciudad |
| `{{SESSION_FECHA}}` | Fecha larga: "20 Abril 2026" |
| `{{SESSION_CONTEXTO}}` | Contexto en una línea: "Propuesta de onboarding" |

El resto de variables siguen el mismo patrón: `{{SLIDE_ELEMENTO_CAMPO}}`.

### Paso 3 — Slides opcionales

El template tiene 12 slides por defecto. Para presentaciones más cortas:
- Eliminar las secciones `<section>` que no necesites
- Los slides de diagnóstico (5–8) se pueden comprimir en 2 si el feedback LinkedIn no aplica
- Slide 11 (propuesta/sinergia) es opcional si no hay colaboración

### Paso 4 — Verificar antes de presentar

- [ ] Abrir en Chrome a pantalla completa (`F`)
- [ ] Navegar todos los slides con ← →
- [ ] Verificar que no queden `{{VARIABLES}}` sin rellenar
- [ ] Comprobar que el footer de cada slide tiene la fuente correcta

---

## Cómo servirla desde la web de CreActive

La web de CreActive (Next.js, repo `creactive-dev/creactive`) sirve archivos estáticos desde `/public`.

**Estructura recomendada:**

```
creactive-studio-landing/
└── public/
    └── propuestas/
        ├── autoritas-ai-2026-04-20.html
        ├── pumpalcerro-2026-05-01.html
        └── ...
```

**URL resultante:** `creactivestudio.agency/propuestas/autoritas-ai-2026-04-20.html`

**Para añadir una presentación:**

```bash
# Copiar el archivo al public de la web
cp clientes/{slug}/outputs/presentacion-{tipo}-{fecha}.html \
   clientes/creactive-studio/outputs/creactive-studio-landing/public/propuestas/{slug}-{fecha}.html

# Commitear y pushear → Vercel despliega automáticamente
cd clientes/creactive-studio/outputs/creactive-studio-landing
git add public/propuestas/
git commit -m "add: propuesta {cliente} {fecha}"
git push
```

La presentación queda en vivo en ~30 segundos sin configuración adicional.

**Para proteger con contraseña (opcional):** añadir Basic Auth en `vercel.json`:
```json
{
  "headers": [
    {
      "source": "/propuestas/(.*)",
      "headers": [{ "key": "X-Robots-Tag", "value": "noindex" }]
    }
  ]
}
```
Esto no bloquea el acceso pero evita indexación en Google. Para auth real usar Vercel Password Protection (plan Pro).

---

## Estructura de componentes (referencia rápida)

| Clase | Uso |
|-------|-----|
| `.card` | Tarjeta de fondo oscuro. Variantes: `.rl` (borde rojo), `.tl` (teal), `.bl` (azul) |
| `.ba-grid` | Grid antes/después 2 columnas. Hijos: `.before` (rojo) y `.after` (teal) |
| `.dc` | Callout con número o dato grande + texto explicativo |
| `.rc` | Risk card — icono + título rojo + descripción |
| `.steps` | Lista de pasos numerados. `.step-n.warn` para alertas en rojo |
| `.chk` | Lista con checkmarks teal |
| `.quote` | Quote con borde azul a la izquierda |
| `.eblock` | Bloque estilo email (asunto + cuerpo) |
| `.fcard` | Feature card — fondo azul tenue |
| `.ns-list` | Lista de siguientes pasos con fecha a la derecha |
| `.ai` | Agenda item — número cuadrado + título + descripción |
| `.g2` `.g3` `.g4` | Grids de 2, 3 o 4 columnas |
| `.hl-red` `.hl-teal` `.hl-blue` | Colores de acento inline |
| `.sf` | Footer fijo de slide (siempre al fondo) |
| `.slide-label` | Etiqueta de categoría arriba del título |
| `.slide-h` | Título estándar de slide (1.8rem, 800) |
| `.portada-*` | Clases exclusivas del slide 1 (portada) |

---

## Tipos de presentación soportados

Con el mismo template se pueden hacer:

- **Consultoría estratégica** — feedback comercial post-reunión (caso Autoritas AI)
- **Propuesta de onboarding** — diagnóstico + alcance + precio (adaptar slides 3–4 a scope)
- **Diagnóstico de presencia digital** — auditoría LinkedIn/web/contenido (slides 5–8)
- **Reporte de resultados** — métricas + próximos 30 días (slide 3 → KPIs, slide 9 → roadmap)
- **Sesión de estrategia de contenido** — pilares + calendario + primer post (slides 9–10)
