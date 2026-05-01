# Design System Master File

> **LOGIC:** When building a specific page, first check `design-system/pages/[page-name].md`.
> If that file exists, its rules **override** this Master file.
> If not, strictly follow the rules below.

---

**Project:** CreActive Studio
**Generated:** 2026-03-28
**Category:** Consulting Agency — AI Transformation
**Style:** Light Moderno + Trust & Authority

---

## Global Rules

### Color Palette

| Role | Hex | CSS Variable (real) | Tailwind Token | Uso |
|------|-----|---------------------|----------------|-----|
| Brand Red | `#FF3231` | `--color-brand-red` | `brand-red` | CTAs principales, energía, acción |
| Brand Blue | `#578BDE` | `--color-brand-blue` | `brand-blue` | Heading principal, métricas, gradientes, autoridad |
| Brand Teal | `#2FB8C5` | `--color-brand-teal` | `brand-teal` | IA/innovación, badges, acentos terciarios |
| Surface (principal) | `#FFFFFF` | `--color-surface` | `surface` | Secciones principales, cards, modals |
| Surface Alt | `#F8FAFC` | `--color-surface-alt` | `surface-alt` | Secciones alternas (slate-50) |
| Surface Muted | `#F1F5F9` | `--color-surface-muted` | `surface-muted` | Fondos de elementos secundarios |
| Text Primary | `#0F172A` | `--color-text-primary` | `text-primary` | Headings, texto principal |
| Text Body | `#334155` | `--color-text-body` | `text-body` | Cuerpo de texto |
| Text Muted | `#64748B` | `--color-text-muted` | `text-muted` | Labels, metadata |
| Border | `#E2E8F0` | `--color-border` | `border` | Bordes de cards, inputs |
| Success | `#16A34A` | — | `green-600` | Estados positivos, métricas "después" |
| Error | `#DC2626` | — | `red-600` | Errores, validación |

> **Importante:** Los tokens en el código usan `surface` (no `bg`). Siempre referenciar `bg-surface`, `bg-surface-alt`, `text-text-primary`, `text-text-body` — no usar clases de Tailwind directas como `bg-slate-50`.

**Notas de uso de color:**
- `brand-red` (#FF3231) es el color de acción — SOLO para CTAs y elementos que requieren atención inmediata
- `brand-blue` (#578BDE) es el color de confianza — heading principal, métricas, gradientes, elementos de autoridad
- `brand-teal` (#2FB8C5) es el color de innovación — para badges de IA, highlights técnicos, acentos secundarios
- Nunca usar los 3 colores de marca juntos en el mismo componente — máximo 2 por sección
- **Modo:** El sitio es light por defecto. Dark mode implementado (`darkMode: 'class'`) y disponible via ThemeToggle en navbar.

**Patrón de gradient border (uso en cards de alto impacto):**
```css
/* Animated gradient border — usar en credential cards, featured cards */
.gradient-border {
  background: linear-gradient(to right, #578BDE, #2FB8C5, #FF3231);
  /* opacity-0 por defecto, opacity-100 en hover */
}
/* El contenido va en un div inset-[1px] con bg-surface para el "hueco" */
```
Este patrón aparece en las credential cards de AboutOscar y es el de mayor impacto visual de la landing.

### Typography

- **Heading Font:** Plus Jakarta Sans (500, 600, 700, **800**)
- **Body Font:** DM Sans (400, 500, 700)
- **Mood:** friendly, modern, tech, approachable, professional
- **Best For:** SaaS, consulting, AI products, professional services

**Google Fonts:**
```css
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');
```

**Tailwind Config (real — usar esta versión, no la anterior):**
```js
fontFamily: {
  heading: ['var(--font-heading)', 'sans-serif'],
  body: ['var(--font-body)', 'sans-serif'],
}
```

**Escala tipográfica:**

| Token | Size | Weight | Font | Uso |
|-------|------|--------|------|-----|
| `display` | 56px / 3.5rem | **800** | Heading | Hero headline |
| `blockquote-hero` | `text-3xl md:text-5xl lg:text-6xl` | **800** | Heading | Citas hero, statements de alto impacto (AboutOscar) |
| `h1` | 48px / 3rem | 700 | Heading | Títulos de página |
| `h2` | 36px / 2.25rem | 700 | Heading | Títulos de sección |
| `h3` | 24px / 1.5rem | 600 | Heading | Subtítulos |
| `h4` | 20px / 1.25rem | 600 | Heading | Card titles |
| `body-lg` | 18px / 1.125rem | 400 | Body | Lead text, subheadlines |
| `body` | 16px / 1rem | 400 | Body | Cuerpo general |
| `body-sm` | 14px / 0.875rem | 400 | Body | Captions, labels |
| `caption` | 12px / 0.75rem | 500 | Body | Badges, tags |

> **Nota:** El peso 800 (`font-extrabold`) es el que da carácter a la landing — no usar 700 en headings principales.

### Spacing System

| Token | Value | Usage |
|-------|-------|-------|
| `--space-xs` | `4px` / `0.25rem` | Tight gaps |
| `--space-sm` | `8px` / `0.5rem` | Icon gaps, inline spacing |
| `--space-md` | `16px` / `1rem` | Standard padding |
| `--space-lg` | `24px` / `1.5rem` | Card padding |
| `--space-xl` | `32px` / `2rem` | Large gaps |
| `--space-2xl` | `48px` / `3rem` | Between sections (mobile) |
| `--space-3xl` | `64px` / `4rem` | Between sections (desktop) |
| `--space-4xl` | `96px` / `6rem` | Hero padding |

### Border Radius

| Token | Value | Usage |
|-------|-------|-------|
| `rounded-sm` | `6px` | Badges, tags |
| `rounded-md` | `8px` | Buttons, inputs |
| `rounded-lg` | `12px` | Cards |
| `rounded-xl` | `16px` | Featured cards, modals |
| `rounded-2xl` | `24px` | Hero containers |

### Shadow Depths

| Level | Value | Usage |
|-------|-------|-------|
| `--shadow-sm` | `0 1px 2px rgba(0,0,0,0.05)` | Subtle lift |
| `--shadow-md` | `0 4px 6px -1px rgba(0,0,0,0.07), 0 2px 4px -2px rgba(0,0,0,0.05)` | Cards default |
| `--shadow-lg` | `0 10px 15px -3px rgba(0,0,0,0.08), 0 4px 6px -4px rgba(0,0,0,0.05)` | Cards hover |
| `--shadow-xl` | `0 20px 25px -5px rgba(0,0,0,0.1), 0 8px 10px -6px rgba(0,0,0,0.05)` | Hero, featured |

---

## Component Specs

### Buttons

```css
/* Primary CTA — Brand Red */
.btn-primary {
  background: #FF3231;
  color: white;
  padding: 12px 28px;
  border-radius: 8px;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-weight: 600;
  font-size: 16px;
  transition: all 200ms ease;
  cursor: pointer;
  box-shadow: 0 4px 6px -1px rgba(255, 50, 49, 0.25);
}

.btn-primary:hover {
  background: #E62D2C;
  box-shadow: 0 6px 12px -2px rgba(255, 50, 49, 0.35);
  transform: translateY(-1px);
}

/* Secondary — Outline */
.btn-secondary {
  background: transparent;
  color: #0F172A;
  border: 2px solid #E2E8F0;
  padding: 12px 28px;
  border-radius: 8px;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-weight: 600;
  font-size: 16px;
  transition: all 200ms ease;
  cursor: pointer;
}

.btn-secondary:hover {
  border-color: #578BDE;
  color: #578BDE;
}
```

### Cards

```css
.card {
  background: white;
  border: 1px solid #E2E8F0;
  border-radius: 12px;
  padding: 24px;
  box-shadow: var(--shadow-sm);
  transition: all 200ms ease;
  cursor: pointer;
}

.card:hover {
  box-shadow: var(--shadow-lg);
  border-color: #578BDE40;
  transform: translateY(-2px);
}
```

### Badges / Tags

```css
.badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  font-family: 'DM Sans', sans-serif;
}

.badge-teal {
  background: #2FB8C510;
  color: #2FB8C5;
  border: 1px solid #2FB8C520;
}

.badge-blue {
  background: #578BDE10;
  color: #578BDE;
  border: 1px solid #578BDE20;
}
```

---

## Style Guidelines

**Style:** Light Moderno + Trust & Authority

**Keywords:** Clean whitespace, subtle shadows, credential badges, case studies with metrics, professional typography, strategic color accents

**Best For:** Consulting agencies, AI/tech services, professional services, B2B

**Key Effects:**
- Badge hover effects con color teal
- Metric counter animations (whileInView)
- Card hover lift con shadow progression
- Smooth section reveal con staggerChildren
- Stat number count-up animations

### Page Pattern: Hybrid (Transformation + Social Proof)

- **Section Order:** Hero → Problem → Services → Methodology → Cases → About → Niches → FAQ → Tools → CTA
- **CTA Placement:** Hero (primary) + After Cases (secondary) + Bottom (final)
- **Color Strategy:** Secciones alternas entre #F8FAFC y #FFFFFF. Brand colors como acentos estratégicos.
- **Conversion Strategy:** Posicionamiento → Empatía → Capacidad → Proceso → Prueba → Credibilidad → Conversión

---

## Animation Guidelines (Framer Motion)

```typescript
// Reveal on scroll
const fadeInUp = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5, ease: "easeOut" } }
}

// Stagger children
const staggerContainer = {
  visible: { transition: { staggerChildren: 0.1 } }
}

// Scale on hover (cards)
const cardHover = {
  whileHover: { y: -4, transition: { duration: 0.2 } }
}

// Number counter
// Use whileInView with a count-up library or custom hook

// IMPORTANT: Always check prefers-reduced-motion
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
```

---

## Componentes clave implementados

**PixelCanvas** — Canvas animado con píxeles que aparecen/desaparecen aleatoriamente. Se usa como background sutil en las credential cards de AboutOscar. Parámetros: `density` (0.01 por defecto) y `maxPixels` (8 por defecto). No abusarlo — funciona por su sutileza.

**TextRotate** — Rotador de palabras animado con Framer Motion. Usado en el Hero para `rotatingWords`. Ideal para headlines que quieren mostrar variaciones de un mismo concepto.

**PixelCanvas + Gradient border** — Combinación signature de la landing. El gradient border aparece en hover (`opacity-0` → `opacity-100`) y el PixelCanvas corre en el fondo del card. Juntos crean el efecto de "card vivo" que distingue la landing.

---

## Anti-Patterns (Do NOT Use)

- **Emojis as icons** — Use SVG icons (Lucide React)
- **Missing cursor:pointer** — All clickable elements must have cursor:pointer
- **Layout-shifting hovers** — Avoid scale transforms that shift surrounding content
- **Low contrast text** — Maintain 4.5:1 minimum contrast ratio
- **Instant state changes** — Always use transitions (150-300ms)
- **Invisible focus states** — Focus states must be visible
- **Generic content** — Todo personalizado al contexto de CreActive
- **No credentials** — Siempre mostrar track record y métricas
- **AI purple/pink gradients** — No gradientes genéricos de IA (el nuestro es blue→teal→red, no purple)
- **Inter/Roboto/Arial** — Usar Plus Jakarta Sans + DM Sans
- **3 brand colors en mismo componente** — Máximo 2 colores de marca por sección (excepción: gradient border en hover, que es intencional)
- **Peso 700 en headings principales** — Usar 800 (`font-extrabold`) para statements de alto impacto
- **`bg-slate-*` directo** — Usar los tokens del design system (`bg-surface`, `bg-surface-alt`)

---

## Icon Set

**Library:** Lucide React (`lucide-react`)
**Size:** 24x24 default, 20x20 para inline, 32x32 para features
**Stroke:** 1.5px (default de Lucide)

Iconos sugeridos por sección:
- Servicios: `Brain` (IA), `BarChart3` (marketing), `Globe` (web), `Workflow` (automation), `Code` (SaaS), `Compass` (consulting)
- Proceso: `MessageCircle` (discovery), `Search` (diagnóstico), `FileText` (propuesta), `Rocket` (ejecución), `RefreshCw` (iteración)
- General: `ArrowRight`, `Check`, `ChevronDown` (accordion), `Calendar` (booking), `Phone` (WhatsApp)

---

## Pre-Delivery Checklist

- [ ] No emojis used as icons (use Lucide React SVGs)
- [ ] All icons from Lucide React (consistent set)
- [ ] `cursor-pointer` on all clickable elements
- [ ] Hover states with smooth transitions (150-300ms)
- [ ] Light mode text contrast 4.5:1 minimum
- [ ] Focus states visible for keyboard navigation
- [ ] `prefers-reduced-motion` respected in Framer Motion
- [ ] Responsive: 375px, 768px, 1024px, 1440px
- [ ] No content hidden behind fixed navbar
- [ ] No horizontal scroll on mobile
- [ ] Brand colors used strategically (max 2 per section)
- [ ] Plus Jakarta Sans for headings, DM Sans for body
- [ ] No generic/placeholder content
