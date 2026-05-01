---
name: Kitchat Landing Page — estado
description: Estado del proyecto de landing page de venta para Kitchat (kitchat.cl). Sigue el flujo PRO de CreActive.
type: project
originSessionId: f509b165-7bf3-4ded-b542-a413d33ca4d6
---
PRD v1.0 generado el 2026-04-20 desde dos docs fuente exhaustivos (brief estratégico + GTM report v1.0).

**Ruta PRD:** `clientes/kitcha/prd-landing-v1.md`
**Repositorio:** `creactive-dev/kitchat` (GitHub)
**Ruta local:** `clientes/kitcha/outputs/kitcha-landing/`
**Dominio:** kitchat.cl

**Why:** Kitchat necesita flujo de conversión self-serve para escalar más allá de los primeros clientes.

**How to apply:** Visual v6 + commit ee1455e pusheado (2026-04-23). Próximo: QA visual mobile+desktop → deploy Vercel.

## Estado (2026-04-28 sesión 17) — ENV VARS VERCEL CORREGIDAS ✅ — Primer cliente activo

### Qué se hizo en sesión 17

- ✅ **Env vars Vercel corregidas**: `NEXT_PUBLIC_SUPABASE_URL` tenía trailing `\n` → URL malformada. `NEXT_PUBLIC_SUPABASE_ANON_KEY` era la key pre-rotación (iat: marzo 2025) → 401 silencioso. Ambas causaban que el polling de `/gracias` fallara silenciosamente. Oscar corrigió desde Vercel Dashboard.
- ✅ **Prod verificada**: Vercel auto-redeployó. Polling de `/gracias` ahora detecta `status='paid'` y muestra form de contraseña.

### Próximo paso

1. **Webhook global MP Dashboard** (tarea crítica para que no requiera rescue manual)
2. Reemplazar `56XXXXXXXXX` en `gracias/page.tsx` (×3), `BillingLapsedPage.jsx` (×1), `constants.ts` (×1)
3. Test flujo anual E2E

### Gotchas técnicos nuevos (sesión 17)

- **Next.js compila `\n` de env vars en el bundle**: Si la var se guarda con newline en Vercel, el string en el bundle incluye `\n` literalmente. El Supabase client falla todas las requests silenciosamente.
- **Diagnosticar env vars compiladas**: `curl https://kitchat.cl/_next/static/chunks/app/suscribirse/page-*.js | grep gjkaboosygjitxgqcawy` → si sale `gjkaboosygjitxgqcawy.supabase.co\n"` hay trailing newline. Buscar el chunk con `placeholder` para verificar si la anon key es el fallback.

---

## Estado (2026-04-27 sesión 14) — LANDING PULIDA ✅ — CTAs corregidos, www resuelto, demo link real

### Commits sesión 14 (2026-04-27)

| Commit | Descripción |
|--------|-------------|
| `1a830ab` | fix: CTA mobile navbar "Probar 7 días gratis →" → "Empezar ahora →" |
| `918eea9` | fix: demo link → `mcdonald-s-antofagasta-playa.kitchat.cl/` |

### Qué se hizo en sesión 14

- ✅ **CTA mobile navbar**: "Probar 7 días gratis →" → "Empezar ahora →" (2 ocurrencias en menú mobile del Navbar).
- ✅ **www.kitchat.cl → landing**: El wildcard `*.kitchat.cl` de la customer app capturaba `www`. Fix: agregar `www.kitchat.cl` explícitamente al proyecto landing en Vercel. DNS en Vercel → se configura automático. Exact match gana sobre wildcard.
- ✅ **Demo link actualizado**: `LINKS.demo` en `lib/constants.ts` → `https://mcdonald-s-antofagasta-playa.kitchat.cl/`. Aplica en 5 lugares (Navbar desktop, Navbar mobile, CTAFinal, ReviewsAI, Footer).

### Gotchas técnicos nuevos (sesión 14)

- **Vercel exact domain > wildcard**: Si `*.kitchat.cl` está en un proyecto y `www.kitchat.cl` se agrega explícitamente a otro, el segundo gana. No requiere cambios de DNS manual — Vercel los configura automáticamente cuando el DNS está en Vercel.
- **DNS en Vercel = sin tocar registros manualmente**: Al agregar un dominio a un proyecto Vercel cuando el DNS ya está en Vercel, los registros A/CNAME se crean solos. No ir al panel de DNS a agregar nada.

### Próximo paso

1. Reemplazar `56XXXXXXXXX` con número real WA Kitchat:
   - `app/gracias/page.tsx` (3 ocurrencias)
   - `admin-react/src/pages/BillingLapsedPage.jsx` (1 ocurrencia)
   - `lib/constants.ts` → `LINKS.waSales` (1 ocurrencia)
2. Commitear edge functions al repo `creactive-dev/white-cassini` (`mp-checkout-create`, `mp-webhook`, `_shared/mercadopago.ts`)
3. Test flujo anual end-to-end
4. Primer pago real de cliente

---

## Estado (2026-04-27 sesión 13) — FLUJO ANUAL IMPLEMENTADO ✅ — billing_type en pending_signups

### Commits sesión 13 (2026-04-27)

| Commit | Descripción |
|--------|-------------|
| `cb1639b` | fix: CTA navbar "Probar gratis" → "Empezar ahora" |
| `1b81fbb` | feat: flujo de pago anual via /suscribirse?billing=annual |

### Qué se hizo en sesión 13

- ✅ **Fix precio MP**: `mp-checkout-create` tenía rate limiting que reutilizaba `init_point` con precio $49.900 stale. Eliminado el bloque de caching — ahora siempre crea preapproval fresco.
- ✅ **CTA navbar**: "Probar gratis" → "Empezar ahora"
- ✅ **Migration DB**: `billing_type text DEFAULT 'monthly' CHECK IN ('monthly','annual')` en `pending_signups`
- ✅ **Flujo anual `/suscribirse?billing=annual`**: form muestra $593.810 IVA incl/año + "2 meses gratis". Submit guarda `pending_signup` con `billing_type='annual'` y redirige al link MP estático.
- ✅ **`mp-webhook` anual**: matchea `payment` events por `payer.email + transaction_amount >= 593000` → marca `pending_signup` como `paid`.
- ✅ **`Pricing.tsx`**: CTA "Pagar año completo" → `/suscribirse?billing=annual` (en vez de link directo a MP).

### Gotchas técnicos nuevos (sesión 13)

- **Rate limiting de `mp-checkout-create` causaba precio stale**: si el mismo email tenía un `pending_signup` con `status='pending'` de un intento anterior, la función retornaba el `init_point` antiguo (creado cuando el precio era $49.900). Fix: eliminar el bloque de rate limiting (líneas 99–120 del original). Ahora siempre crea preapproval fresco.
- **Link estático `mpago.li/2Pzv3FE` no acepta `back_url` ni `external_reference`**: es un link de pago fijo de MP. No se puede automatizar el redirect post-pago ni linkear con un pending_signup por `external_reference`. El matching se hace por email+monto en el webhook.
- **Node.js v24 local incompatible con Next.js 14**: `npm run build` local falla. Vercel usa versión correcta. Usar TypeScript check en su lugar para validar tipos localmente.

### Account creation post-pago anual

Oscar ve en Supabase quién pagó anual:
```sql
SELECT email, nombre_local, status, paid_at 
FROM pending_signups 
WHERE billing_type = 'annual' 
ORDER BY created_at DESC;
```
Cuando `status='paid'` → crear cuenta manualmente (INSERT restaurantes + INSERT suscripciones con `current_period_end = now() + interval '365 days'`).

### Próximo paso

1. Reemplazar `56XXXXXXXXX` con número real WA Kitchat (3 archivos)
2. Commitear `mp-webhook/index.ts` + `_shared/mercadopago.ts` al repo `creactive-dev/white-cassini`
3. Test flujo anual end-to-end (form → MP link → webhook → paid)
4. Primer pago real de cliente

---

## Estado (2026-04-27 sesión 12) — LANDING EN VERCEL FUNCIONANDO ✅ — Pricing actualizado, flujo MP activo

### Commits sesión 12 (2026-04-27)

| Commit | Descripción |
|--------|-------------|
| `378449a` | fix: SSR-safe Supabase client init + sessionStorage guard |
| `aae7dae` | fix: wrap useSearchParams in Suspense boundary for Next.js 14 |
| `e7f8740` | fix: actualizar precio Pro a $59.381 (IVA incluido) |
| `74bdd37` | feat: pricing neto + IVA mensual, anual con link de pago MP |

### Qué se hizo en sesión 12

- ✅ **Vercel build fix 1** — `lib/supabase.ts`: `createClient` lanzaba "supabaseUrl is required" durante SSR prerender porque las vars `NEXT_PUBLIC_*` no estaban configuradas en Vercel. Fix: usar fallbacks placeholder no-vacíos en lugar de `!` assertion.
- ✅ **Vercel build fix 2** — `useSearchParams()` en Next.js 14 App Router requiere `<Suspense>` boundary. Ambas páginas (`/suscribirse` + `/gracias`) refactorizadas: contenido en `XxxContent()`, export default es wrapper con `<Suspense>`.
- ✅ **Precio mensual display**: `$49.900 + IVA /mes` (neto). DB cobra $59.381 (con IVA). Landing muestra neto.
- ✅ **Precio anual**: `$593.810/año` IVA incluido. CTA anual → link MP directo `https://mpago.li/2Pzv3FE` (no suscripción recurrente). 2 meses gratis.
- ✅ **Precios actualizados** en `constants.ts`, `Pricing.tsx`, `NoCommissions.tsx`, `suscribirse/page.tsx`.

### Pendientes del cliente (con ubicación exacta)

1. **Número WA ventas** → `lib/constants.ts` → `LINKS.waSales` → reemplazar `56XXXXXXXXX`
2. **Número WA soporte** → `app/gracias/page.tsx` → 3 ocurrencias de `56XXXXXXXXX` (timeout + expired + failed)
3. **Logo Kitchat SVG/PNG** → Navbar.tsx + Footer.tsx usan texto placeholder
4. **Permiso testimonios** → citas en SocialProof.tsx son fallback
5. **Decisión analytics** → GA4/Plausible → agregar script en `layout.tsx`

### Gotchas técnicos nuevos (sesión 12)

- **Next.js 14 + `useSearchParams()` en `'use client'`**: aunque sea client component, Next.js intenta pre-renderizar en build. `useSearchParams()` lanza error a menos que esté envuelto en `<Suspense>`. Patrón: extraer a `XxxContent()` + export default con `<Suspense><XxxContent /></Suspense>`.
- **`createClient(undefined!, undefined!)` en build**: Supabase JS v2 valida que la URL sea string no-vacío. Usar fallback `?? 'https://placeholder.supabase.co'` para que el build no explote cuando las `NEXT_PUBLIC_*` vars no están en Vercel durante el build estático.
- **Vercel env vars no son automáticas**: aunque el `.env.local` local funciona, Vercel necesita que las 3 vars (`NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `NEXT_PUBLIC_ADMIN_URL`) estén en Dashboard → Settings → Environment Variables del proyecto `creactive-dev/kitchat`.

### Próximo paso

1. Reemplazar `56XXXXXXXXX` con número real de WA Kitchat (soporte + ventas)
2. Verificar que el flujo completo funciona en producción: landing → /suscribirse → MP → /gracias → admin

---

## Estado (2026-04-23) — V6 COMMITEADA Y PUSHEADA ✅

- ✅ PRD v1.0 — `clientes/kitcha/prd-landing-v1.md`
- ✅ Estructura v1.0 — `clientes/kitcha/estructura-landing-v1.md`
- ✅ Plan de trabajo v1.0 — `clientes/kitcha/plan-trabajo-landing-v1.md`
- ✅ Build v1 — 24 archivos, 142 kB
- ✅ **Visual v2** — commit 6112648 (2026-04-20)
- ✅ **Visual v3** — mobile audit + feedback Oscar (parte de ee1455e)
- ✅ **Visual v4** — bento + logos reales + bugfixes (parte de ee1455e)
- ✅ **Visual v5** — hero 2 imágenes + ReviewsAI zig-zag + Pricing + métricas (parte de ee1455e)
- ✅ **Visual v6** — overflow fix + radar despacho + RepeatOrder VIP + mini mac mobile + Hero mobile fix (ee1455e, 2026-04-23)
- ✅ **Commit + Push** — `ee1455e` en main, 23 archivos, repo `creactive-dev/kitchat`

## Cambios v6 (2026-04-23) — en ee1455e

| Archivo | Cambio |
|---------|--------|
| `app/globals.css` | `overflow-x: hidden` en html+body — fix definitivo scroll horizontal |
| `components/sections/Hero.tsx` | Mobile: laptop full-width + phone absoluto `bottom-0 left-0 w-[20%]` (antes side-by-side con traslape; antes `bottom-[-12%]` que sobresalía) |
| `components/sections/Features.tsx` | ZonaDespacho → radar SVG 3 anillos concéntricos desde pin central verde; RepeatOrder → perfil VIP + 2 filas historial + precio; "Menú con tu marca" mobile → `menu-mini-mac.png` (500×500) |
| `public/menu-mini-mac.png` | NEW: 500×500 PNG copia de `Referencias/mini mac.png` |

## Archivos public/ (todos commiteados en ee1455e)

| Archivo | Contenido |
|---------|-----------|
| `public/hero-computador.png` | Screenshot Chrome panel admin Kitchat — Hero |
| `public/hero-celular.png` | iPhone mockup menú white-label — Hero |
| `public/hero-mockup.png` | Composite antiguo — NO SE USA (candidato a borrar) |
| `public/menu-phone-kitchat.png` | Frame iPhone — Features white-label card (desktop/tablet) |
| `public/menu-mini-mac.png` | Mac mockup — Features white-label card (mobile only, sm:hidden) |
| `public/logo-el-padrino.png` | Logo El Padrino Pizza |
| `public/logo-felds-kitchen.png` | Logo Feld's Kitchen |
| `public/logo-freires-express.png` | Logo Freire's Express |
| `public/menu-mockup-phone.png` | Antiguo — candidato a borrar |
| `public/howitworks-step3.png` | Antiguo — candidato a borrar |

## Estado de componentes mockup

- `DashboardMockup.tsx` — no importado — candidato a borrar
- `ElPadrinoPhoneMockup.tsx` — no importado — candidato a borrar
- `WhatsAppOrderMockup.tsx` — no importado — candidato a borrar
- `OrdersPanelMockup.tsx` — ✅ en uso: HowItWorks (dark) + Features (light). Sidebar `hidden sm:flex`.
- `Counter.tsx` — ✅ en uso en Problem.tsx

## Decisiones cerradas (acumuladas)

- **CTA trial:** `href="#"` — hotfix cuando exista `app.kitchat.cl/signup`
- **Mockups:** mayoría en CSS/Tailwind; Hero usa PNGs reales separados
- **Hero mobile v6:** laptop full-width + phone absoluto bottom-0 left-0 w-20% (side-by-side descartado por traslape)
- **Hero desktop:** laptop full-width + phone absoluto bottom-[-18%] left-0 w-28% (no tapa panel de pedido)
- **Calculadora NoCommissions:** 30% tasa Rappi, slider $500K–$15M
- **HowItWorks tema:** light (white)
- **Plan Esencial:** eliminado — Pro es el entry point
- **CTA global:** "Empezar a recibir pedidos"
- **CommissionDonut:** dice "apps" no "Rappi" — más genérico
- **Phone en Features desktop:** `absolute right-[-16px] top-1/2 -translate-y-1/2`, hidden en mobile
- **"Menú con tu marca" mobile:** mini mac.png (500×500 cuadrado) en lugar de phone
- **logoBg por logo:** El Padrino #111111, Feld's Kitchen #FFFFFF, Freire's Express #F5F0DC
- **Pricing:** 3 cols centradas, Pro con dark card que sobresale verticalmente en md+
- **ReviewsAI flow:** zig-zag 3 pasos (como HowItWorks) con visual cards propias
- **OrdersPanelMockup mobile:** sidebar hidden, solo chat + order detail
- **Métricas bento:** pedidos hoy / clientes frecuentes / ticket promedio
- **ZonaDespacho:** radar SVG 3 anillos concéntricos, pin verde central, dots rojo/amarillo por zona
- **RepeatOrder:** perfil VIP + historial 2 pedidos para no desbalancear bento grid
- **overflow-x global:** `overflow-x: hidden` en html+body en globals.css (fix definitivo para scroll horizontal causado por phone `right-[-16px]` en card white-label)

## Gotchas técnicos (acumulados)

- Dev server necesita `pkill next dev && rm -rf .next` cuando hay cambios grandes de módulos
- `React.CSSProperties` en TS requiere `import React from 'react'` explícito
- Primer compile con Turbopack tarda ~6 minutos (349s). Compilaciones subsiguientes: 63–266ms. Es normal.
- Filenames de macOS con U+202F (NARROW NO-BREAK SPACE antes de "p.m.") rompen rutas directas. Usar `glob` para encontrar el archivo.
- `nohup npm run dev` necesario para que el proceso sobreviva al ambiente de herramientas.
- **hero-computador.png y hero-celular.png:** usar `unoptimized` prop. Sin dimensiones exactas conocidas; usar 1280×800 y 390×780 como hints de layout.
- **Logos PNG con fondo incorporado:** El Padrino tiene fondo negro en el PNG mismo → `logoBg: '#111111'` en el contenedor.
- **Barras BarChart:** contenedor `relative` con fondo coloreado + un solo div `absolute` verde animando width.
- **OrdersPanelMockup sidebar `hidden sm:flex`:** sidebar usa `flex flex-col` como layout — necesita `sm:flex` no `sm:block`.
- **Features white-label card phone overflow:** `sm:overflow-visible` + phone `right-[-16px]` puede causar horizontal scroll si html/body no tienen `overflow-x: hidden`. Fix: globals.css.
- **Hero mobile phone `bottom-[-X%]`:** puede hacer que el phone se cuele debajo de la sección si el padding no es suficiente. Usar `bottom-0` para alinear al borde del laptop.
- **mini mac.png:** 500×500 cuadrado (no portrait) — mostrar a 140×140 con `unoptimized`.
- **RepeatOrder expansión:** si tiene demasiadas filas (>2 +header), el card se vuelve más alto que sus vecinos en el grid y desbalancea la fila. Usar máximo 2 historial rows.

## Pendientes del cliente (con ubicación exacta)

1. **Número WA ventas** → `lib/constants.ts` → `LINKS.waSales` → reemplazar `56XXXXXXXXX`
2. **URL trial** → `lib/constants.ts` → `LINKS.trial` → reemplazar `'#'`
3. **Logo Kitchat SVG/PNG** → Navbar.tsx + Footer.tsx usan texto placeholder
4. **Permiso testimonios** → citas en SocialProof.tsx son fallback — pedir cita real a El Padrino, Feld's Kitchen, Freire's Express
5. **Decisión analytics** → GA4/Plausible → agregar script en `layout.tsx`
6. **Validar 8 FAQ** → `lib/constants.ts` → `FAQ_ITEMS`

## Git

- **Repo:** `https://github.com/creactive-dev/kitchat`
- **Branch:** `main`
- **Último commit push:** `ee1455e` — feat: landing visual v3-v6 (2026-04-23)
- **Estado:** limpio, en sync con origin/main

## Próximo paso

1. **QA visual:** abrir en mobile 375px + desktop 1440px. Revisar especialmente:
   - Hero mobile: laptop full-width + phone superpuesto (no traslape)
   - Features bento: radar despacho, RepeatOrder VIP, mini mac mobile
   - Pricing: Pro card elevated (md:-mt-4/-mb-4)
   - Scroll horizontal: debe estar eliminado en todos los tamaños
2. **Deploy Vercel:** vercel.com → New Project → Import `creactive-dev/kitchat` → deploy → dominio `kitchat.cl`
3. **Compartir URL con Oscar/Kitchat** para aprobación final y pendientes del cliente
