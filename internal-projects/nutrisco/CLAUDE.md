# Nutrisco — Contexto Global del Proyecto
**Versión:** 0.2.0
**Última actualización:** Abril 2026
**Agencia:** CreActive Studio (Oscar Vergara Barros)  
**Cliente:** Constanza Nutrición

---

## Qué es este proyecto

Nutrisco es una plataforma SaaS de nutrición antiinflamatoria. Permite a la nutricionista Constanza gestionar pacientes de forma automatizada: asigna planes alimentarios personalizados mediante IA, hace seguimiento quincenal, y ofrece soporte 24/7 vía agente conversacional basado en Claude API.

**No es una app genérica de nutrición.** Trabaja exclusivamente con el catálogo de pautas pre-diseñadas de Constanza. La IA selecciona, no genera.

---

## Stack

| Capa | Tecnología |
|------|-----------|
| Frontend | Next.js 14 (App Router) + Tailwind CSS + TypeScript |
| Backend / DB | Supabase (PostgreSQL + Auth + Storage + RLS) |
| IA | Claude API (Anthropic) — Sonnet 4.6 (asignación pauta, ajuste quincenal) + Haiku 4.5 (soporte chat) |
| Pagos | Mercado Pago (suscripciones recurrentes en CLP) |
| CRM / Automatizaciones | GoHighLevel (GHL) |
| Email transaccional | Resend |
| Hosting | Vercel |
| Boletas | VSale (integración externa) |

---

## Estructura del proyecto

```
nutrisco/
├── CLAUDE.md                  ← este archivo
├── app/                       ← rutas y componentes Next.js
│   └── CLAUDE.md
├── supabase/                  ← schema, migraciones, seeds
│   └── CLAUDE.md
├── lib/                       ← utilidades, clientes, helpers
│   └── CLAUDE.md
├── docs/                      ← documentación viva
│   ├── decisiones.md
│   ├── schema.md
│   └── progreso.md
├── .env.local                 ← variables de entorno (no commitear)
└── package.json
```

---

## Variables de entorno requeridas

```bash
# Supabase
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

# Claude API
ANTHROPIC_API_KEY=

# Mercado Pago
MP_ACCESS_TOKEN=
MP_WEBHOOK_SECRET=

# Resend
RESEND_API_KEY=

# App
NEXT_PUBLIC_APP_URL=
```

---

## Usuarios del sistema

| Rol | Descripción | Acceso |
|-----|-------------|--------|
| `paciente` | Usuario final suscrito | Solo sus propios datos |
| `nutricionista` | Constanza — opera el dashboard | Todos los pacientes |
| `admin` | CreActive — mantenimiento técnico | Acceso total |

---

## Decisiones de producto importantes

- **La IA no genera planes desde cero** — solo selecciona del catálogo de pautas de Constanza
- **Delay de 24h en entrega del plan** — simula revisión humana para percepción de personalización
- **Mobile-first obligatorio** — 90% del tráfico esperado es móvil (375px+)
- **Sin memoria persistente en el agente de soporte** — contexto por pauta, no por historial personal
- **Comunidad en WhatsApp para MVP** — la integración nativa va en v2
- **Pagos exclusivamente en CLP** vía Mercado Pago

---

## Reglas de desarrollo

1. **TypeScript estricto** — no usar `any`, tipar todo explícitamente
2. **App Router de Next.js 14** — no usar Pages Router
3. **Server Components por defecto** — usar Client Components solo cuando sea necesario
4. **RLS siempre activo** — ninguna tabla sin Row Level Security
5. **Variables de entorno** — nunca hardcodear credenciales
6. **Mobile-first** — diseñar desde 375px hacia arriba

---

## Patrones críticos del codebase

### RLS
- `FOR ALL USING (...)` **no cubre INSERT** — siempre agregar `WITH CHECK (auth.uid() = user_id)` en policies con INSERT
- Función `public.current_user_role()` SECURITY DEFINER — nunca poner `SELECT FROM users` dentro de una policy de `users` (causa recursión infinita)

### Tres clientes Supabase
- `lib/supabase/client.ts` → browser (Client Components)
- `lib/supabase/server.ts` → RSC y Route Handlers
- `middleware.ts` → middleware de Next.js

### Streaming (primer uso — 2026-04-02)
Patrón: `anthropic.messages.stream()` → `ReadableStream` con `TextEncoder` → cliente lee con `fetch body reader + TextDecoder`
- Metadata al final del stream: `\n__META__{json}__META__` — evita un segundo HTTP request para pasar datos post-stream al cliente
- Ver `src/lib/ia/soporte-chat.ts` y `src/app/(app)/soporte/soporte-chat.tsx`

### Límite client/server en componentes con IA
- Archivos que importan `next/headers` (como `lib/supabase/server.ts`) son **server-only**
- Un Client Component que importe transitivamente un archivo server-only lanza error en runtime
- **Solución:** Extraer constantes compartidas a un archivo neutral sin imports de servidor
- Patrón establecido: `src/lib/ia/soporte-constants.ts` — importable desde client y server

### Optimistic UI
`snapshot → setLoading(id) → try { await; if (error) throw; actualizar estado } catch { rollback snapshot } finally { setLoading(null) }`

### Types cross-boundary
Exportar tipos desde `page.tsx` (server), importar en client component con `import type { Foo } from "./page"`

---

## Reglas de documentación

Después de cada tarea completada debes:
1. Actualizar el `CLAUDE.md` de la carpeta correspondiente si creaste o modificaste archivos en ella
2. Registrar en `docs/decisiones.md` cualquier decisión técnica relevante con fecha y razón
3. Actualizar `docs/schema.md` si creaste o modificaste tablas en Supabase
4. Actualizar `docs/progreso.md` marcando qué está listo y qué sigue

---

## Contexto de negocio relevante

- **290 clientes del ebook** son la lista de conversión inmediata al lanzamiento
- **Beta cerrada:** ~11 de abril 2026
- **Lanzamiento público:** fines de abril 2026
- **Precio fundador:** $19.990 CLP/mes (2 semanas) → estándar $24.990 CLP/mes
- **MRR objetivo mes 3:** $4.000.000 CLP (~160 suscriptores)
- **Revenue share CreActive:** 30% de las ventas

---

## Estado actual del proyecto (2026-04-14) — post Servicio Primera Clase Fase 1

### Fase 0 (Infraestructura) ✅
- Next.js 14 + Supabase + Vercel deployado
- Schema v1 aplicado (users, pautas, suscripciones, asignaciones_pauta, checkins, tickets)

### Fase 0.5 (Digitalización) ✅
- Schema v2 aplicado — nuevas tablas: `screening_responses`, `recetas`, `faq` + columnas género/antropometría en `users` + tipo/familia/contenido en `pautas`
- **20 pautas iniciales** digitalizadas de PDF a JSONB estructurado en DB (6 familias: sandía, palta, frutos_secos, lima_limon, tuti_fruti, shock_semillas)
- **6 pautas de mantención** cargadas (etapas 1/2/3 × hombre/mujer) — `familia='mantencion'`, `fase_protocolo='mantencion'` — **Total: 26 pautas**
  - Estructura diferente: guía de porciones por grupo alimentario (no plan diario). JSON usa `tipo_contenido: "guia_porciones"`
  - Etiquetas pendientes validación Constanza
- **84 recetas** cargadas (41 carbo + 43 grasas) en tabla `recetas`
- **52 FAQ** cargadas en tabla `faq`
- **Etiquetas definitivas aplicadas y verificadas en remoto** — CSV validado por Constanza, migración `20260331100000_etiquetas_constanza.sql`
  - 20/20 pautas iniciales con etiquetas pobladas, 4 compatibles celiaquia
  - Nuevo formato: multi-objetivo con prioridad + condiciones clínicas (celiaquia, hipotiroidismo, etc.)
  - Ver `docs/mapping-etiquetas-propuesta.md` para el mapping completo

### Fase 1 (MVP) 🔨 — En curso
**Última actualización:** 2026-04-02

#### Auth + Onboarding ✅ (2026-04-01)
- `app/middleware.ts` — guards: anon → /login, autenticado + ruta auth → /
- `app/src/lib/auth.ts` — `getCurrentUser()`, `isScreeningComplete()`
- `app/src/app/page.tsx` — redirect según estado (login / screening / dashboard)
- `app/src/components/ui/` — Button, Input, Card, Logo, StepIndicator
- `app/src/app/(auth)/` — login, registro, forgot-password, auth/callback
- `app/src/app/(onboarding)/` — screening 11 pasos + procesando
- `app/src/app/(app)/` — layout header+nav + dashboard placeholder
- Tailwind brand colors + Inter/Playfair Display configurados

#### Motor IA + Vista Plan ✅ (2026-04-01)
- `app/src/lib/ia/asignar-pauta.ts` — scoring algorítmico (género, fase, condiciones, objetivos) + Claude API selección final
- `app/src/lib/ia/adaptaciones.ts` — mapa de sustituciones por intolerancia (7 tipos: lactosa, gluten, fructosa, huevo, mariscos, frutos secos, soya)
- `app/src/app/api/ia/asignar-pauta/route.ts` — POST autenticado, fire-and-forget desde screening
- `app/src/app/(app)/dashboard/page.tsx` — plan completo: desayuno/colaciones/almuerzo/cena + permitidos/prohibidos + adaptaciones
- Screening step 4 reestructurado: chips de intolerancias + campo libre
- `screening_responses.alergias_estructuradas text[]` — nueva columna para manejo estructurado

#### Check-in Diario ✅ (2026-04-01)
- `app/src/app/(app)/checkin/page.tsx` — Server component: auth, fetch daily check-in + streak + quincenal availability
- `app/src/app/(app)/checkin/checkin-form.tsx` — Client component: 3-question daily form (energía 1-5, digestión 1-5, adherencia sí/parcial/no) + streak + success view
- RLS fix: `WITH CHECK` added to `paciente_own_checkin_diario` policy
- Migration: `supabase/migrations/20260401300000_fix_checkin_diario_rls.sql`

#### Check-in Quincenal ✅ (2026-04-01)
- `app/src/app/(app)/checkin/checkin-quincenal.tsx` — Client component: 6-step multi-step form (síntomas, energía, adherencia pre-calculada, dificultades, contexto, peso)
- `app/src/app/(app)/checkin/checkin-quincenal-section.tsx` — Client component: banner wrapper that shows/hides the quincenal form
- `app/src/app/api/ia/ajuste-quincenal/route.ts` — POST endpoint: auth, insert checkin, trigger IA in background
- `app/src/lib/ia/ajuste-quincenal.ts` — Claude API (Sonnet 4.6) generates adjustment suggestion from check-in + pauta context + daily history
- RLS fix: `WITH CHECK` added to `paciente_own_checkin_quincenal` policy
- Migration: `supabase/migrations/20260401400000_fix_checkin_quincenal_rls.sql`
- **Design decisions:** Single `/checkin` route for both daily and quincenal. Quincenal unlocks 15 days after pauta assignment (or 15 days after last quincenal). Adherencia step pre-populated from daily data. Claude suggestion is fire-and-forget (Constanza reviews later). No memory persistence in suggestions.

#### Recetario ✅ (2026-04-01)
- `app/src/app/(app)/recetario/page.tsx` — Server component: auth, fetch recipes filtered by user's pauta type (carbo/grasas), fetch user favorites, extract categories
- `app/src/app/(app)/recetario/recetario-client.tsx` — Client component: category filter chips (scrollable horizontal), recipe grid (2 cols), recipe detail modal (bottom sheet with ingredients + preparation steps), favorites system (heart toggle, optimistic update, "Favoritas" filter tab)
- `supabase/migrations/20260401500000_recetas_favoritas.sql` — New table `recetas_favoritas` (user_id, receta_id, UNIQUE constraint) with RLS + WITH CHECK
- **Design decisions:** Recipes auto-filtered by user's active pauta type (carbo/grasas). If mantención or no pauta, shows all. Placeholder images with category emoji + gradient (ready for real images from Storage bucket `recetas`). Favorites with optimistic UI update. Detail modal as bottom sheet on mobile. 84 recipes total (41 carbo, 43 grasas) across 15 categories.

#### Dashboard Nutricionista ✅ (2026-04-02)
- `src/lib/auth.ts` — `getUserRole()` added
- `src/app/page.tsx` — Role redirect: nutricionista/admin → /nutricionista/dashboard
- `src/app/nutricionista/` — Full dashboard: layout + nav + 4 sub-pages (URLs: /nutricionista/*)
  - `dashboard/` — Metrics (pacientes activos, ajustes pendientes, tickets, adherencia 30d) + previews
  - `ajustes/` — Approve/reject AI-generated biweekly adjustment suggestions (optimistic UI)
  - `tickets/` — Respond to + resolve escalated support tickets (optimistic UI)
  - `pacientes/` — Patient list with search, status filter, expandable detail (screening + check-ins)

#### Soporte IA ✅ (2026-04-02)
- Tabla `uso_ia_mensual` + RPC `incrementar_uso_ia` — rate limiting atómico por usuario/mes
- `lib/ia/limites-soporte.ts` — trial=10, fundador=50, mensual=30 msgs/mes
- `lib/ia/soporte-context.ts` — context assembly: pauta + screening + check-ins + 52 FAQ
- `lib/ia/soporte-chat.ts` — streaming Haiku 4.5, detección escalación, fire-and-forget ticket
- `api/ia/soporte/route.ts` — POST: auth + rate limit + context + stream
- `(app)/soporte/` — page.tsx (server) + soporte-chat.tsx (client)
- Primer uso de streaming en el codebase — patrón: `anthropic.messages.stream()` → ReadableStream → fetch body reader

#### UI Sprint 1 — Rediseño Visual ✅ (2026-04-03)
- `tailwind.config.ts` + `postcss.config.js` — design tokens (shadows, borderRadius 4xl) + fix crítico Tailwind sin PostCSS
- `app-shell.tsx` — Client Component: header sticky (avatar+greeting+streak), nav glassmorphism 5 tabs, FAB chat overlay
- `dashboard/` — reescritura completa: ProgresoCard + MealCards (comidas_completadas) + QuickCheckin
- `plan/` — Server+Client: selector días, meal cards expandidas, lista de compras por categoría
- `recetario/` — búsqueda, cards verticales, overlay full-screen detalle
- `progreso/` — FaseCard, hidratación, síntomas, TrendCharts SVG, check-in quincenal integrado
- `perfil/` — hero card, Mi Salud, suscripción, comunidad, logout
- `api/ia/soporte-contexto/` — endpoint GET para overlay FAB chat
- Tabla `comidas_completadas` — migración `20260402100000_comidas_completadas.sql`

#### UI Sprint 2 — "The Modern Apothecary" ✅ (2026-04-03)
Refactor puramente visual. 31 archivos. Build: 26 rutas, 0 errores TypeScript.
- **Design System:** 4 tokens de superficie (surface/low/lowest/high), 3 tamaños editoriales (display/display-sm/editorial), ambient shadows, `.grain`, `.warm-mesh`, `.ghost-border`, `.stagger-children`
- **No-Border Rule:** Cero borders para seccionar contenido — solo tonal layering y ghost-border para inputs
- **App Shell:** outer `bg-surface warm-mesh`, header/nav glassmorphism, sidebar `grain`, FAB `animate-breathe`
- **Todas las páginas paciente:** heroes `rounded-[2rem] grain`, headings `font-serif`, chips sin border, `stagger-children`
- **Auth/Onboarding:** layout `warm-mesh grain`, chips `bg-surface-low`, RadioCards `ring-1 ring-sandia/20`, procesando `animate-breathe text-editorial`
- **Soporte IA:** burbujas `bg-surface-low`, input `ghost-border-input`
- **Nutricionista:** layout `warm-mesh`, cards `bg-surface-lowest`, borders eliminados en los 4 archivos

#### Fixes Beta ✅ (2026-04-03)
- Skip delay 24h: asignar-pauta ahora awaited → redirect directo a `/dashboard`
- Error registro: manejo específico de `429 email rate limit` de Supabase
- Redirect directo a `/screening` cuando `confirm email` desactivado en Supabase
- Repo consolidado: `app/` + `supabase/` + `docs/` en un solo git repo → `creactive-dev/nutrisco`
- Variables de entorno configuradas en Vercel Dashboard

#### QA Sprint ✅ (2026-04-03)
16 issues pre-beta resueltos. Ver `docs/progreso.md` y `docs/decisiones.md` para el detalle completo.
Nuevas tablas: `registro_diario`, `conversaciones_soporte` (migración `20260403000000`).
Nuevos archivos clave: `_components/receta-detail.tsx` (componente compartido), `api/soporte/conversacion/route.ts`.
Build: 26 rutas, 0 errores TypeScript.

#### Sesión 6: UX Tarjetas de Comida ✅ (2026-04-02)
- Chips Proteínas/Verduras/Frutas en `WeeklyVariantCard` ahora colapsables (cerrados por defecto). Sub-componente `CollapsibleChips`.
- Chips Opciones/Evitar en `StructuredDesc` ahora colapsables (cerrados por defecto).
- Acordeón redundante "Ver alimentos permitidos de tu pauta" eliminado de `MealCardExpanded` (~50 líneas).
- Favoritos de recetas disponibles desde la vista Plan: `plan/page.tsx` fetch `recetas_favoritas`, `PlanClient` gestiona `favoritas: Set<string>` + `toggleFavorita()` optimista, `RecetaDetail` recibe `isFav`/`onToggleFav` desde Plan.
- Build: 26 rutas, 0 errores TypeScript.

#### Refactorización Pautas — Sesiones 1-3 ✅ (2026-04-02) — Deploy atómico
- **Sesión 1:** Fix `waitUntil` en `ajuste-quincenal/route.ts` + `soporte/route.ts`. Tipos centralizados en `lib/types/pauta.ts`. Funciones puras en `lib/pauta-helpers.ts`. Componentes `StructuredDesc.tsx` + `WeeklyVariantCard.tsx` extraídos. ~300 líneas de duplicación eliminadas de `plan-client.tsx` y `dashboard-client.tsx`. Badge "X/7 días" eliminado de `WeeklyVariantCard`.
- **Sesiones 2+3 (atómico):** 20/20 pautas migradas de strings monolíticos a arrays atómicos. Script `app/scripts/migrate-pautas.mjs`. Tabla backup `pautas_backup` en Supabase. `proteinas_permitidas`/`verduras_permitidas`/`frutas_permitidas`/`aderezos` → `string[]`, `almuerzo.entrada`/`cena.entrada` → `string[]`, `almuerzo.plato_fondo`/`cena.plato_fondo` → `RotacionPlato` donde aplica. UI: `rotacionToStr()` serializa `RotacionPlato` → string parseable (zero-risk), acordeón "Ver alimentos permitidos" en `MealCardExpanded`, entradas como bullet list. 6 pautas de mantención NO migradas.
- Build: 26 rutas, 0 errores TypeScript.

#### Lista de Compras v2 — Sesión 4 ✅ (2026-04-02)
- `src/lib/lista-compras.ts` — `buildListaCompras()`: consolida items de pauta base + ingredientes de recetas sugeridas de la semana, deduplica por normalize(), agrupa en 6 pasillos de supermercado chileno. `clasificarPasillo()` por keyword matching. `loadListaState()` / `saveListaState()` para persistencia en localStorage con key `nutrisco_lista_v2_{userId}`. Tipos: `CompraItem`, `PasilloKey`, `ListaByPasillo`, `ListaComprasState`.
- `src/components/lista-compras/ListaComprasV2.tsx` — Client Component: secciones por pasillo (oculta vacíos), checkboxes con nota de receta de origen, sección Extras (input + Enter), sección "En el carro" con botón "Vaciar", estado persistido en localStorage vía `useEffect` (sin SSR mismatch). Pasillos: Frutas y Verduras / Carnes y Proteínas / Lácteos y Huevos / Abarrotes y Despensa / Panadería y Cereales / Otros.
- `plan-client.tsx` — reemplazado componente inline `ListaCompras` por `<ListaComprasV2 userId={userId} ...>`. Eliminados imports obsoletos (`parseListaCompras`, `Sparkles`, `ChefHat`, `Check`).
- Build: 26 rutas, 0 errores TypeScript.

#### Servicio Primera Clase — Fase 1 ✅ (2026-04-14)
- `lib/copy/voz.ts` — fuente única de copy (9 templates + `FRASES_CONSTANZA`)
- `lib/email/resend-client.ts` — cliente Resend + `enviarEmail()` + `crearNotificacion()`
- `resend ^6.11.0` instalado
- `vercel.json` — 6 crons (entregar-planes, recordar-checkin, reengagement, hitos, cerrar-semana, **detectar-sintomas**)
- Cron handlers: `/api/cron/{entregar-planes,recordar-checkin,hitos,reengagement}`
- `/api/auth/bienvenida` — email bienvenida al registro
- `/procesando` refactorizado: Server Component + delay 24h restaurado + WelcomeAsset flexible
- `asignaciones_pauta.visible_para_paciente` — gate del delay 24h
- `/api/nutricionista/ajustes/[id]/aprobar` — nota obligatoria (20-300 chars) + email + notificación
- `ajustes-client.tsx` — textarea obligatoria antes de aprobar
- `/api/nutricionista/tickets/[id]/responder` — email + notificación al responder
- `tickets-client.tsx` — llama al endpoint en lugar de Supabase directo
- `/api/notificaciones` — GET (lista + unread) + POST (marcar leídas)
- `/api/users/last-active` — PATCH debounced desde app-shell
- `app-shell.tsx` — Bell icon + badge unread + InboxOverlay + hook last_active_at
- `nutricionista/dashboard` — widget "Pacientes en riesgo" (top 5 por inactividad + WhatsApp CTA)
- Migración `20260414100000_servicio_primera_clase.sql` — **pendiente aplicar en remoto**

#### Servicio Primera Clase — Fase 2 ✅ (2026-04-14)
- `dashboard-client.tsx` — `ConstanzaCard` con frase rotativa diaria (determinista, sin estado)
- `nutricionista/alertas/page.tsx` + `alertas-client.tsx` — cola priorizada de alertas (Urgente/Atención/Informativo)
- `/api/nutricionista/alertas/[id]/resolver` — POST idempotente
- `nutricionista/layout.tsx` — link "🚨 Alertas" agregado al nav
- `/api/cron/detectar-sintomas` — analiza quincenales 24h, delta síntomas ≥3 → alerta `sintomas_empeorando`
- `supabase/migrations/20260414200000_caso_clinico_trigger.sql` — trigger SECURITY DEFINER detecta celiaquía, 2+ condiciones, alto rendimiento + diagnóstico
- `(app)/perfil/inbox/page.tsx` — historial completo de notificaciones (últimas 100)
- `perfil/page.tsx` — link "Mensajes de Constanza" en sección Comunidad + `PerfilEdit` integrado
- `(app)/perfil/perfil-edit.tsx` — alergias (chips predefinidos + texto libre) + exclusiones editables
- `/api/perfil/alergias` + `/api/perfil/exclusiones` — PATCH endpoints

#### Servicio Primera Clase — Fase 3: Mercado Pago ✅ (2026-04-14)
- `lib/mercadopago/client.ts` — cliente REST MP (`crearPreapproval`, `getPreapproval`, `PRECIOS_PLAN`)
- `api/webhooks/mercadopago/route.ts` — webhook con verificación HMAC-SHA256, upsert suscripciones, update users.estado_suscripcion, email confirmación
- `api/suscripciones/crear/route.ts` — POST: crea preapproval y retorna init_point
- `app/suscribirse/page.tsx` + `suscribirse-client.tsx` — paywall con diseño Modern Apothecary, maneja estado suspendida/cancelada/sin suscripción
- `(app)/layout.tsx` — gate de suscripción: redirige a `/suscribirse` si `estado_suscripcion NOT IN ('activo', 'trial')`
- `voz.ts` — template `suscripcionActivada()` para email de confirmación post-pago
- Build: 20 rutas API, 0 errores TypeScript

#### Pendiente pre-deploy (configuración — NO código)
- ~~Aplicar migraciones `20260414100000` y `20260414200000` en Supabase remoto~~ ✅ HECHO
- Vercel Dashboard → Environment Variables (Production + Preview):
  - `RESEND_API_KEY` = `re_ELUKP5Ju_EcXsLEbZees44ZbBBD7MwGV9`
  - `EMAIL_REMITENTE` = `Constanza de Nutrisco <contacto@constanzanutricion.cl>`
  - `CRON_SECRET` = `35fbbbae5c1e0d64a5b12b52aac15483b97478ee748f5348e09e2c6fb916c288`
  - `NEXT_PUBLIC_APP_URL` = URL de producción
  - `MP_ACCESS_TOKEN` = Access Token de producción (Dashboard MP → Credenciales)
  - `MP_WEBHOOK_SECRET` = Clave secreta del webhook (Dashboard MP → Webhooks → crear webhook → `/api/webhooks/mercadopago`)
- Resend Dashboard → Domains → verificar `constanzanutricion.cl` (TXT + DKIM)
- Link WhatsApp real de Constanza en `perfil/page.tsx` (reemplazar `https://chat.whatsapp.com/`)
- Para beta: SET `estado_suscripcion = 'trial'` en `users` para pacientes beta vía Supabase Dashboard
- Asset de bienvenida para `/procesando` (decisión de formato pendiente)

**Target:** Beta cerrada ~18 abril 2026

⚠️ **Entorno:** Next.js 14 requiere Node.js v18 o v20. Node v24 no es compatible. Vercel usa v20 por defecto (deploy OK).

### Notas operativas
- **Proyecto Supabase:** `kkkqpkyltekphrurjzwp` — reactivado 2026-03-31
- **MCP Supabase:** Configurado y apuntando a Nutrisco. White Cassini disponible como `supabase-white-cassini`.
- **MercadoPago:** Cuenta verificada y lista para suscripciones.
- **Migraciones como seeds:** Los datos iniciales se cargaron como migraciones numeradas (`20260331000001` a `20260331000004`)
- **Dev server:** `cd app && /opt/homebrew/opt/node@20/bin/node node_modules/.bin/next dev` — usa Node v20 (v24 no compatible). Puerto 3000 por defecto; si ocupado, sube a 3001, 3002, etc.
- **Usuario de prueba:** `hola@creactivestudio.agency` — screening completo, pauta Lima Limón 1 - Hombre asignada. Para probar nutricionista: `UPDATE users SET rol = 'nutricionista' WHERE email = 'hola@creactivestudio.agency';`

---

*Proyecto de CreActive Studio — Confidencial*
