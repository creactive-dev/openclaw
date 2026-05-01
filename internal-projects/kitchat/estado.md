# Estado — Kitchat Landing Page
**Slug:** `kitcha`
**Proyecto:** Landing de venta de Kitchat (SaaS restaurantes / White Cassini)
**Última actualización:** 2026-04-20

## Estado actual

Visual v2 en GitHub. repo `creactive-dev/kitchat` (commit 6112648). Landing con 3 mockups CSS reales, 5 secciones reescritas, 152kB, 0 errores TS. Pendiente: deploy Vercel + QA visual completo → compartir con Oscar.

## Completado

- ✅ Brief estratégico (`docs/kitchat-landing-brief.md`) — previo a esta sesión
- ✅ GTM report v1.0 (`docs/kitchat-gtm-report.md`) — previo a esta sesión
- ✅ PRD v1.0 (`clientes/kitcha/prd-landing-v1.md`) — 2026-04-20
- ✅ Estructura v1.0 (`clientes/kitcha/estructura-landing-v1.md`) — 2026-04-20
- ✅ Notas de estrategia (`clientes/kitcha/notas-estrategia.md`) — 2026-04-20
- ✅ Plan de trabajo v1.0 (`clientes/kitcha/plan-trabajo-landing-v1.md`) — 2026-04-20
- ✅ Build completo Next.js (`clientes/kitcha/outputs/kitcha-landing/`) — 2026-04-20 — 24 archivos, 0 errores TS, build limpio
- ✅ Visual v2 (`clientes/kitcha/outputs/kitcha-landing/`) — 2026-04-20 — 3 mockups CSS reales + 5 secciones reescritas, 152kB, 0 errores TS

## Pendiente de CreActive

| Tarea | Urgencia | Para qué |
|-------|----------|----------|
| QA visual completo en mobile (375px) + desktop | 🔴 | Gate A antes de compartir con Oscar |
| ~~Mockup hero~~ | ✅ | Hero con DashboardMockup + ElPadrinoPhoneMockup CSS fieles al producto real |
| ~~Problem section visceral~~ | ✅ | WhatsApp chaos + contadores de pérdida rojos animados |
| ~~HowItWorks impactante~~ | ✅ | Zig-zag + números gigantes outline + mini-mockups + línea verde animada |
| ~~Features bento~~ | ✅ | WhatsApp 2×2 estrella + phone 2×1 + 4 cards con mini-visuales |
| ~~NoCommissions calculadora~~ | ✅ | Slider interactivo + bar chart "de cada $100" |
| Crear OG image 1200x630px | 🟡 | Agregar en `/public/og-image.jpg` y descomentar en `layout.tsx` |
| Actualizar CLAUDE.md raíz: "Kitcha" → "Kitchat" + precios reales | 🟡 | Consistencia de datos de la agencia |

## Pendiente del cliente (Oscar — en rol de dueño del producto)

| Pendiente | Urgencia | Bloquea |
|-----------|----------|---------|
| URL de destino de "Probar 7 días gratis" | 🔴 | CTA principal — flujo self-serve no implementado. CTA actual = `href="#"`. Reemplazar con URL real en `lib/constants.ts` cuando esté listo. |
| Número de WhatsApp de Kitchat para ventas | 🔴 | Reemplazar `56XXXXXXXXX` en `lib/constants.ts` → botones "Hablar con ventas" y footer |
| Logo Kitchat SVG/PNG | 🟡 | Navbar y footer usan logo texto placeholder — agregar imagen cuando llegue |
| ~~Mecanismo "Hablar con ventas"~~ | ✅ | **WhatsApp directo** — implementado en `LINKS.waSales` |
| ~~Confirmar dominio kitchat.cl~~ | ✅ | **kitchat.cl confirmado** — verificar DNS → Vercel antes del deploy |
| Testimonio real de El Padrino | 🟡 | `SocialProof.tsx` — copy de fallback ya en código, reemplazar cuando llegue |
| Permiso formal de Soli Sushi (logo) | 🟢 | `SocialProof.tsx` — diseñado para funcionar sin logo |
| Copy del FAQ (validar 8 preguntas sugeridas) | 🟡 | `lib/constants.ts` — las 8 preguntas están escritas, Oscar confirma si son las correctas |
| Capturas reales del producto (scrubbed) | 🟡 | Mockups CSS en Hero, S3, S4 — reemplazar con capturas reales cuando lleguen |
| Decisión analytics (GA4 / Plausible) | 🟢 | Agregar script en `layout.tsx` cuando se decida |

## Próximo hito

**Gate A (CreActive)** — QA visual completo: `npm run dev` → revisar 10 secciones en mobile + desktop → confirmar que todo se ve bien.

**Gate B (Oscar)** — Compartir URL staging con Oscar para feedback visual antes del deploy.

## Propuesta comercial estándar (WhatsApp)

**Ruta:** `plantillas/propuesta-kitcha/template.html`
**Estado:** ✅ Completa — lista para usar
**Variables:** `{{NOMBRE_RESTAURANTE}}` + `{{FECHA}}` (solo 2)
**Oferta principal:** Plan anual = implementación gratis + 2 meses gratis
**Demo link en la propuesta:** `mcdonald-s-antofagasta-playa.kitchat.cl`
**Pendiente antes de usar en campo:**
- QA visual: abrir en Chrome → Cmd+P → verificar que las 2 páginas se ven bien sin cortes
- Reemplazar `Escribir por WhatsApp →` con número real de Oscar en el CTA
- Confirmar precio anual Pro: ¿$449.004 (landing) o $499.000? Fuente de verdad: `lib/constants.ts`

## Historial de sesiones

| Fecha | Qué se hizo |
|-------|-------------|
| 2026-04-20 | Primera sesión: PRD v1.0 + Estructura v1.0 + Notas estrategia generados. Trial corregido a 7 días. Carpeta clientes/kitcha/ creada. |
| 2026-04-20 | Segunda sesión: Plan de trabajo v1.0 generado (9 fases, 22 abril → 9 mayo). Bloqueante URL trial desescalado con propuesta Tally form. Gate A identificado como acción urgente. |
| 2026-04-20 | Tercera sesión (build): Landing Next.js completa generada. 24 archivos, 0 errores TS, 142kB. CTA trial = href="#". |
| 2026-04-20 | Cuarta sesión (visual v2): Problem reescrita con WhatsApp chaos visceral. Hero, HowItWorks, Features, ReviewsAI, NoCommissions reescritas. 3 mockups CSS reales del producto. 152kB, 0 errores TS. |
| 2026-04-20 | Quinta sesión (git): Commit y push a creactive-dev/kitchat (commit 6112648). 30 archivos. Merge --allow-unrelated-histories con README.md del remote. Repo listo para deploy en Vercel. |
| 2026-04-23 | Propuesta comercial estándar WhatsApp: template HTML 2 págs light theme, branding Kitchat, stats reales del landing, 3 pasos onboarding, 3 cards planes estilo landing, banner implementación gratis. |
| 2026-04-23 | Propuesta v2: imágenes portada → computador.png + celular.png con overlap (margin-right -80px). Eliminado todo lo de CreActive. Sin prueba gratuita. CTA → "Empezar a recibir pedidos". Mobile responsive completo (@media screen 768px). |
