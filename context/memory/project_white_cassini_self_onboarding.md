---
name: White Cassini Self-Onboarding — Plan
description: Plan completo de implementación del flujo self-serve de signup para White Cassini / Kitchat — 3 fases, 8 pasos, MP trial 14d sin tarjeta, Google OAuth, preview de menú, QR celebración, Kapso embebido.
type: project
originSessionId: e07fc43b-c898-4aea-9574-8f8a737999ab
---
# White Cassini / Kitchat — Plan Self-Onboarding

## Estado actual (2026-04-21)

**Fase:** Planning completado. Pendiente de ejecución.

**Plan file:** `~/.claude/plans/para-white-casini-kitchat-vast-allen.md` — 12 secciones + archivos a tocar + verificación + 10 preguntas abiertas.

## Decisiones tomadas con Oscar

1. **Scope:** MVP completo de las 3 fases propuestas (no incremental).
2. **Billing:** Mercado Pago Chile. Planes Starter $29.990 / Pro $59.990. Trial 14 días **sin tarjeta** (DB-only, no toca MP hasta que paguen).
3. **Menu parser:** Mantener n8n externo, pero mover de `webhook-test` Railway a URL productiva versionada (`n8n.kitchat.cl/webhook/v1/menu-extraction` o Railway prod — decisión pendiente).
4. **Auth:** Email + password (con verificación por correo) + Google OAuth.
5. **Tenancy:** 1 user = 1 restaurante (NO refactor multi-sucursal ahora — queda para otra iteración).

## Arquitectura propuesta

### Nuevas migraciones SQL
- `20260420_billing_and_onboarding.sql` — tablas `planes`, `suscripciones`, `mp_eventos` + columnas nuevas en `restaurantes` (`onboarding_step` enum 11 valores, `paleta_id`, `wa_setup_mode`, etc).
- `20260420_storage_buckets.sql` — versiona `restaurant-assets` (hoy creado a mano).
- `20260420_refactor_onboarding_triggers.sql` — reemplaza trigger n8n (lee de Vault), agrega `sync_onboarding_legacy`, **DROP `on_auth_user_created`** (ahora lo hace edge function).
- `20260420_seed_legacy_tenants.sql` — Padrino + Soli Sushi con Pro cortesía 365d.

### Nuevas edge functions
- `signup-tenant` — orquesta auth user + restaurante + suscripción atómicamente.
- `mp-checkout-create` — crea MP Preapproval.
- `mp-webhook` — idempotencia via `mp_eventos.event_id UNIQUE`.
- `menu-parser-callback` — n8n callback con `X-Kitchat-Secret`.
- `menu-parser-retry` — reintento con JWT.

### Frontend admin-react
- Nuevas rutas públicas: `/signup`, `/signup/account`, `/verify-email`, `/auth/callback`, `/billing/*`.
- Refactor wizard: monolito 525 líneas → `OnboardingShell` + 8 steps + 5 componentes compartidos.
- Extraer `useKapsoSetup` hook de SettingsPage.jsx:205-237 para reutilizar en Step 8.
- Banner `WhatsAppPendingBanner` en AppShell cuando `wa_setup_mode='deferred'`.
- `useAuth`: agregar `signUp`, `signInWithOAuth('google')`, `resetPassword`.
- Reemplazar gate de App.jsx con `resolveOnboardingRoute(settings, subscription)`.
- Librerías a instalar: `node-vibrant` (color dominante de logo), `qrcode.react` (QR Step 7).

## Plan de ejecución (2 sprints)

### Sprint 1 (~1 semana) — lanzable sin MP
Fases A (DB) + B parcial (`signup-tenant`, parser callbacks) + C (frontend público) + D (refactor wizard) + E (n8n productivo) + G (Google OAuth config). Deploy con toggle "solo trial" ocultando cards pagadas.

### Sprint 2 (~1 semana) — habilitar MP
`mp-checkout-create` + `mp-webhook` + páginas `/billing/*` + cron trial expiration. Testing MP sandbox. Activar cards Starter/Pro.

## Inventario hecho en esta sesión

2 Explore agents en paralelo generaron inventario completo:
- **Signup público:** NO EXISTE. Todo manual vía Admin API.
- **Onboarding actual:** 4 pasos en `OnboardingPage.jsx` (525 líneas). Gate en `App.jsx:38-45`.
- **Trigger DB `handle_new_user_restaurante`:** schema_base.sql:221-234. El trigger `on_auth_user_created` NO está versionado (se aplicó a mano vía Dashboard).
- **Trigger n8n:** schema_base.sql:259-281 — URL `webhook-test` de Railway hardcodeada.
- **Kapso:** `kapso-setup` + `kapso-webhook` edge functions OK. UI en SettingsPage, no en wizard.
- **Schema tenant:** tabla única `restaurantes` con FK `user_id → auth.users` (1:1 forzado). `onboarding_status` enum de solo 3 valores.
- **Tipos TS:** `database.types.ts` manual (no generado). Faltan `zonas_delivery`, `pedido_review_turns`.
- **Bucket `restaurant-assets`:** sin migración versionada (riesgo).
- **Cero:** billing (Stripe/MP/planes/suscripciones), preview menú, paletas, QR, edición branding en Settings, edge function parser propia, banner "activa WA".

## Preguntas abiertas (pendientes de confirmar antes de implementar)

1. Colores exactos de las 5 paletas predefinidas (propuesta inicial en plan).
2. Copy mensajes rotativos Step 5.
3. Copy banner "Activa WhatsApp".
4. n8n: subdominio propio `n8n.kitchat.cl` o Railway productivo.
5. Plan legacy Padrino/Soli Sushi — Pro cortesía 1 año (propuesto) o trialing.
6. Plan "paid" sin trial — cobro día 1 o 14 días gratis con tarjeta capturada.
7. Slug editable solo en wizard o también en Settings.
8. Duración trial: desde creación (asumido) o desde `wa_connected`.
9. QR: PNG simple o PDF con branding imprimible.
10. Límite 5 imágenes Step 4 — validar client-side.

## Próximo paso exacto

Al retomar: revisar las 10 preguntas abiertas con Oscar → empezar Sprint 1 por Fase A (migraciones SQL). Orden recomendado:
1. `20260420_billing_and_onboarding.sql` + `20260420_storage_buckets.sql` en branch feature.
2. Validar con `supabase db push --dry-run` antes de aplicar.
3. `20260420_seed_legacy_tenants.sql` después de verificar regresión Padrino/Soli Sushi.
4. `20260420_refactor_onboarding_triggers.sql` solo cuando edge function `signup-tenant` esté lista (orden crítico — este SQL rompe el trigger actual de auto-creación).

## Gotchas importantes

- **El trigger `on_auth_user_created` NO está en SQL versionado** (CLAUDE.md §11). Al aplicar `DROP TRIGGER`, validar primero que existe en DB real.
- **MP Preapproval Chile ejecuta primer cobro inmediato.** Por eso trial sin tarjeta = solo DB, nunca toca MP.
- **El `external_reference` para MP** se prefija con `pendsub:{uuid}` para distinguir primer cobro de signup de cobros recurrentes.
- **Reutilizar Kapso existente:** cero cambios en edge functions `kapso-setup`/`kapso-webhook`. Solo extraer hook y embeber UI.
- **Eliminar `localStorage.wc_onboarding`:** fuente de verdad pasa a ser `restaurantes.onboarding_step` granular.
- **`onboarding_status` legacy se conserva** y se sincroniza vía trigger `sync_onboarding_legacy` para no romper código existente.
- **Bucket `restaurant-assets`:** hoy sin migración — versionarlo es prerrequisito para rehidratar proyecto en otro environment.
