---
name: ContentOps — Estado del proyecto
description: SaaS de marketing operacional interno de CreActive. Estado del PRD, roadmap, y próximos pasos de ejecución.
type: project
originSessionId: de88d1fa-bb08-42d5-b564-0f451a8e1174
---
ContentOps es el sistema de marketing operacional de CreActive Studio. Stack: Next.js 16.2.4 + Tailwind CSS v4 + Supabase + n8n + Claude API. Dominio: ops.creactivestudio.agency.

**Why:** Centraliza todo el ciclo de contenido (ideación → generación → publicación → métricas → aprendizaje) que hoy se opera manualmente. Primero para uso interno (Operación 90 + marca personal Oscar), después SaaS multi-tenant.

**How to apply:** Al retomar ContentOps, el PRD v2.1 es el único source of truth. La app está deployada en Vercel. **Fase 1 completada** — próxima tarea: Fase 2 (LinkedIn OAuth + publicación).

---

## Estado actual (2026-04-17)

**✅ FASE 0 COMPLETADA.**

### Deploy
- URL producción: `https://app-ecru-three-91.vercel.app`
- Proyecto Vercel: `app` (renombrar a `contentops` en el dashboard)
- Dominio custom pendiente: `ops.creactivestudio.agency` (requiere acción manual de Oscar)

### Infraestructura
- **14 migraciones SQL** aplicadas en Supabase (`ymxdnvywznayxbmjzyhy`): 34 tablas, RLS completo, función `get_user_org_ids()`
- **Storage buckets:** `assets` y `generated-content` creados
- **Seed data** aplicado: org CreActive Studio + brand Oscar Vergara + 2 tracks + 10 topics
- **TypeScript types** generados en `app/src/types/database.ts`
- **Env vars** configuradas en Vercel: `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `NEXT_PUBLIC_APP_URL`

### Notas técnicas importantes
- Next.js 16 usa `proxy.ts` (no `middleware.ts`) con `export async function proxy()`
- shadcn/ui usa `@base-ui/react` (NO Radix UI) — `asChild` prop NO existe
- Repo local: `Proyectos Internos/contentops/` — el `app/` subdir NO tiene su propio `.git` (se borró para evitar gitlink)
- **⚠️ Gotcha auth.users manual:** Al insertar usuario manualmente en auth.users, se debe:
  1. Insertar también en `auth.identities` (provider='email', provider_id=email)
  2. Setear todos los token fields a `''` (string vacío), NO NULL: `confirmation_token`, `recovery_token`, `email_change_token_new`, `email_change`, `email_change_token_current`, `reauthentication_token`
  — GoTrue falla con "converting NULL to string is unsupported" si quedan en NULL

### Usuario de prueba creado
- Email: `hola@creactivestudio.agency`
- Password: `ContentOps2026!`
- UUID: `b2c3d4e5-f6a7-8901-bcde-f12345678901` (alineado entre auth.users y public.users)
- Estado: pendiente verificar que login funciona tras el fix de confirmation_token

## LinkedIn OAuth — Configurado (2026-04-26)

**App:** ContentOps en developer.linkedin.com
- Client ID: `777zochdabinom`
- Productos aprobados: Sign In with LinkedIn (OpenID Connect) ✅ + Share on LinkedIn ✅
- Redirect URI: `https://ops.creactivestudio.agency/oauth/linkedin/callback` ✅
- Credenciales en `.env.local` (raíz + app/) y pendiente en Vercel env vars
- **Community Management API:** requiere app separada (LinkedIn lo exige así). No es bloqueante para Fase 2 (posting en perfil personal). Relevante solo para posting en páginas de empresa.

## Pendiente de Oscar (acciones manuales)

| Tarea | Urgencia | Para qué |
|-------|----------|----------|
| ANTHROPIC_API_KEY en Vercel env vars | 🔴 Inmediato | Sin esto el generador no funciona en prod |
| LinkedIn creds en Vercel env vars | 🔴 Antes Fase 2 | `LINKEDIN_CLIENT_ID`, `LINKEDIN_CLIENT_SECRET`, `LINKEDIN_REDIRECT_URI` |
| Verificar login en `https://app-ecru-three-91.vercel.app/login` | 🔴 Pronto | Confirmar Fase 0 operacional |
| Agregar dominio en Vercel (Settings → Domains) → obtener CNAME value | 🟡 | Activar dominio custom |
| DNS: CNAME `ops` → valor que da Vercel | 🟡 | Después del paso anterior |
| Supabase Auth → URL redirect: `https://ops.creactivestudio.agency/auth/callback` + Site URL | 🟡 | Sin esto el OAuth no funciona con dominio custom |

## Próximo paso

**Fase 2 — LinkedIn e2e:** OAuth + publicación + scheduling + métricas.
LinkedIn app lista (Sign In + Share on LinkedIn). Bloqueante real: DNS + Supabase URL config + Vercel env vars.

## ✅ FASE 1 COMPLETADA (2026-04-17)

~45 archivos nuevos + 8 stubs reescritos. Build: 0 errores TS.

### Vistas funcionales
- **Strategy:** editor markdown voz/oferta/ICP, track manager con topics, competitor list, review indicator
- **Pipeline:** kanban 6 columnas con drag & drop nativo, idea form, idea cards
- **Calendar:** grilla mensual, drag & drop ideas/posts, sidebar distribución por track
- **Generator:** panel izquierdo (formato/topic/hook/briefing), Claude API (prompt caching), preview LinkedIn + IG carrusel, save/approve
- **Assets:** upload drag & drop, grid con filtros, detail panel
- **Dashboard:** métricas (posts real, pipeline), track distribution bar, trend placeholder Fase 2

### Deploy

- **Commit Fase 1:** `a411c50` — 68 archivos, 7017 inserciones
- **Deploy:** `npx vercel --prod` desde `app/` — sin GitHub, usa `.vercel/project.json` local
- **URL producción activa:** https://app-ecru-three-91.vercel.app
- **Nota deploy:** No hay remote git configurado. Deploy es 100% via Vercel CLI local.

### Notas técnicas Fase 1
- shadcn/ui base-ui: Tooltip = `TooltipProvider/Tooltip/TooltipTrigger/TooltipContent` (no namespace)
- Switch usa `checked`/`onCheckedChange`, Dialog usa `data-open`/`data-closed`
- `Linkedin` no existe en lucide-react — usar SVG custom
- `s` regex flag requiere target ES2018 (tsconfig es ES2017 — usar `[\s\S]`)
- `cache_control` en Anthropic SDK ahora está tipado (no necesita `@ts-expect-error`)
- Supabase strict insert types: usar `as any` para computed property keys e interfaces custom

## Historial de sesiones

| Fecha | Qué se hizo |
|-------|-------------|
| 2026-04-16 | Análisis exhaustivo PRD v2.0 → v2.1: 12 mejoras en 8 secciones. Schema SQL mejorado. Roadmap actualizado. |
| 2026-04-17 | Fase 0 completa: git init, 14 migraciones SQL, scaffold Next.js 16, 9 vistas stub, auth, sidebar, topbar, seed data, tipos TypeScript, deploy Vercel con env vars. |
| 2026-04-17 | Auth fix: env vars en Vercel, redeploy, usuario creado en auth.users+auth.identities, fix confirmation_token NULL→''. Login pendiente verificación. |
| 2026-04-17 | Fase 1 completa: ~45 archivos, todas las vistas funcionales (Strategy/Pipeline/Calendar/Generator/Assets/Dashboard). Build 0 errores TS. |
| 2026-04-17 | Commit `a411c50` (68 archivos, 7017 inserciones) + deploy a producción vía `npx vercel --prod`. URL activa: https://app-ecru-three-91.vercel.app |
