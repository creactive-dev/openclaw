# Estado — Constanza Nutrición
**Slug:** `constanza-nutricion`
**Última actualización:** 2026-04-25

## Estado actual
Landing Fundadores completada en código (2026-04-25): 60 archivos, build 0 errores TS, 16 secciones, modo dual pre-registro/venta. **Pendiente crítico: 5 env vars + deploy Vercel + assets Constanza + DNS — todo antes del 3-mayo (lanzamiento).** Módulo Comunidad diseñado (spec + plan), pendiente aprobación para ejecutar.

## Completado
- ✅ Fase 1: Web + landing ebook + Meta Ads (ROI 421%, 290 clientes, $5.2M CLP)
- ✅ App SaaS Nutrisco MVP al 90% (26 rutas, IA, pagos, crons, dashboard nutricionista)
- ✅ Servicio Primera Clase fases 1-3: voz.ts, Resend emails, notificaciones, alertas, paywall
- ✅ Landing page Nutrisco inicial (2026-04-03): 11 secciones, Modern Apothecary, código base
- ✅ Landing page upgrade completo (2026-04-17): ver detalle en project_nutrisco_estado.md
- ✅ Módulo Comunidad — diseño (2026-04-18): spec + plan de implementación completos. Reemplaza grupo WhatsApp. Feed unificado con tabs (Todos/Logros/Recetas/Dudas), replies 1 nivel, 5 reacciones emoji, imágenes, alias privados, Supabase Realtime, Web Push PWA. Documento: `outputs/nutrisco-app/docs/superpowers/specs/2026-04-18-comunidad-design.md` + plan `~/.claude/plans/hidden-sauteeing-music.md`.
- ✅ **Landing Fundadores (2026-04-25):** 60 archivos desde cero, build 0 errores TS. 16 secciones: BarraUrgencia, Hero (parallax), BarraConfianza, Problema, PuenteReto, QueEsNutrisco, ComoFunciona, ProductPreview, QueIncluye, SobreConstanza, Testimonios, Pricing, Garantia, FAQ, CTAFinal, Footer. Modo dual pre-registro/venta con switch automático por fecha. Form custom → webhook GHL. BloqueIsapre. BannerCookies con gating GA+Pixel. Design system Modern Apothecary. Ruta: `outputs/landing-fundadores/`.

## Pendiente de CreActive
| Tarea | Urgencia | Para qué |
|-------|----------|----------|
| Deploy landing-fundadores a Vercel (root dir: `landing-fundadores/`) | 🔴 | Landing live — lanzamiento 3 mayo |
| Setear env vars en Vercel: `NEXT_PUBLIC_LAUNCH_MODE=preregistro`, `NEXT_PUBLIC_CUPOS_DISPONIBLES=100` | 🔴 | Modo pre-registro correcto desde el inicio |
| Confirmar dominio (nutrisco.cl / fundadores.constanzanutricion.cl / subruta) + DNS | 🔴 | Apuntar antes del 3-mayo |
| El 3-mayo 9 AM: remover `NEXT_PUBLIC_LAUNCH_MODE` en Vercel → redeploy | 🔴 | Activar modo venta automático |
| Crear webhook GHL + tag `pre-registro-fundadores` → setear `GHL_PREREG_WEBHOOK` | 🔴 | Form pre-registro funciona |
| Configurar MP_WEBHOOK_SECRET en Vercel (app SaaS) | 🔴 | Pagos SaaS funcionando |
| DNS beta: CNAME app.constanzanutricion.cl → Vercel | 🔴 | Beta URL app |
| Verificar dominio Resend (constanzanutricion.cl) | 🔴 | Emails transaccionales |
| Ejecutar plan Módulo Comunidad (~9.5 días) | 🟡 | Reemplazar grupo WhatsApp por comunidad interna. Requiere aprobación previa de Oscar. |

## Pendiente del cliente
| Pendiente | Urgencia | Bloquea |
|-----------|----------|---------|
| URL Mercado Pago suscripción $19.990/mes | 🔴 | Botón CTA modo venta landing fundadores |
| Foto profesional de Constanza | 🔴 | SobreConstanza — placeholder activo (`public/constanza-placeholder.svg`) |
| Screenshots reales app: `/plan`, `/progreso`, `/recetario` (390px, frame shots.so) | 🔴 | ProductPreview — 3 SVGs placeholder |
| Testimonios reales (3-5, síntomas — NO peso) | 🔴 | Testimonios ocultos (`SHOW_TESTIMONIALS=false`) |
| Número WhatsApp Business | 🟡 | Botón flotante + footer landing fundadores |
| RUT + dirección legal | 🟡 | Footer legal landing fundadores |
| Analytics IDs: GA4 + Meta Pixel | 🟡 | Configurar en Vercel antes de activar analytics |
| Link grupo WhatsApp beta | 🟡 | /procesando en la app SaaS |
| Grabación activo bienvenida /procesando | 🟡 | Asset visual /procesando app |

## Próximo hito
1. **HOY (25-abril):** Deploy landing-fundadores en Vercel + crear webhook GHL + setear env vars → landing en pre-registro live.
2. Pedir a Constanza: URL Mercado Pago, foto, screenshots app, testimonios reales.
3. **3-mayo 9 AM:** Remover `NEXT_PUBLIC_LAUNCH_MODE` en Vercel → redeploy → activa modo venta.
4. Aprobación del plan Módulo Comunidad por Oscar (plan en `~/.claude/plans/hidden-sauteeing-music.md`) → ejecutar Fase 0.

## Historial de sesiones
| Fecha | Qué se hizo |
|-------|-------------|
| 2026-04-25 | Landing Fundadores: 60 archivos desde cero en `outputs/landing-fundadores/`, build 0 errores TS, 16 secciones, modo dual pre-registro/venta, Modern Apothecary, form GHL custom, BloqueIsapre, BannerCookies con gating analytics. Listo para deploy. |
| 2026-04-24 | Nutrisco SaaS: UX comunidad chat-style (tabs sticky, mensajes abajo, InputBar delgada). PR #1 V3 abierto. |
| 2026-04-18 | Módulo Comunidad: brainstorming completo + design spec aprobado + plan de implementación detallado (~9.5 días, incluye Web Push PWA). 3 mockups visuales. Exploración codebase para fiabilidad. Pendiente aprobación del plan. |
| 2026-04-17 | Upgrade landing page vendedora: mobile menu, StickyCTA, Button unificado, social proof, font fix, legal pages, Meta Pixel. TypeScript 0 errores. |
| 2026-04-15 | QA app SaaS: /procesando corregido, PWA instructions, nombre dinámico, emoji 🍉, cron delays |
| 2026-04-14 | Servicio Primera Clase Fases 1-3: voz.ts, Resend, notificaciones, alertas, paywall |
| 2026-04-03 | Landing inicial: PRD + estructura + código base 11 secciones |
