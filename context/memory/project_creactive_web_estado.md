---
name: CreActive Studio Website
description: Estado del proyecto de la web propia de la agencia (creactivestudio.agency) — landing Next.js con i18n ES/EN, light mode forzado
type: project
originSessionId: 517309f1-e7ca-4ddd-abdf-42148fbd4952
---
# CreActive Studio — Web propia de la agencia

## Estado: En producción, iterando (2026-04-27)

**Why:** Proyecto interno — esta landing ES el portafolio de CreActive. Estándar de calidad máximo.

**How to apply:** Cualquier cambio debe mantener la coherencia del sistema de tokens CSS, el sistema i18n, y la estructura de directorios establecida.

---

## Stack
- Next.js 14 + Tailwind CSS 3 + Framer Motion + TypeScript
- Deploy: Vercel (auto-deploy en push a main)
- Repo: https://github.com/creactive-dev/creactive.git (branch: main)
- Ruta local: `clientes/creactive-studio/outputs/creactive-studio-landing/`

---

## Dark mode — ELIMINADO (2026-04-27)

Dark mode fue implementado pero luego removido en sesión 2026-04-27.
- `Providers.tsx`: `forcedTheme="light"` + `enableSystem={false}`
- `Navbar.tsx`: sin `<ThemeToggle />` (desktop y mobile)
- La sección Booking usa fondo `#0C1525` hardcoded — es la única sección oscura, intencional para contraste.

---

## Estructura de secciones (orden en page.tsx)
1. Navbar
2. Hero (`pt-44` — espacio entre badge y navbar)
3. AboutOscar (`#oscar`)
4. Problem
5. Services (`#servicios`)
6. ToolsStrip (logos en color, sin `grayscale`)
7. HowWeWork (`#proceso`)
8. CaseStudies (`#casos`)
9. Testimonials
10. Niches (dos columnas: criterios + sectores)
11. FAQ (`#faq`)
12. BookDiscovery (`#agendar`) — layout split dark
13. Footer

---

## CaseStudies — logos de clientes (2026-04-27)

Cada card muestra el logo del cliente en el panel izquierdo (via `Image` next/image con `fill` + `object-contain`).

| Cliente | Logo path |
|---------|-----------|
| Constanza Nutrición | `/logos/constanza-nutricion.png` |
| Pumpalcerro | `/logos/pumpalcerro.png` |
| Feld's Kitchen | `/logos/felds-kitchen.png` |

**Gotcha:** El archivo original del logo de Felds tenía espacios y paréntesis (`Logo Felds Kitchen (4).png`). Se copió como `felds-kitchen.png`. El original sigue en `public/logos/` sin trackear.

`CaseItem` en `types.ts` tiene campo `logo?: string` (opcional, por si un caso no tiene logo).

---

## BookDiscovery — Rediseño (2026-04-27)

**Layout:** Split 2 columnas en desktop. Fondo oscuro `#0C1525` con glows decorativos.
- Izquierda: badge, título, subtítulo, 4 bullets de beneficios, trust badges (sticky en desktop)
- Derecha: widget GHL embebido

**GHLCalendar.tsx:** URL real hardcodeada (ya no usa env variable).
```
URL: https://crm.creactivestudio.agency/widget/booking/jWoatPHeZLQyhDOh0oCj
ID iframe: jWoatPHeZLQyhDOh0oCj_1777224108146
Script: https://crm.creactivestudio.agency/js/form_embed.js
```
**Gotcha crítico:** El script `form_embed.js` se carga via `useEffect` — si se carga con `<Script>` de Next.js o en el HTML puede causar hydration errors. El useEffect revisa si ya existe antes de insertarlo.

Duración del discovery: **45 minutos** (fue 30, corregido en 4 lugares: badge, subtitle, trust badge ES y EN).

---

## Copy — Estado actual (2026-04-27)

Tres pasadas de copy aplicadas:

1. **Marketing → Operación** — hero, problems, cases title, services order, niches
2. **Voseo argentino → tuteo LATAM neutro** — `vos/querés/sabés/entendés` → `ti/quieres/sabes/entiendes`, `plata` → `dinero`
3. **Humanización** — eliminar em-dashes encadenados, patrones "Sin X. Sin Y.", construcciones tipo IA. Narración de casos como historias reales.

**Voz de referencia:** `content-engine/brand/voz.md` — conversacional, directo, con datos, spanglish técnico natural.

**Testimoniales:** NO modificar — son citas reales de clientes.

---

## Sistema i18n

| Archivo | Propósito |
|---------|-----------|
| `lib/i18n/types.ts` | Tipo `Dictionary` completo |
| `lib/i18n/es.ts` | Español LATAM neutro (idioma por defecto) |
| `lib/i18n/en.ts` | Inglés completo |
| `lib/i18n/context.tsx` | `LanguageProvider` + `useTranslations()` hook |
| `components/ui/LanguageToggle.tsx` | Toggle ES/EN |

**Patrón crítico de keys en listas animadas:** Siempre `key={index}` (no texto traducible) en `motion.div` que mapean arrays. Texto como key causa unmount al cambiar idioma → Framer Motion con `once: true` lo deja invisible.

---

## Iconos en Problem.tsx y Niches.tsx (2026-04-27)

`BarChart3` reemplazado por `AlertCircle` (rojo `text-brand-red`) para el criterion "El negocio no funciona sin ti". Ambos componentes actualizados: import + iconMap + iconColorMap.

---

## Gotchas de sesión

- **Build local lento (~3 min)** — no esperar el build local para pushear. Vercel lo hace solo y es más rápido confirmar en el log de Vercel.
- **Error Vercel anterior:** Al eliminar `<ThemeToggle />` del Navbar se borró accidentalmente el tag `<a` del CTA, dejando solo `<`. Build fail. Siempre revisar el JSX alrededor cuando se elimina un componente inline.
- **Logos con espacios en nombre:** Next.js los sirve OK pero son difíciles de usar en código. Siempre copiar/renombrar antes de trackear en git.

---

## Logos en ecosistema (ToolsStrip) — gotcha svgl

svgl.app no tiene URLs sin sufijo para algunos logos. Regla:
- Claude AI: `claude-ai-wordmark-icon_light.svg` (no `claude-ai-wordmark-icon.svg`)
- Next.js: `nextjs_icon_dark.svg` (no `nextjs.svg`)
- Para verificar URLs: `curl -s "https://api.svgl.app?search=<nombre>"` devuelve JSON con rutas correctas
- Todos los demás logos del strip validados con HTTP 200 ✅

## Favicon (2026-04-27)

`app/icon.png` = `public/logo footer.png` copiado. Next.js App Router lo detecta automáticamente. Sin cambios en layout.tsx.

## Niches — Sectores (2026-04-27)

Rivas Legal removido del campo `note` de "Legal y servicios profesionales" en ES y EN. El sector sigue apareciendo como pill pero sin referencia al caso.

## Pendientes
- QA visual en producción Vercel — verificar que todos los deploys pasaron OK
- Conectar dominio `creactivestudio.agency`
- OG image
- Verificar que form_embed.js de GHL redimensiona el iframe correctamente en producción

---

## Historial de commits relevantes

| Commit | Descripción |
|--------|-------------|
| `bca3ceb` | Humanizar copy — sacar tono IA, alinear con voz Oscar |
| `23ec7c2` | Voseo argentino → tuteo LATAM neutro |
| `00a3f1b` | Copy marketing → transformación operacional |
| `317078b` | Fix duración discovery 30 → 45 min |
| `dbcbb64` | Logos clientes en casos + Booking redesign |
| `c397004` | Fix: tag `<a` roto en Navbar (Vercel build fail) |
| `e6f8f47` | Light mode, hero spacing, services copy, ecosistema, casos reales, niches |
| `53415ad` | i18n ES/EN + dark mode (luego removido) + Niches rebuild + mobile fixes |
