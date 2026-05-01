# Memory Index — CreActive Studio

## Proyecto: CreActive Studio Web (web propia de la agencia)
- [project_creactive_web_estado.md](project_creactive_web_estado.md) — Landing Next.js (2026-04-27). 10 commits. Favicon ✅, logos svgl corregidos (Claude+Next.js), Rivas Legal removido de sectores. Copy: operación>marketing, tuteo LATAM, humanizado. Pendiente: dominio, OG image, QA GHL iframe.

## Proyecto: Ph Labs landing
- [project_phlabs_landing_estado.md](project_phlabs_landing_estado.md) — Favicon ✅ commit `7e9377e` (2026-04-30). Correos Flujo B redactados (físico + digital → mismo doc "Presentación PHL"). **Bloqueante: Gastón entrega el doc → Oscar configura GHL.** 7 logos F&F en slider.

## Proyecto: FWC Ellinger landing
- [project_fwc_landing_estado.md](project_fwc_landing_estado.md) — Landing completada (2026-03-29). Build Next.js, feedback ronda 1 de Sebastián aplicado, repo en GitHub. Pendiente deploy Vercel + dominio .CL.

## Proyecto: Kitchat Landing Page (landing de venta del SaaS)
- [project_kitchat_landing_estado.md](project_kitchat_landing_estado.md) — Env vars Vercel corregidas ✅ (s17 2026-04-28): SUPABASE_URL sin trailing newline, anon key rotada actualizada. Polling /gracias funciona. **Pendiente: 56XXXXXXXXX + webhook global MP Dashboard.**
- [project_kitcha_propuesta_template.md](project_kitcha_propuesta_template.md) — Template propuesta comercial WhatsApp ✅ v2 (2026-04-23): `plantillas/propuesta-kitcha/template.html`. 2 págs, light, 100% Kitchat (sin CreActive), imágenes overlap (celular + laptop), mobile responsive, CTA "Empezar a recibir pedidos". Pendiente: QA Chrome PDF + ajustar overlap (-80px) + número WA.

## Proyecto: White Cassini / Kitchat (SaaS restaurantes)
- [project_white_cassini_estado.md](project_white_cassini_estado.md) — Messaging audit ✅ commit `76e35f3` (2026-05-01): welcome dedup 24h, toggle transferencia en Mensajes Automáticos, prefix "Acá debes transferir", encuesta bloqueada sin google_review_url. **Pendiente: Oscar configura bank_instructions + google_review_url + QA flujo + webhook MP.**
- [project_white_cassini_self_onboarding.md](project_white_cassini_self_onboarding.md) — 📋 PLAN COMPLETADO (2026-04-21): self-onboarding 3 fases/8 pasos con MP trial 14d sin tarjeta + Google OAuth + preview menú + QR. Plan: `~/.claude/plans/para-white-casini-kitchat-vast-allen.md`. Próximo: validar 10 preguntas abiertas → Sprint 1 (Fase A migraciones SQL).
- [project_white_cassini_bsuid_migration.md](project_white_cassini_bsuid_migration.md) — ⏳ TAREA SEMANA 2026-04-20: migración BSUIDs Kapso. Meta ya rollando BSUIDs en webhooks — phone_number puede llegar null. Checklist 8 items: schema nullable, nuevos campos, matching BSUID-first, parsers, identity events.
- [project_white_cassini_demo_mcdonalds.md](project_white_cassini_demo_mcdonalds.md) — 📋 PLAN DOCUMENTADO (2026-04-23) — demo McDonald's: login demo@kitchat.cl + fixtures WhatsApp + seed pedidos + flag `demo_mode`. Roadmap, sin ejecutar.
- [handoff_white_cassini_2026-04-13.md](handoff_white_cassini_2026-04-13.md) — Handoff sprint 5 (2026-04-13): QA checklist + merge + roadmap Fase 2.
- [project_white_cassini_chat_conversations_limit.md](project_white_cassini_chat_conversations_limit.md) — ✅ COMPLETADO (2026-04-15). per_page=100 deploado.

## Preferencias de herramientas
- [feedback_worktree_setup.md](feedback_worktree_setup.md) — Worktrees: siempre `.worktrees/` local al proyecto, no ubicación global.

## Proyecto: Pumpalcerro — campaña Meta Ads + email marketing
- [project_pumpalcerro_estado.md](project_pumpalcerro_estado.md) — Meta Ads lanzado (2026-04-15). Email masivo Conguillío v3 listo (2026-04-21). Email promocional Valle del Elqui creado en base a la landing (2026-04-29). Pendientes: Michi dispara correos y sube imagen hero a CDN. Reporte ads.

## Empresa: Constitución legal
- [project_empresa_constitucion.md](project_empresa_constitucion.md) — CREACTIVE STUDIO SPA, RUT 78.387.691-4, constituida 01-04-2026 en Antofagasta. Pro Pyme Transparente. Trámites: SII verificación ⏳, Global66 ⏳.

## Prospecto: Pizzas Pelikan Express (venta de negocio)
- [project_pelikan_express_estado.md](project_pelikan_express_estado.md) — Propuesta HTML A4 v1 lista (2026-04-23): logo Pelikan portada, 5 páginas, Fase 2 = 6–8 semanas, correo envío redactado. Pendiente: exportar PDF → enviar a Jessica → confirmar propuesta → Fase 1 Diagnóstico Copiapó.

## Proyecto: Easyway Chile (prospecto — landing page)
- [project_easywaychile_estado.md](project_easywaychile_estado.md) — Flujo PRO al 60% (2026-04-16). CLAUDE.md + PRD + Estructura completados. Color #ff3131, precio $280K, fecha 30 abril. Pendiente: respuestas de Claudia → `/pro-plan-trabajo`.

## Workflow de sesiones
- Usar `/cierre-sesion` cuando el contexto llega a ~60–70%: detecta tipo de sesión (🔧/🤝/🔀) y actualiza los documentos correspondientes sin generar handoffs.

## Agency OS — Skills internas y herramientas
- [project_agency_os_skills.md](project_agency_os_skills.md) — 2 scrapers (PedidosYa + Uber Eats). Skill `/kitcha-import-pedidosya` acepta URL directa → scraper automático → demo Kitcha en 2 min. 21 comandos slash activos.
- [feedback_cierre_sesion.md](feedback_cierre_sesion.md) — No generar handoffs en `/cierre-sesion` — solo actualizar documentos (ahorra tokens).
- [project_pedidosya_scraper.md](project_pedidosya_scraper.md) — Scraper PedidosYa + Uber Eats ✅ (2026-04-22). Flujo: `/kitcha-import-pedidosya <url>` → scraper correcto → SQL → Supabase. Gotcha horarios: usar `horarios_semana = NULL` siempre en demos.

## Proyecto: Autoritas AI / ARENA (peer — landing + consultoría)
- [project_autoritas_ai_estado.md](project_autoritas_ai_estado.md) — Landing Next.js ✅ + deck consultoría 12 slides ✅ + fix centrado vertical ✅ (2026-04-17). Deck listo para presentar. Pendiente: deploy Vercel + LinkedIn DM antes del 20-04.

## Proyecto: ContentOps (SaaS marketing operacional — interno)
- [project_contentops_estado.md](project_contentops_estado.md) — Fases 0+1 ✅ (2026-04-17). LinkedIn OAuth configurado (Client ID 777zochdabinom, Sign In + Share). Bloqueantes Fase 2: Vercel env vars (ANTHROPIC_API_KEY + LinkedIn creds) + DNS + Supabase URL config. Community Management API no bloqueante para Fase 2. Código Fase 2 no arrancado.

## Proyecto: Nutrisco (SaaS nutrición — Constanza Nutrición)
- [project_nutrisco_estado.md](project_nutrisco_estado.md) — DSv3 F1+F2+F3 ✅ main. F4.1 dashboard: código listo (3 archivos) pero **commit pendiente** (git reset --soft e1caab5 ejecutado, re-commitear al inicio de próxima sesión). Próximo: git add 3 archivos → commit → build → QA /scraps/ds-preview → Fase 4.2 checkin.
- [project_nutrisco_servicio_primera_clase.md](project_nutrisco_servicio_primera_clase.md) — **COMPLETADO EN CÓDIGO.** Servicio primera clase full en main. Pendiente solo configuración externa + QA.
- `Nutrisco/docs/estado-actual.md` — Documento fundacional (2026-04-17): inventario completo features paciente + nutricionista + journey end-to-end + 12 gaps objetivos. Baseline para sesión de mejoras al journey.
- [project_nutrisco_landing_fundadores.md](project_nutrisco_landing_fundadores.md) — Landing Fundadores ✅ branding alineado + en GitHub (2026-04-27): Montserrat, Hero claro, navbar/foto/mockup reales, Pill system, PuenteReto rediseñado. Repo: `creactive-dev/nutrisco-landing`. **Próximo: deploy Vercel + env vars + URL MP de Constanza.**
