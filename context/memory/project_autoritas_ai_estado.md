---
name: Proyecto Autoritas AI / ARENA — landing + consultoría
description: Estado del flujo PRO + landing Next.js + presentación de consultoría para ARENA (peer/colaboración con Héctor Partida, Madrid). Pendiente deploy Vercel + envío a Héctor.
type: project
originSessionId: e077a60f-5ea2-40f4-9593-1942325247de
---
Flujo PRO completo ejecutado el 2026-04-17. Presentación de consultoría generada 2026-04-17.

**What:** Landing Next.js 14 + Tailwind + Framer Motion + presentación de consultoría (12 slides Reveal.js, dark theme CreActive) para ARENA (Autoritas AI). Propuesta de referencia para Héctor Partida Bazo (Madrid) como cumplimiento del compromiso de Oscar de dar feedback comercial esta semana.

**Why:** Oscar ofreció feedback comercial en la reunión inicial del 17-04-2026. La landing existente vendía "testing técnico" — la propuesta reencuadra el mensaje a "protección de negocio": Margin Leak, Alucinación de Políticas, Over-Explaining, EU AI Act.

**How to apply:** Al continuar, leer `clientes/autoritas-ai/estado.md` y los proyectos en `outputs/autoritas-ai-landing/` y `outputs/presentacion-consultoria-2026-04-20.html`. El dev server se levanta con `npm run dev` desde la carpeta de la landing.

## Estado (2026-04-17 — sesión 3)

- [x] Fix centrado vertical en deck de consultoría — `display:flex; justify-content:center` en `.reveal .slides > section`
- [ ] Deploy Vercel (pendiente) → fecha objetivo 2026-04-20
- [ ] LinkedIn DM a Héctor con preview URL landing + deck presentación (pendiente)

### Gotcha Reveal.js centrado
`center: false` en `Reveal.initialize()` controla la posición del contenedor de slides dentro del viewport (arriba vs centrado), NO el centrado vertical del contenido dentro de cada `<section>`. Para centrar contenido internamente: `display:flex; flex-direction:column; justify-content:center` en la sección vía CSS.

## Estado (2026-04-17 — sesión 2)

- [x] PRD → `clientes/autoritas-ai/prd-landing-v1.md`
- [x] Estructura → `clientes/autoritas-ai/estructura-landing-v1.md`
- [x] Plan → `clientes/autoritas-ai/plan-trabajo-landing-v1.md`
- [x] Build Next.js → `clientes/autoritas-ai/outputs/autoritas-ai-landing/` — ✅ 0 errores TS. Dev server ✅
- [x] Presentación de consultoría → `clientes/autoritas-ai/outputs/presentacion-consultoria-2026-04-20.html` — 12 slides Reveal.js, dark theme CreActive
- [ ] Deploy Vercel (pendiente) → fecha objetivo 2026-04-20
- [ ] LinkedIn DM a Héctor con preview URL landing + deck presentación (pendiente)

## Contenido de la presentación de consultoría

12 slides cubriendo las 4 promesas de la reunión:
1. Portada CreActive × Autoritas AI
2. Agenda — 4 compromisos → 4 entregables
3. Marco: 4 riesgos de negocio (Margin Leak / Alucinación / Over-Explaining / EU AI Act)
4. Entregable #1 — Landing antes/después del copy + estado "Live en local"
5. Auditoría LinkedIn — diagnóstico 3 marcas (Autoritas/ARENA/Eon32) diluyen posicionamiento
6. Headline propuesto (antes/después — listo para copiar)
7. Extracto propuesto (antes/después — listo para copiar)
8. Sección Experiencia — consolidación recomendada + CTA Featured
9. Estrategia contenido LinkedIn 30 días — 3 pilares + primer post listo
10. GTM: Caballo de Troya (cold email) + Certificación ARENA para agencias
11. Feature "Cliente Incógnito Externo" + sinergia Kitcha/Nutrisco
12. Recursos (Vexa AI, estructura Claude Code) + siguientes pasos con fechas

## Gotchas técnicos de la sesión de landing (sesión 1)

- `next.config.ts` no soportado en Next.js 14.2.29 — usar `next.config.mjs`
- El skill `pro-build-landing` tiene regla "no Inter" — ignorar cuando el cliente ya decidió Inter
- Inconsistencia de rutas entre skills: `pro-estructura-landing` guarda en `clientes/{slug}/` pero `pro-build-landing` busca en `clientes/{slug}/outputs/` — copiar manualmente con `cp`

## Gotchas estratégicos nuevos (sesión 2 — perfil LinkedIn)

- La descripción de Autoritas AI en LinkedIn es voice-first para despachos legales — completamente desconectada de ARENA. No estaba documentado en CLAUDE.md del cliente. Esto confunde a cualquier prospecto de ARENA.
- LinkedIn handle confirmado: `hectorpartidabazo` (resolvía duda del TODO en el código de la landing)
- Héctor tiene 3 marcas activas (Autoritas/ARENA/Eon32) + trabaja en Volvo como recambista — solopreneur a tiempo parcial, no full-time en ARENA todavía

## Assets pendientes de Héctor (TODO en el código de la landing)
- Logo oficial ARENA SVG/PNG
- Screenshot real del ARENA Score output
- URL deeplink al free tier (por ahora CTAs van a root autoritas.ai)
- Precio "Pack de 10 tests" (cuarto tier pricing)

## Relación
Peer/colaboración — no cliente pagante. Posible evolución: referidos ARENA para clientes de CreActive que implementen agentes.
