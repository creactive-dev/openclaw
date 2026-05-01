---
name: Nutrisco Landing Fundadores — estado
description: Landing de lanzamiento fundadores para Nutrisco. Branding alineado con Constanza Nutrición (navbar real, Montserrat, Hero claro, Pill system). Repo en GitHub. Deploy Vercel pendiente.
type: project
originSessionId: ce708c60-f786-4a6c-873c-5df541f5850f
---
## Estado actual

Landing completa en código con branding alineado a las landings de Constanza en producción. **Repo en GitHub (`creactive-dev/nutrisco-landing`). Pendiente: deploy Vercel + env vars + DNS antes del 3 mayo.**

**Ruta local:** `clientes/constanza-nutricion/outputs/landing-fundadores/`
**Repo:** https://github.com/creactive-dev/nutrisco-landing

---

## Completado — sesión 2026-04-27 (branding + repo)

- ✅ Servidor local levantado en localhost:3000
- ✅ Navbar: logo oficial `navbar.png` (sandía roja + "CONSTANZA JIMÉNEZ PASCHOLD" en azul + "Nutrición & Salud") — reemplaza el SVG vectorial genérico de hoja
- ✅ BarraUrgencia: gradiente coral 3 pasos + botón "Ver precio →" integrado
- ✅ Assets reales integrados: `constanzaoficial.jpeg` (foto en clínica, bata blanca), `mockuphome.png` (iPhone app con progreso + check-in)
- ✅ Colores dark sections: `carbon` → `#0E2233`, `dark-section` → `#0C1E2E`, `dark-card` → `#0F2535` (azul navy derivado del azul del logo, NO negro puro)
- ✅ Fuente display: Playfair Display → **Montserrat** (700/800/900) — match con las dos landings de referencia
- ✅ Hero: oscuro → claro (`bg-crema`), headline `font-black` text-carbon, Google Reviews badge, social proof en card blanca
- ✅ Componente `<Pill>` reutilizable — 4 variantes: `solid` / `outline-coral` / `glass-light` / `glass-dark`
- ✅ Pill aplicado en: Hero eyebrow, ComoFunciona, SobreConstanza, Pricing, Testimonios
- ✅ ComoFunciona: Pill "El método único" + números en círculo coral editorial (w-20 h-20)
- ✅ PuenteReto: rediseñado desde texto plano a → Pill eyebrow + callout card navy con highlight coral + 2 columnas comparativas (reto vs nutrisco)
- ✅ SobreConstanza: Pill `glass-dark` eyebrow + foto real `constanzaoficial.jpeg` con `object-top` aspect-ratio 3:4
- ✅ Pricing: Pill `outline-coral` + headline `font-black` + CTA con `shadow-[0_8px_28px_rgba(233,69,85,0.5)]`
- ✅ Testimonios: `SHOW_TESTIMONIALS = true`, cards con avatar inicial (letra), stars SVG, badge BETA en placeholders
- ✅ CTAFinal: `font-black + tracking-tight` con Montserrat
- ✅ TypeScript: 0 errores (`npx tsc --noEmit`)
- ✅ Git init + primer commit (66 archivos) + **force push** a `creactive-dev/nutrisco-landing`
  - El remoto tenía 2 commits de versión anterior (v1) — se sobreescribió intencionalmente

---

## Completado — sesión 2026-04-25 (build inicial)

- ✅ 60 archivos creados desde cero
- ✅ Build `next build` → 0 errores TypeScript
- ✅ 16 secciones: BarraUrgencia sticky, Hero (parallax Framer Motion), BarraConfianza, Problema, PuenteReto, QueEsNutrisco, ComoFunciona, ProductPreview (carrusel mobile), QueIncluye, SobreConstanza, Testimonios, Pricing, Garantia, FAQ acordeón, CTAFinal, Footer
- ✅ Modo dual pre-registro/venta: switch automático por fecha + override `NEXT_PUBLIC_LAUNCH_MODE`
- ✅ Form pre-registro custom + POST `/api/preregistro` → webhook GHL
- ✅ Bloque isapre (boleta exenta IVA + reembolso)
- ✅ BannerCookies que gatean GA + Meta Pixel
- ✅ README + `.env.local.example` documentado

---

## Pendiente de CreActive (ordenado por urgencia)

| Tarea | Urgencia | Para qué |
|-------|----------|----------|
| Deploy a Vercel (root dir: `landing-fundadores/`) | 🔴 | Landing live — lanzamiento 3 mayo |
| Confirmar dominio (nutrisco.cl / fundadores.constanzanutricion.cl) | 🔴 | DNS antes del 3 mayo |
| Obtener URL webhook GHL pre-registro + crear tag `pre-registro-fundadores` | 🔴 | API route /api/preregistro |
| Setear `NEXT_PUBLIC_LAUNCH_MODE=preregistro` en Vercel | 🔴 | Switch correcto hasta el 3 mayo |
| El 3-mayo 9 AM: remover `NEXT_PUBLIC_LAUNCH_MODE` → redeploy | 🔴 | Activa modo venta automático |
| Setear `NEXT_PUBLIC_CUPOS_DISPONIBLES=100` en Vercel | 🟡 | Contador correcto |

---

## Pendiente del cliente

| Pendiente | Urgencia | Bloquea |
|-----------|----------|---------|
| URL Mercado Pago suscripción $19.990/mes | 🔴 | Botón CTA modo venta (sin esto → "Disponible el 3 de mayo") |
| Testimonios reales (3-5, síntomas — NO peso) | 🟡 | Activados como BETA, reemplazar con reales antes del lanzamiento |
| Screenshots reales app: `/plan`, `/progreso`, `/recetario` (390px, frame iPhone) | 🟡 | ProductPreview (actualmente 3 SVGs placeholder) |
| Número WhatsApp Business | 🟢 | Botón flotante + footer |
| RUT + dirección legal | 🟢 | Footer legal |
| Analytics IDs: GA4 + Meta Pixel | 🟢 | Configurar en Vercel |

---

## Variables de entorno requeridas

| Variable | Estado |
|---|---|
| `NEXT_PUBLIC_LAUNCH_MODE` | Setear `=preregistro` hasta el 3-may → remover el 3-may 9 AM |
| `GHL_PREREG_WEBHOOK` | ⏳ Pendiente crear en GHL |
| `NEXT_PUBLIC_MP_URL` | ⏳ Pendiente Constanza |
| `NEXT_PUBLIC_CUPOS_DISPONIBLES` | Inicializar en `100` |
| `NEXT_PUBLIC_GA4_ID` | ⏳ Pendiente |
| `NEXT_PUBLIC_META_PIXEL_ID` | ⏳ Pendiente |

---

## Gotchas técnicos acumulados

- **Logo es una sandía, no una hoja**: El SVG vectorial inicial (hoja botánica) estaba conceptualmente equivocado. Se reemplazó por `navbar.png` oficial que tiene la sandía roja con semillas + texto azul.
- **Dark sections son azul navy, no negro puro**: Derivados del azul del texto del logo (`#0E2233`). Importante para coherencia de marca.
- **Montserrat, NO Playfair Display**: Las landings de referencia de Constanza usan sans-serif bold pesado. Playfair es demasiado editorial/serif para este sistema de marca.
- **Hero debe ser CLARO**: Las dos landings de referencia tienen hero con bg crema. La versión inicial dark era un desvío de marca.
- **SHOW_TESTIMONIALS**: Fue `false` (placeholders ocultos), ahora es `true` con badge "BETA" visible. Reemplazar con reales antes del lanzamiento.
- **Force push al repo**: El remoto `creactive-dev/nutrisco-landing` tenía una v1 anterior (2 commits). Se sobreescribió con force push intencionalmente.
- **Agentes paralelos y tipos TypeScript** (sesión anterior): Agentes subagentes usaron props en español (`titulo`, `icono`) en lugar de los definidos en TypeScript. Verificar siempre alineación con tipos antes de correr build.

---

## Próximo paso

1. **URGENTE — Deploy Vercel**: Conectar repo `creactive-dev/nutrisco-landing` → Vercel, root dir `./`, setear env vars
2. Confirmar dominio con Constanza
3. Pedir a Constanza: URL Mercado Pago + testimonios reales
4. El 3-mayo 9 AM: remover `NEXT_PUBLIC_LAUNCH_MODE` en Vercel → redeploy

---

## Historial de sesiones

| Fecha | Qué se hizo |
|-------|-------------|
| 2026-04-27 | Branding completo alineado con referencias Constanza. Navbar/foto/mockup reales. Montserrat. Hero claro. Pill system. PuenteReto rediseñado. Git init + force push a creactive-dev/nutrisco-landing. |
| 2026-04-25 | Build inicial desde cero: 60 archivos, 16 secciones, modo dual, 0 errores TS. Design system Modern Apothecary. |
