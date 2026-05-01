---
name: White Cassini — estado del proyecto
description: SaaS restaurantes (Kitchat). Messaging audit ✅ (2026-05-01): welcome dedup 24h, toggle transferencia en Mensajes Automáticos, prefix "Acá debes transferir", encuesta bloqueada sin google_review_url. Commit 76e35f3.
type: project
originSessionId: 8bad418c-9634-42ae-806c-1e4f8bdbbe0d
---

## Estado: EN PRODUCCIÓN — messaging behavior audit completo ✅ (2026-05-01)

---

## Sesión 2026-05-01 (tarde) — Messaging behavior audit: 4 fixes

### Tipo: 🔧 Técnico

### Completado

- ✅ **Migración `20260501_welcome_sent_at.sql`**: `clientes.welcome_sent_at timestamptz` — columna para deduplicar bienvenida.
- ✅ **Commit `76e35f3`** (4 archivos, 2 edge functions deploadas):
  - `kapso-webhook`: `clienteRow` hoistado fuera de `if (incomingText)` — ahora siempre se busca el cliente (con `welcome_sent_at`). Welcome: solo se envía si no fue enviado en las últimas 24h; después de enviar, actualiza `welcome_sent_at`.
  - `kapso-webhook`: mensaje de transferencia ahora respeta toggle `mensajes.transferencia` y antepone `"Acá debes transferir:\n\n"` al texto de `bank_instructions`.
  - `SettingsPage.jsx`: card "Datos de Transferencia" con toggle en la sección Mensajes Automáticos de Integraciones. Toggle `mensajes.transferencia`. Sin textarea custom (el texto viene de Operaciones).
  - `kapso-feedback-scheduler`: bloquea la encuesta si `google_review_url` está vacío — hace `continue` (no marca como enviado) para que se reintente si el restaurante configura la URL dentro de la ventana de 24h.
  - `SettingsPage.jsx`: eliminado `Textarea` de los imports de HeroUI (ya no se usa).

### Pendiente

- ⏳ **Configurar `bank_instructions`** (Oscar): Settings > Operaciones > Transferencia → escribir mensaje completo → guardar.
- ⏳ **QA flujo transferencia** (Oscar): pedido de prueba con método "Transferencia" → WA → verificar auto-respuesta con "Acá debes transferir:\n\n" + datos.
- ⏳ **Configurar `google_review_url`** (Oscar): Integraciones > Encuesta Post-Entrega → agregar URL de Google Reviews → la encuesta se activará automáticamente.
- ⏳ **Webhook global MP Dashboard** (Oscar — CRÍTICO): URL `https://gjkaboosygjitxgqcawy.supabase.co/functions/v1/mp-webhook`
- ⏳ **Reemplazar `56XXXXXXXXX`** (5 puntos en el código)

### GOTCHAs

- **Toggle `transferencia` por defecto activo**: el toggle `kapso.mensajes.transferencia` es nuevo — `undefined` se interpreta como `true` (enabled), igual que los otros mensajes. Si el restaurante no ha guardado explícitamente `false`, el toggle estará activo.
- **clienteRow siempre se busca**: la búsqueda del cliente en kapso-webhook ya no está gateada en `incomingText`. Se hace siempre (para welcome dedup). Las operaciones de review y transfer siguen gateadas en `if (incomingText && clienteRow)` y `if (clienteRow)` respectivamente.
- **Encuesta: `continue` no marca `feedback_sent = true`**: si no hay URL, el pedido sigue elegible. Si el restaurante agrega la URL dentro de 24h post-entrega, la encuesta se enviará en el próximo ciclo del cron. Después de 24h, el cleanup la marca como enviada.

---

## Sesión 2026-05-01 (noche) — Polish UI Settings: tarjeta Transferencia

### Tipo: 🔧 Técnico

### Completado

- ✅ **Commit `db27ec3`**: eliminado campo `bank_alias` (Input "CBU / Alias / Banco") de la tarjeta Transferencia en Settings. Solo queda el textarea `bank_instructions`. Placeholder mejorado (instructivo, no datos de ejemplo).
- ✅ **Commit `cdeda9d`**: label del Textarea movido a `<p>` manual encima, description debajo como texto `10px`. Placeholder estructurado (`Nombre completo / RUT / Tipo de cuenta / Número / Banco / Email`).
- ✅ **Commit `e5acfeb`**: reemplazado HeroUI `<Textarea>` por `<textarea>` nativo con clases Tailwind. Borde visible, fondo blanco/dark, focus ring púrpura. Build ✓ sin errores. Pusheado a main → Vercel deploando.

### Pendiente (sin cambios respecto a sesión anterior)

- ⏳ **Configurar bank_instructions** (Oscar): Settings > Operaciones > Transferencia → escribir mensaje completo → guardar.
- ⏳ **QA flujo transferencia** (Oscar): pedido de prueba con método "Transferencia" → WA → verificar auto-respuesta con datos bancarios.
- ⏳ **Webhook global MP Dashboard** (Oscar — CRÍTICO): URL `https://gjkaboosygjitxgqcawy.supabase.co/functions/v1/mp-webhook`
- ⏳ **Reemplazar `56XXXXXXXXX`** (5 puntos en el código)

### GOTCHAs

- **HeroUI `<Textarea>` con `label` prop**: el label flotante se renderiza gigante cuando el campo está vacío — no usar `label` prop en textareas dentro de cards con layout propio. Usar `<p>` manual encima + `<textarea>` nativo con Tailwind para control total.
- **HeroUI `Textarea variant="bordered"`**: en contextos de card anidada no siempre muestra el borde visual. Si la UI necesita borde garantizado, preferir `<textarea>` nativo.

---

## Sesión 2026-05-01 — Flujo automático de datos de transferencia por WhatsApp

### Tipo: 🔧 Técnico

### Completado

- ✅ **Commit `991f03a`**: flujo completo de datos de transferencia por WhatsApp:
  - `admin-react/src/pages/SettingsPage.jsx`: Textarea "Mensaje WhatsApp" (`bank_instructions`) en tarjeta Transferencia. Se guarda en `config_pagos_integraciones.bank_instructions`. El campo `bank_alias` se mantiene intacto (se usa en checkout de customer app).
  - `supabase/functions/kapso-webhook/index.ts`: Refactor del for loop de restaurantes: hoistea `clienteRow` fuera del bloque `if (incomingText)` para que lo puedan reusar el review router (paso 1) y el nuevo bloque de transferencia (paso 2). Nuevo bloque: busca pedido con `metodo_pago ILIKE '%transfer%'` + `transfer_sent = false` + `created_at > NOW() - 4h`. Si lo encuentra y hay `bank_instructions` configurado: invoca `kapso-send` con `type: custom_text`, marca `transfer_sent = true`. Skip del welcome si se enviaron datos bancarios.
  - `supabase/migrations/20260501_transfer_sent.sql`: `ALTER TABLE pedidos ADD COLUMN IF NOT EXISTS transfer_sent boolean DEFAULT false`. Aplicada en producción via Management API.
- ✅ **kapso-webhook deploado** con `--no-verify-jwt`.
- ✅ **Build admin-react** ✓ sin errores.
- ✅ Push a main → Vercel deploando admin automáticamente.

### Pendiente

- ⏳ **Configurar bank_instructions** (Oscar): Settings > Operaciones > Transferencia → escribir el mensaje completo con nombre/RUT/cuenta/banco/email → guardar. Hasta que no se configure, el flujo no envía nada.
- ⏳ **QA flujo transferencia** (Oscar): hacer pedido de prueba con método pago "Transferencia" → enviar por WA → verificar que llega el mensaje con datos bancarios automáticamente (1 sola vez).
- ⏳ **QA producción admin — grupos modificadores** (Oscar, pendiente de sesión anterior): `admin.kitchat.cl` → Modificadores → grupos colapsados, editar grupo, agregar opción.
- ⏳ **QA customer app** (Oscar, pendiente): `?local=elpadrino` → pizza → 28 ingredientes; `?local=eltamborcito` → 3 grupos mayo.
- ⏳ **Webhook global MP Dashboard** (Oscar — CRÍTICO): MP Dashboard → Configuración → Notificaciones → `https://gjkaboosygjitxgqcawy.supabase.co/functions/v1/mp-webhook`
- ⏳ **Reemplazar `56XXXXXXXXX`** (5 puntos: `gracias/page.tsx` ×3, `BillingLapsedPage.jsx` ×1, `constants.ts` ×1)

### GOTCHAs

- **`bank_alias` vs `bank_instructions`**: `bank_alias` es el campo viejo (texto corto, se muestra en checkout de la customer app). `bank_instructions` es el nuevo campo (texto largo multiline, solo para WhatsApp). No confundir ni reemplazar uno con el otro.
- **Skip welcome si se enviaron datos bancarios**: decisión intencional — no tiene sentido enviar "aquí está el menú" cuando el cliente ya hizo el pedido. El restaurant puede desactivar el welcome desde Integraciones si quiere.
- **Ventana 4h**: si el pedido tiene más de 4 horas y el cliente escribe, NO se envían los datos de transferencia. Se asume que si pasaron 4h sin mensaje, el cliente siguió por otro canal. Se puede ajustar si el restaurante lo pide.
- **Errores IDE Deno en kapso-webhook**: el IDE marca errores en `Deno.env`, `Deno.serve`, y el import de `esm.sh`. Son pre-existentes — el IDE no tiene tipos Deno. El código corre correctamente en el runtime de Supabase Edge Functions.

---

---

## Sesión 2026-04-30 (noche) — Admin UI modificadores: CRUD grupos + colapsables + edición

### Tipo: 🔧 Técnico

### Completado

- ✅ **Verificación El Tamborcito** (`61a03ad8`): confirmado en mismo schema 3 niveles. 3 grupos globales, 21 adicionales todos con `grupo_id`. No requirió migración.
- ✅ **Commit `2061c70`**: UI modificadores — grupos colapsados por defecto, botón editar por opción (abre `ModifierModal`), KPI cards cuentan `modifiers` total (no solo flat), 3er card "En Grupos" con conteo real.
- ✅ **Commit `846175e`**: CRUD completo de grupos desde admin:
  - `GroupModal` nuevo: nombre, tipo radio/checkbox, min/max selección, scope (global/categoría/producto)
  - Botón "Nuevo Grupo" en barra de acciones
  - Botón editar (pencil) en header de cada grupo → abre `GroupModal`
  - Botón "Agregar opción al grupo" en pie de grupo expandido → `ModifierModal` con `grupoId` pre-asignado
  - `ModifierModal` acepta prop `grupoId` para crear opciones dentro de un grupo (oculta "Asignar a", incluye `grupo_id` en INSERT)
  - Eliminar grupo: hace `UPDATE adicionales SET grupo_id = NULL` (no DELETE) para preservar opciones huérfanas
- ✅ Ambos commits deploados a Vercel vía `main`.

### Pendiente

- ⏳ **QA producción admin** (Oscar): `admin.kitchat.cl` → Modificadores → verificar que grupos aparecen colapsados, botón editar grupo funciona, "Agregar opción" crea la opción correctamente dentro del grupo.
- ⏳ **QA customer app** (Oscar): `?local=elpadrino` → pizza → verificar 28 ingredientes igual. `?local=eltamborcito` → verificar 3 grupos mayo.
- ⏳ **Webhook global MP Dashboard** (Oscar — CRÍTICO): MP Dashboard → Configuración → Notificaciones → `https://gjkaboosygjitxgqcawy.supabase.co/functions/v1/mp-webhook`
- ⏳ **Reemplazar `56XXXXXXXXX`** (5 puntos: `gracias/page.tsx` ×3, `BillingLapsedPage.jsx` ×1, `constants.ts` ×1)

### GOTCHAs

- **`inGroup` flag en `ModifierModal`**: se calcula como `!!(modifier?.grupo_id || grupoId)`. Cubre tanto editar una opción existente de un grupo como crear una nueva opción en un grupo. Si solo se usara `modifier?.grupo_id`, el modal para nuevas opciones no ocultaría "Asignar a".
- **Eliminar grupo no borra opciones**: decisión intencional — se hace `UPDATE SET grupo_id = NULL` en lugar de DELETE. Las opciones quedan como modificadores huérfanos (visibles en el grid de flat modifiers). Alternativa sería borrarlas, pero se eligió preservar datos.
- **El Tamborcito 100% en sistema nuevo**: todos sus 21 adicionales tienen `grupo_id`. No existe ningún adicional flat en ese restaurante. Si se agregara un adicional flat accidentalmente, aparecería en todos los productos (scope global por default).

---

---

## Sesión 2026-04-30 (tarde) — Sistema escalable de grupos modificadores + migración El Padrino

### Tipo: 🔧 Técnico

### Completado

- ✅ **Commit `40d8b07`**: grupos modificadores globales (`producto_id` nullable). CustomerApp filtra por `producto_id === null`, admin muestra sección "Grupos Globales".
- ✅ **Commit `dae4229`**: sistema 3 niveles de scope — `categoria_id` en `grupos_modificadores`. El scoping ahora es:
  - `producto_id = UUID` → 1 producto específico
  - `producto_id = NULL + categoria_id = UUID` → todos los productos de esa categoría
  - `producto_id = NULL + categoria_id = NULL` → todos los productos del restaurante
- ✅ **Schema DB**: `ALTER TABLE grupos_modificadores ADD COLUMN categoria_id uuid REFERENCES categorias(id)` + índice. Aplicado en producción via Management API.
- ✅ **customer-app ProductModal.tsx**: filtro 3 niveles implementado.
- ✅ **TypeScript**: `database.types.ts`, `store.ts`, `useStore.ts` actualizados. `tsc --noEmit` = 0 errores.
- ✅ **Admin ModifiersTab.jsx**: badge "Solo [Categoría]" o "Todos los productos" por grupo. Título cambiado a "Grupos de Modificadores".
- ✅ **El Padrino migrado**: 1 grupo "Ingredientes adicionales" con `categoria_id = Pizza` + 28 extras migrados (grupo_id seteado, categoria_id limpiado). `opciones_precio` (Individual/Mediana/Grande) intactos. Red bull queda como extra plano global.
- ✅ **El Tamborcito** (`61a03ad8`): 3 grupos globales (mayo libre radio + mayo extra checkbox + extras opcionales) — creados en sesión anterior, deploados ahora.
- ✅ **Push a main**: 2 commits deploados a Vercel.

### Pendiente

- ⏳ **QA producción El Padrino** (Oscar): `?local=elpadrino` → cualquier pizza → verificar que aparecen los 28 ingredientes igual que antes. Hard refresh si hay caché PWA.
- ⏳ **QA producción El Tamborcito** (Oscar): `?local=eltamborcito` → cualquier producto → verificar 3 grupos de mayo visibles.
- ⏳ **QA admin** (Oscar): `admin.kitchat.cl` → Menú → Modificadores → verificar badge "Solo Pizza" en El Padrino y grupos de mayo en El Tamborcito.
- ⏳ **Webhook global MP Dashboard** (Oscar — crítico): MP Dashboard → Configuración → Notificaciones → `https://gjkaboosygjitxgqcawy.supabase.co/functions/v1/mp-webhook`
- ⏳ **Reemplazar `56XXXXXXXXX`** (5 puntos: `gracias/page.tsx` ×3, `BillingLapsedPage.jsx` ×1, `constants.ts` ×1)

### GOTCHAs

- **Vite 7 + Node 24 incompatibilidad**: dev server arranca, TCP conecta, pero HTTP nunca responde. Workaround: `npm run build` local + deploy Vercel para QA. No bloquea producción.
- **PWA caché**: customer-app tiene service worker. Si el usuario vio la app antes del deploy, verá versión vieja hasta hard refresh (`Cmd+Shift+R`) o unregister del SW en DevTools.
- **`categoria_id` en `useStore.ts` requiere cast**: el tipo `GrupoRow` de database.types.ts no se propaga automáticamente al mapping, se usa `(g as unknown as { categoria_id?: string | null }).categoria_id ?? null`.
- **Extras en grupos NO deben tener `categoria_id`**: el scoping lo maneja el grupo. Si un extra tiene `grupo_id`, su `categoria_id` debe ser NULL (el grupo define el alcance). El Padrino quedó correcto.
- **Red bull** de El Padrino: extra plano sin grupo, sin categoría. Aparece en todos los productos. Es un outlier intencional.

---

## Sesión 2026-04-30 (mañana) — Grupos globales de modificadores (hamburguesería `61a03ad8`)

---

## Sesión 2026-04-30 — Grupos globales de modificadores (hamburguesería `61a03ad8`)

### Tipo: 🔧 Técnico — schema migration + data cleanup + código customer-app + admin

### Contexto
Restaurante `61a03ad8-3e3e-45cc-851b-071c061c346d` (hamburguesería) había cargado 1.827 adicionales y 249 grupos el 2026-04-29, todos duplicados por producto. El problema: desactivar "Merkén" requería 97 updates individuales.

### Completado

- ✅ **Migración schema**: `grupos_modificadores.producto_id` ahora es nullable (`DROP NOT NULL`). Grupos con `producto_id = NULL` aplican a todos los productos del restaurante. Migración: `supabase/migrations/20260430_grupos_modificadores_global.sql`
- ✅ **Data cleanup**: borrados 249 grupos y 1.827 adicionales duplicados del 2026-04-29 para `61a03ad8`.
- ✅ **3 grupos globales insertados** (`producto_id = NULL`):
  - "Elige tu mayonesa" (radio, min=1, max=1) — 8 sabores a $0
  - "Mayonesa adicional" (checkbox, min=0, max=7) — 8 sabores a $500
  - "Extras opcionales" (checkbox, min=0, max=5) — Huevo $600, Tomate $1000, Queso $2000, Palta $2500, Pollo $2500
- ✅ **customer-app `ProductModal.tsx`** — filtro actualizado: `.filter(g => g.producto_id === product.id || g.producto_id === null)`. Incluye grupos globales en todos los productos.
- ✅ **TypeScript types** — `database.types.ts` y `signals/store.ts`: `GrupoModificador.producto_id: string → string | null`
- ✅ **Admin `ModifiersTab.jsx`** — nueva sección "Grupos Globales" arriba del grid de modificadores planos. Muestra grupos con `producto_id IS NULL`, lista sus opciones, toggle disponible/agotado por opción (1 click desactiva "Merkén" globalmente).
- ✅ **Build customer-app**: 0 errores TypeScript. `tsc --noEmit` limpio.

### Pendiente

- ⏳ **Deploy Vercel** (Oscar): commit + push de `customer-app` y `admin-react`. Dev server local en `localhost:5174` para QA previo.
- ⏳ **Confirmar build admin-react en producción**: el build local tuvo problemas de procesos múltiples pero el código TypeScript es válido.
- ⏳ **Webhook global MP Dashboard** (crítico, de sesión anterior)
- ⏳ **Reemplazar `56XXXXXXXXX`** (5 puntos)

### GOTCHAs

- **CTE PostgreSQL con múltiples INSERTs + UNION ALL requiere casts explícitos**: `::uuid` y `::text` necesarios cuando se combinan INSERTs en CTEs — Postgres no infiere tipos en UNION ALL de subqueries de CTE.
- **Builds múltiples de Vite se cuelgan**: lanzar varios `vite build` en background simultáneamente deja procesos zombi. Matar por PID antes de reiniciar: `kill <pids>`.
- **`grupos_modificadores` tiene FK a `productos`**: al hacer `DROP NOT NULL`, la FK sigue activa (NULL es válido en FK). Los grupos globales con `producto_id = NULL` no violan la FK.
- **Admin ModifiersTab solo muestra adicionales sin `grupo_id`**: las opciones de grupos (con `grupo_id` seteado) no aparecían antes. La nueva sección "Grupos Globales" es la única forma de gestionarlos desde el admin.

---

## Sesión 2026-04-28 (sesión 17) — Primer pago real + debugging env vars Vercel + ADMIN_URL fix

### Tipo: 🔧 Técnico — debugging producción, primer cliente real

### Completado

- ✅ **Primer pago real recibido**: "Fuente de soda el Tamborcito" (`waldo_cc@hotmail.com`) pagó $59.381 CLP — `preapproval status: authorized`, `charged_quantity: 1`.
- ✅ **Diagnóstico webhook**: MP no envió webhook a `mp-webhook` — logs de edge functions muestran cero llamadas. Causa: webhook global de MP Dashboard no configurado. El `notification_url` del preapproval API no es confiable en Chile para suscripciones.
- ✅ **Rescue manual**: `UPDATE pending_signups SET status='paid', paid_at='2026-04-28T19:09:39Z'` → cliente pudo continuar con el link `/gracias?ref=pendsub_ba7d6b7d-02ae-4f72-9573-db1e41bb5307`.
- ✅ **Bug env vars Vercel encontrado**: bundle de producción tenía `NEXT_PUBLIC_SUPABASE_URL` con `\n` trailing + `NEXT_PUBLIC_SUPABASE_ANON_KEY` era la key pre-rotación (iat: marzo 2025). Ambas causaban polling silencioso en `/gracias`. Oscar corrigió en Vercel Dashboard.
- ✅ **`ADMIN_URL` secret corregido**: estaba en `http://localhost:3000` → `https://admin.kitchat.cl` via `supabase secrets set ADMIN_URL=https://admin.kitchat.cl`.
- ✅ **Cliente creado exitosamente**: `pending_signups.status='done'`, restaurante `fuente-de-soda-el-tamborcito-cdgb` creado, `suscripciones.estado='active'`.

### Pendiente

- ⏳ **Webhook global MP Dashboard** (Oscar): ir a MP Dashboard → Tu negocio → Configuración → Notificaciones → URL `https://gjkaboosygjitxgqcawy.supabase.co/functions/v1/mp-webhook` + eventos `subscription_preapproval` + `payment`. Sin esto, cada pago requiere rescue manual.
- ⏳ **Reemplazar `56XXXXXXXXX`** (5 puntos: `gracias/page.tsx` ×3, `BillingLapsedPage.jsx` ×1, `constants.ts` ×1)
- ⏳ **Test flujo anual E2E**

### GOTCHAs nuevos

- **MP `notification_url` no confiable para suscripciones Chile**: El campo se manda en el preapproval API pero MP no lo usa para disparar webhooks de suscripción recurrente. Webhook global del Dashboard es el único mecanismo confiable.
- **Env vars Vercel con `\n` trailing**: Si se copia-pega una env var con salto de línea al final, Next.js compila ese `\n` en el bundle. El Supabase client recibe una URL con newline → todas las requests fallan silenciosamente (error capturado en polling como `if (fetchErr || !data) return`).
- **Anon key vieja en Vercel**: La key `iat:1743128339` (marzo 2025) fue revocada al rotar. Retorna 401 silencioso. Verificar siempre con `get_publishable_keys` MCP y comparar `iat` de la key en producción con la key actual.
- **`ADMIN_URL` secret debe ser prod antes de primer pago**: Este secret controla el `redirect_to` del magic link post-finalize. Si apunta a localhost, el cliente queda con un token válido pero URL rota.
- **Rescue manual via SQL + link directo funciona**: Si el webhook falla, hacer `UPDATE pending_signups SET status='paid'` y enviar `/gracias?ref=XXX` al cliente. El `status='paid'` persiste y el link no expira hasta `expires_at` (24h desde creación).

---

## Sesión 2026-04-28 (sesión 16) — Commit edge functions al repo

### Completado

- ✅ **Commit `83b36cb`** pusheado a `creactive-dev/white-cassini`: `mp-checkout-create` (flujo anual + fix supabaseUrl2), `mp-webhook` (match anual por email+monto), `_shared/mercadopago.ts` (dual-mode HMAC).

---

## Sesión 2026-04-28 (sesión 15) — Fix crítico supabaseUrl2 + MP_ACCESS_TOKEN restaurado

### Tipo: 🔧 Técnico — debugging producción

### Completado

- ✅ **Bug `supabaseUrl2` corregido**: Al agregar el flujo anual en sesión 13, se eliminó la variable `supabaseUrl2` pero quedó referencia en línea 136 de `mp-checkout-create/index.ts` (`notification_url: \`${supabaseUrl2}/functions/v1/mp-webhook\``). Causaba `ReferenceError` silencioso capturado por try/catch → mensaje genérico "Error al crear el link de pago". Fix: `supabaseUrl2` → `supabaseUrl`. Redeployado.
- ✅ **`MP_ACCESS_TOKEN` restaurado**: El secret había sido sobreescrito con un hex string (`ba39061f...`) inválido como token MP. Restaurado via Supabase CLI: `supabase secrets set MP_ACCESS_TOKEN=APP_USR-184406752567367-042712-5c80c789676f7c36ca9ee747a54f9b05-3362466707`.
- ✅ **Checkout verificado**: curl test retorna `init_point` válido de MP ✅

### Pendiente

- ⏳ **Commitear edge functions** al repo `creactive-dev/white-cassini`: `mp-checkout-create/index.ts` (fix supabaseUrl2 + flujo anual), `mp-webhook/index.ts` (match anual), `_shared/mercadopago.ts`
- ⏳ **Reemplazar `56XXXXXXXXX`** (5 puntos: `gracias/page.tsx` ×3, `BillingLapsedPage.jsx` ×1, `constants.ts` ×1)
- ⏳ **Test flujo anual E2E**
- ⏳ **Primer pago real de cliente**

### GOTCHAs nuevos

- **Variable eliminada pero referenciada**: Al refactorizar (renombrar `supabaseUrl2` → `ANNUAL_PAYMENT_LINK`), una referencia al nombre viejo quedó en el código. Deno lanza `ReferenceError` en runtime que el try/catch captura → se ve como "Error al crear el link de pago", no como error de variable. Difícil de debuggear sin logs. Siempre buscar `grep supabaseUrl2` después de renombrar variables.
- **Supabase secrets via Management API REST no actualizaba**: `POST /v1/projects/{ref}/secrets` retornó vacío pero el valor no cambió. Usar CLI: `supabase secrets set NAME=VALUE --project-ref {ref}`.
- **Secret `MP_ACCESS_TOKEN` sobreescrito misteriosamente**: Llegó a ser `ba39061fd22a78eb7d1cb3045e3572798ee7c636ccbdbf960c405ebb9a17c339` (hex). Origen desconocido — posible confusión manual con `MP_WEBHOOK_SECRET`. Guardar el Access Token en lugar seguro y verificar con `curl api.mercadopago.com/v1/payment_methods` antes de asumir que es válido.

---

## Sesión 2026-04-27 (sesión 13) — Fix precio stale + flujo anual + CTA navbar

### Tipo: 🔧 Técnico

### Completado

- ✅ **Fix precio stale en checkout**: `mp-checkout-create` tenía bloque de rate limiting que reutilizaba `mp_init_point` guardado (precio $49.900 antiguo). Eliminado el bloque completo — ahora siempre crea preapproval fresco. Registros stale borrados de `pending_signups`.
- ✅ **CTA navbar**: "Probar gratis" → "Empezar ahora". Commit `cb1639b`.
- ✅ **Migration DB**: `ALTER TABLE pending_signups ADD COLUMN billing_type text NOT NULL DEFAULT 'monthly' CHECK IN ('monthly','annual')`.
- ✅ **Flujo anual completo**: `mp-checkout-create` acepta `billing_type='annual'` → guarda `pending_signup` con email/nombre/billing_type → retorna link MP estático sin llamar a API de MP. Commit `1b81fbb`.
- ✅ **`mp-webhook` anual**: `handlePayment` ahora matchea por `payer.email + transaction_amount >= 593000` → marca `pending_signup` como `paid`. Sin `external_reference` (link estático no lo tiene).
- ✅ **`Pricing.tsx`**: CTA "Pagar año completo" → `/suscribirse?billing=annual` (antes iba directo al link de MP sin recolectar datos).
- ✅ **`/suscribirse`**: muestra pricing anual ($593.810 IVA incl. + "2 meses gratis") cuando `?billing=annual`.
- ✅ **Edge functions redeployadas**: `mp-checkout-create` + `mp-webhook`.

### Pendiente

- ⏳ **Commit cambios mp-webhook + _shared/mercadopago.ts + mp-checkout-create** al repo `creactive-dev/white-cassini` (deployados en Supabase pero no en git)
- ⏳ **Reemplazar `56XXXXXXXXX`** en `app/gracias/page.tsx` (3 ocurrencias) y `admin-react/src/pages/BillingLapsedPage.jsx`
- ⏳ **Test flujo anual end-to-end**: form → link MP → payment webhook → `status='paid'`
- ⏳ **Primer pago real de cliente**

### GOTCHAs nuevos

- **Rate limiting de init_point causa precio stale**: si el mismo email tiene un `pending_signup` vigente, la función retorna el `init_point` guardado (con precio antiguo). No usar caching de `init_point` — siempre crear preapproval fresco.
- **Link estático MP no acepta `back_url`/`external_reference`**: el matching de pago anual usa `payer.email + amount >= 593000`. Si el usuario paga con un email diferente al que ingresó en el form, el match falla y el signup queda en `pending`. Gestionar manualmente en ese caso.
- **Account creation anual es manual**: cuando `pending_signups.billing_type='annual' AND status='paid'` → Oscar crea cuenta con INSERT en `restaurantes` + `suscripciones` (current_period_end = now() + 365 days).

---

## Sesión 2026-04-27 (sesión 12) — MP_ACCESS_TOKEN correcto + pricing IVA + Vercel build fixes

### Tipo: 🔧 Técnico — debugging producción + configuración billing final

### Completado

- ✅ **MP_ACCESS_TOKEN correcto**: El token guardado era la Public Key (UUID corto `APP_USR-6c9fac5a-...`), no el Access Token. Access Token correcto: `APP_USR-184406752567367-042712-5c80c789676f7c36ca9ee747a54f9b05-3362466707`. Secret actualizado en Supabase.
- ✅ **`planes.precio_clp` = 59381** (antes 49900): MP cobra $49.900 + IVA = $59.381. DB actualizada via SQL.
- ✅ **Pricing landing actualizado**:
  - Mensual: `$49.900 + IVA /mes` (precio neto en display)
  - Anual: `$593.810/año` IVA incluido → link directo `https://mpago.li/2Pzv3FE` (no suscripción)
  - 4 archivos actualizados: `constants.ts`, `Pricing.tsx`, `NoCommissions.tsx`, `suscribirse/page.tsx`
- ✅ **Vercel build fixes** (3 errores consecutivos resueltos):
  1. `supabaseUrl is required` → `lib/supabase.ts` usa fallback placeholder
  2. `useSearchParams()` needs Suspense → ambas páginas refactorizadas con patrón `XxxContent + Suspense`
  3. Build Vercel pasa limpio ✅
- ✅ **`mp-checkout-create` debugeado**: error 502 → causa: token incorrecto. Redesplegado v10 limpio.

### Pendiente

- ⏳ **Commit cambios mp-webhook + _shared/mercadopago.ts** al repo `creactive-dev/white-cassini` (deployados en Supabase pero no en git — viene de sesión 11)
- ⏳ **Reemplazar `56XXXXXXXXX`** en `app/gracias/page.tsx` (3 ocurrencias) y `admin-react/src/pages/BillingLapsedPage.jsx` (1 ocurrencia)
- ⏳ **Test primer pago real** — happy path completo en producción

### GOTCHAs nuevos

- **Public Key ≠ Access Token en MP**: La Public Key (`APP_USR-<UUID>`) es el ID de la aplicación. El Access Token es mucho más largo (`APP_USR-{números}-{fecha}-{hash}-{cuentaId}`). Verificar siempre con `curl` antes de guardar en secretos.
- **Precio con IVA**: Chile 19% IVA. $49.900 neto → $59.381 con IVA. Display en landing: precio neto. Cobro MP: precio con IVA. Plan anual: link de pago fijo (no suscripción), $593.810 IVA incl.

---

## Sesión 2026-04-27 (sesión 11) — Secrets producción + webhook HMAC fix

### Tipo: 🔧 Técnico — configuración final de producción + debugging HMAC

### Completado

- ✅ **`MP_ACCESS_TOKEN` → producción**: Secret actualizado de `TEST-184406752567367-...` a `APP_USR-6c9fac5a-24f2-4db7-89fe-59040f047707`. El flujo de pago real ya usa credenciales de producción.
- ✅ **`MP_WEBHOOK_SECRET` configurado**: Secret HMAC real de MP Dashboard: `6bd327cebd26bb72e2387cbff3967a173225785ba48778c14096b63e48443efb`.
- ✅ **`mp-webhook` — 200-always pattern**: El webhook ahora retorna 200 para TODOS los requests, incluyendo los con HMAC inválido. Eventos inválidos se ignoran internamente (log + return early) pero nunca retornan 4xx. Esto evita retry storms de MP y es el patrón estándar de la industria.
- ✅ **Dual-mode HMAC en `_shared/mercadopago.ts`**: `verifyWebhookSignature` intenta primero el secret como UTF-8, luego como hex-decodificado. Cubre todos los formatos posibles de MP.
- ✅ **Simulator de MP Dashboard devuelve 200**: Ambos tipos de evento (`payment` y `subscription_preapproval`) responden 200. El HMAC del simulator es diferente al de producción (comportamiento esperado de MP) — el 200-always lo maneja correctamente.
- ✅ **Bug fix en x-signature parsing**: El parser original usaba `chunk.split("=")` — perdía caracteres en el `v1` si el HMAC hex contenía `=`. Fix: `chunk.indexOf("=")` + `slice(idx + 1)`.
- ⚠️ **PENDIENTE COMMIT**: Los cambios en `mp-webhook/index.ts` y `_shared/mercadopago.ts` están deployados en Supabase pero NO commiteados al repo `creactive-dev/white-cassini`. Commitear antes de cambios futuros.

### Pendiente de producción

- ⏳ **Commit cambios mp-webhook** al repo `creactive-dev/white-cassini` (archivos modificados: `supabase/functions/mp-webhook/index.ts` + `supabase/functions/_shared/mercadopago.ts`)
- ⏳ **Reemplazar `56XXXXXXXXX`** en `/gracias/page.tsx` y `BillingLapsedPage.jsx` con número real de WA Kitchat
- ⏳ **Test con primer pago real** — happy path completo landing → MP → /gracias → admin

### GOTCHAs nuevos (esta sesión)

- **MP Dashboard simulator ≠ producción**: El botón "Simular notificación" de MP Dashboard firma con un secret interno diferente al configurado en la UI. Es comportamiento documentado de MP. No esperar que el simulator pase HMAC — usar 200-always pattern y validar solo con webhooks reales.
- **200-always es la seguridad correcta para webhooks**: Aunque el HMAC falle, el evento se ignora (no se procesa). La seguridad real está en que `handlePreapproval`/`handlePayment` llaman a la API de MP para verificar el estado antes de modificar la DB. Retornar 4xx a MP solo causa retries innecesarios.
- **Logs de Supabase Edge Functions no muestran `console.log`**: El endpoint de logs de la Management API solo retorna logs HTTP (status, method, time). Para debugging real, testear con `curl` local con HMAC computado en Python: `hmac.new(secret.encode(), template.encode(), hashlib.sha256).hexdigest()`.
- **`verifyWebhookSignatureDebug`** está en `_shared/mercadopago.ts` (sin usar desde index.ts). Útil para debugging futuro — no eliminar.
- **x-signature parsing bug**: El split original `chunk.split("=")` era incorrecto — el HMAC hex en `v1` puede contener `=`. El fix (indexOf + slice) ya está en producción.

---

## Sesión 2026-04-27 (sesión 9) — QA E2E billing + fixes

### Tipo: 🔧 Técnico — debugging y validación del flujo completo de suscripciones

### Completado

- ✅ **Anon key rotada corregida**: La key en `.env.local` (landing + admin) era la vieja (iat:1743116166). Nueva key válida: termina en `noAous5ynUpvg0l2ko9LbnUM6z_8qPAnl6xRGk9GkNw`. Ambos `.env.local` actualizados.
- ✅ **CORS fix en `signup-finalize`**: Mismo bug que `mp-checkout-create` — solo permitía `localhost:3000`. Fix: `origin?.startsWith("http://localhost:")`. Redeploy exitoso.
- ✅ **`ADMIN_URL` secret actualizado a `http://localhost:5174`** para QA local (antes apuntaba a `:3000`).
- ✅ **`signup-finalize` bypasa onboarding**: `onboarding_status: "pendiente"` → `"completado"`. Nuevos clientes llegan directo al dashboard. CreActive hace el onboarding manualmente.
- ✅ **Redirect cambiado**: `/onboarding` → raíz del admin (`adminUrl`).
- ✅ **QA E2E validado**: `/gracias?ref=...` → polling detecta `paid` → form contraseña → `signup-finalize` → usuario + restaurante + suscripción creados → redirect a `localhost:5174` con sesión activa.
- ✅ **TEST token MP verificado**: `TEST-184406752567367-042712-2265e9a7847561f79c921454dcc9d036-3362466707`. Supabase secret `MP_ACCESS_TOKEN` actualizado.
- ✅ **`ADMIN_URL` secret** → `https://admin.kitchat.cl` (producción). ✅
- ✅ **Commit landing** `5d0cd6e` — `/suscribirse` + `/gracias` + `lib/supabase.ts` + `package.json`. Pusheado a `creactive-dev/kitchat`.
- ✅ **Commit white-cassini** `b85945e` — 4 edge functions billing + 2 migraciones + admin gate + docs. Pusheado a `creactive-dev/white-cassini`.

### Pendiente antes de que el flujo funcione en producción (🔴 bloqueante)

- ⏳ **Vercel env vars landing** (sin esto la landing no conecta a Supabase en prod):
  - `NEXT_PUBLIC_SUPABASE_URL=https://gjkaboosygjitxgqcawy.supabase.co`
  - `NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...noAous5ynUpvg0l2ko9LbnUM6z_8qPAnl6xRGk9GkNw`
  - `NEXT_PUBLIC_ADMIN_URL=https://admin.kitchat.cl`
- ⏳ **Cambiar `MP_ACCESS_TOKEN` secret** de `TEST-...` → `APP_USR-...` (token de producción) — sin esto los pagos son en sandbox
- ⏳ **Configurar webhook en MP Dashboard**: URL `https://gjkaboosygjitxgqcawy.supabase.co/functions/v1/mp-webhook`, eventos `subscription_preapproval` + `payment`
- ⏳ **Actualizar `NEXT_PUBLIC_ADMIN_URL`** en `.env.local` de la landing a `https://admin.kitchat.cl` para producción
- ⏳ **Reemplazar `56XXXXXXXXX`** en `/gracias/page.tsx` y `BillingLapsedPage.jsx` con número real de WA Kitchat
- ⏳ **Deploy landing** a Vercel con env vars de producción
- ⏳ **Test webhook en producción** con un pago real (primer cliente o test con tarjeta real)

### GOTCHAs nuevos (esta sesión)

- **Supabase anon key rotada**: El proyecto tiene una nueva anon key desde ~enero 2026 (iat:1769040475). La key vieja (iat:1743116166) retorna "Invalid API key" en REST. Siempre verificar con Management API: `GET /v1/projects/{ref}/api-keys`.
- **MP Chile sandbox incompatible para suscripciones**: Las cuentas reales (collector) no pueden tener test buyers como payers — error "Both payer and collector must be real or test users". El sandbox de MP Chile para subscriptions recurrentes requiere cuentas 100% de prueba en ambos lados, lo que no aplica a cuentas de producción que usan TEST token. Solución práctica: simular webhook vía DB directamente para QA backend.
- **Orphan users en tests**: Si `signup-finalize` crea auth.users pero falla en INSERT restaurante o suscripcion, el email queda bloqueado para nuevos intentos. Para tests, usar email fresco con timestamp (`qa-$(date +%s)@...`).
- **`suscripciones.mp_preapproval_id` es UNIQUE**: Cada test de QA necesita un `mp_preapproval_id` distinto. Usar timestamp en el valor de prueba.
- **`ADMIN_URL` secret requiere reset antes de producción**: Quedó en `http://localhost:5174` para el QA. Cambiar a `https://admin.kitchat.cl` antes del deploy.
- **`signup-finalize` también tenía CORS bug**: Además de `mp-checkout-create`, esta función también tenía `localhost:3000` hardcodeado. Verificar `mp-webhook` por el mismo patrón si se testea desde localhost.

---

## Sesión 2026-04-27 (sesión 8) — Setup MP + QA prep

### Tipo: 🔧 Técnico — ejecución completa del mp-setup.md

### Completado

- ✅ Migración A1 aplicada: tablas `planes`, `suscripciones`, `pending_signups`, `mp_eventos` + cols `signup_email`, `is_demo` en `restaurantes`
- ✅ Migración A2 aplicada: backfill legacy (+ bug fix: slug era `elpadrino` en SQL, corregido a `el-padrino`)
- ✅ El Padrino: `estado='active'`, `current_period_end=2027-04-27`
- ✅ Soli Sushi, El Charakato, Hillfood: `is_demo=true`, `estado='demo'`
- ✅ Plan Pro: `mp_preapproval_plan_id=NULL` (limpiado — el plan de MP era tipo pago directo, incorrecto para checkout)
- ✅ 4 secrets Supabase configurados: `MP_ACCESS_TOKEN` (TEST), `MP_WEBHOOK_SECRET`, `LANDING_URL`, `ADMIN_URL`
- ✅ 3 edge functions deployadas: `mp-checkout-create`, `mp-webhook`, `signup-finalize`
- ✅ Smoke test `mp-checkout-create`: genera `init_point` + crea `pending_signup` en DB
- ✅ CORS fix `mp-checkout-create`: permite cualquier `localhost:*` (antes solo `:3000`)
- ✅ `.env.local` creados: landing (`NEXT_PUBLIC_*`) + admin (`VITE_*`)
- ✅ Dev servers corriendo: landing en `:3003`, admin en `:5174`

### Pendiente
- ⏳ QA E2E sandbox: pagar con tarjeta de prueba MP → webhook → /gracias polling → signup-finalize → onboarding
- ⏳ Reemplazar `56XXXXXXXXX` con número real de WA Kitchat en `/gracias/page.tsx` y `BillingLapsedPage.jsx`
- ⏳ Switch a producción: cambiar `MP_ACCESS_TOKEN` a `APP_USR-...` + verificar webhook en MP Dashboard

### GOTCHAs nuevos (esta sesión)

- **Slug El Padrino:** en DB es `el-padrino`, no `elpadrino`. La migración A2 tenía el slug incorrecto — se corrigió el archivo SQL y se aplicó manualmente.
- **Plan MP tipo "pago directo":** el plan `811fb108e6c94bc6bc203c1b2eefec4b` de MP Dashboard requiere `card_token_id` (pago directo), no genera `init_point`. Incompatible con nuestro checkout flow. Limpiar `mp_preapproval_plan_id=NULL` es la solución — la función funciona sin él.
- **MP sandbox rechaza `@example.com`:** error "Cannot operate between different countries" era por email con dominio falso. Con email real (cualquier dominio válido) funciona.
- **CORS de edge functions:** `mp-checkout-create` tenía `localhost:3000` hardcodeado. Next.js puede arrancar en cualquier puerto libre. Fix: `origin?.startsWith("http://localhost:")` en lugar de lista fija.
- **4 servidores Next.js simultáneos:** causan lentitud extrema + error `ECANCELED: operation canceled, read` en framer-motion. Transitorio — se resuelve en el siguiente request.
- **Dev server landing:** arrancó en `:3003` (`:3000`, `:3001`, `:3002` ocupados). Confirmar puerto real antes de intentar abrir.

---

## Sesión 2026-04-27 — Billing Mercado Pago completo

### Tipo: 🔧 Técnico — flujo de suscripciones MP end-to-end

### Decisiones clave
- **Plan único MVP:** Pro a $49.900/mes CLP (Starter no existe)
- **Cobro día 1:** sin trial
- **El Padrino:** plan Pro activo, `current_period_end = now() + 365 days`
- **Demos (Soli Sushi, El Charakato, Hillfood):** `estado = 'demo'`, `is_demo = true` en restaurantes — bypass total del billing gate
- **Thank-you page:** vive en la landing Next.js (pública), no en admin
- **Idempotencia:** tabla `mp_eventos` con `event_id UNIQUE` — mejora sobre Nutrisco que no tenía tabla de eventos

### Archivos creados (código pendiente de deploy)

**Migraciones SQL:**
- `supabase/migrations/20260427_billing_subscriptions.sql` — tablas `planes`, `suscripciones`, `pending_signups`, `mp_eventos` + columnas `signup_email` + `is_demo` en `restaurantes` + RLS + seed plan Pro
- `supabase/migrations/20260427_seed_legacy_subscriptions.sql` — El Padrino → activo 365 días; demos → `is_demo=true` + `estado='demo'`

**Edge Functions (todas con `--no-verify-jwt`):**
- `supabase/functions/_shared/mercadopago.ts` — cliente REST compartido: `createPreapproval`, `getPreapproval`, `getPayment`, `verifyWebhookSignature` (HMAC-SHA256), `mpStatusToKitchat`
- `supabase/functions/mp-checkout-create/index.ts` — POST `{plan_id, email, nombre_local}` → `{init_point, external_reference}`. Reutiliza pending si existe dentro de 24h. CORS: kitchat.cl + localhost:3000
- `supabase/functions/mp-webhook/index.ts` — valida HMAC, idempotencia via `mp_eventos ON CONFLICT DO NOTHING`, maneja `subscription_preapproval` y `payment`
- `supabase/functions/signup-finalize/index.ts` — POST `{external_reference, password}` → crea auth.users + restaurante + suscripcion + UPDATE pending → done. Genera magic link para auto-login

**Landing (Next.js):**
- `clientes/kitcha/outputs/kitcha-landing/lib/supabase.ts` — cliente Supabase + `functionsUrl`
- `clientes/kitcha/outputs/kitcha-landing/app/suscribirse/page.tsx` — form email + nombre_local → MP checkout
- `clientes/kitcha/outputs/kitcha-landing/app/gracias/page.tsx` — polling `pending_signups` 2s/90s, 5 estados UI (waiting/paid/done/timeout/expired/failed), form password post-pago

**Admin:**
- `admin-react/src/pages/BillingLapsedPage.jsx` — gate para suscripciones canceladas/pausadas: reactivar → MP checkout
- `admin-react/src/context/DataContext.jsx` — carga `suscripciones` en `loadData()`, expone `subscription` en contexto
- `admin-react/src/App.jsx` — gate de suscripción post-onboarding: canceled/paused (y no is_demo) → `/billing/lapsed`

**Docs:**
- `docs/mp-setup.md` — guía completa: migraciones, config MP Dashboard, secrets Supabase, deploy commands, tarjetas de prueba sandbox, secuencia smoke tests, switch a producción

### Pendiente manual antes de QA

1. Aplicar migración A1 (`20260427_billing_subscriptions.sql`) vía Management API — verificar 4 tablas creadas
2. Aplicar migración A2 (`20260427_seed_legacy_subscriptions.sql`) — verificar legacy
3. Configurar MP Dashboard: webhook URL `https://gjkaboosygjitxgqcawy.supabase.co/functions/v1/mp-webhook` + eventos `subscription_preapproval` + `payment` + copiar `MP_WEBHOOK_SECRET`
4. Supabase Edge Functions → Secrets: `MP_ACCESS_TOKEN`, `MP_WEBHOOK_SECRET`, `LANDING_URL=https://kitchat.cl`, `ADMIN_URL=https://admin.kitchat.cl`
5. Deploy 3 edge functions: `mp-checkout-create`, `mp-webhook`, `signup-finalize` (todas con `--no-verify-jwt`)
6. `.env.local` en `kitcha-landing`: `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `NEXT_PUBLIC_ADMIN_URL`
7. Verificar `admin-react` tiene `VITE_SUPABASE_URL` + `VITE_SUPABASE_ANON_KEY` en su `.env.local`
8. Reemplazar `56XXXXXXXXX` con número real de WA Kitchat en `/gracias/page.tsx` y `BillingLapsedPage.jsx`
9. E2E sandbox QA con tarjetas de prueba MP (ver `docs/mp-setup.md §8`)
10. Switch a prod: cambiar `MP_ACCESS_TOKEN` a `APP_USR-...`

### GOTCHAs nuevos

- **`supabase.supabaseUrl` no existe en Supabase v2:** El cliente JS v2 no expone `.supabaseUrl`. En `BillingLapsedPage.jsx` usar `import.meta.env.VITE_SUPABASE_URL` directamente.
- **`stableEventId` sin timestamp:** Para idempotencia real, el `event_id` de `mp_eventos` es `type + ':' + dataId` (sin timestamp). Con timestamp, el mismo evento retryado genera un ID diferente y se procesa dos veces.
- **Cuenta MP:** Hoy usa la cuenta de CreActive Studio. Pendiente: conectar cuenta MP real del cliente Kitchat (El Padrino / Oscar como cliente final).
- **Orphan auth users:** Si `signup-finalize` crea el user en Auth pero falla el INSERT en `restaurantes`, queda un user huérfano. `pending_signups` se mantiene en `status='paid'` — el usuario puede reintentar. Cleanup: cron diario (deuda técnica documentada).

---

## Estado: EN PRODUCCIÓN — Review IA pipeline completamente operativo y validado en múltiples pruebas E2E reales. main en sync con origin. kapso-webhook v23 + review-classifier v5.

## Impresión de comandas (2026-04-23) — PENDIENTE EJECUTAR

Análisis AS IS + arquitectura documentada en `docs/impresion-comandas-plan.md`.

**AS IS:** 0% implementado. Cero código de impresión.

**Hardware El Padrino listo:** Epson TM-T88IV M129h Ethernet (raw TCP :9100, ESC/POS). No soporta CloudPRNT ni ePOS-Print nativo.

**Arquitectura elegida:** Print agent Node.js local (Raspberry Pi Zero 2 W o cualquier PC) suscrito a Supabase Realtime filtrando por `restaurante_id`. Config por tenant en `config_operaciones.print_config`. Stack: `node-thermal-printer` + `@supabase/supabase-js`. Costo por restaurante: $0 (si tiene PC encendido) o ~$25 USD (Pi).

**Fases:** Fase 0 prototipo El Padrino (8-12h) → Fase 1 multi-tenant + Settings UI (8-12h) → Fase 2 imagen Pi + auditoría (6-10h).

**5 decisiones pendientes de Oscar antes de ejecutar:** (1) go/no-go Fase 0, (2) hardware default Pi vs PC, (3) cuándo imprimir (INSERT vs `preparando`), (4) ticket único vs por estación, (5) logo vs solo texto.

---

## Sesión 2026-04-23 (sesión 6) — kapso-webhook Kapso v2 compat + review flow hardening

### Tipo: 🔧 Técnico — 5 bug fixes en kapso-webhook y review-classifier

### Completado

**Bug #4.4 — kapso-webhook no recibía eventos de Kapso (webhook no registrado):**
- Root cause: Kapso requiere registro explícito vía `POST /platform/v1/whatsapp/phone_numbers/{id}/webhooks`. Nunca se había registrado.
- Fix: GET handler (callback OAuth) ahora registra el webhook automáticamente al completar la conexión. El Padrino se registró manualmente disparando el GET handler.
- Commit: `a90ce66`

**Bug #4.5 — kapso-webhook event type incorrecto:**
- Root cause: El código chequeaba `message.received` pero Kapso v2 envía `whatsapp.message.received`.
- Fix: corregido event type en POST handler.
- Commit: `a90ce66`

**Bug #4.6 — kapso-webhook routing fallaba por payload v2 incompatible:**
- Root cause: Kapso v2 no incluye `customer_id` en el payload de `whatsapp.message.received`. El código chequeaba `kapsoCustomerId && fromPhone` — como `customer_id` era `undefined`, el bloque completo nunca se ejecutaba.
- Cambios adicionales: `message.text` es objeto `{body:"..."}`, no string → extraer `message.kapso.content` o `message.text.body`. `fromPhone` viene de `message.from` (no de top level). Routing por `phone_number_id` (top level) en lugar de `kapso_customer_id`.
- `whatsapp.phone_number.created`: customer id está en `customer.id`, no `customer_id`.
- Commit: `8a72b1c`

**Bug #4.7 — welcome message se enviaba después de review completado:**
- Root cause: cuando `review_completed_at` ya está seteado, `pendingReview` es null y el código caía al path de bienvenida.
- Fix inicial: check `recentCompleted` después de `pendingReview`. No suficiente — existía bug cross-order.
- Commit: `42525cb`

**Bug #4.8 — cross-order routing: mensaje post-review se ruteaba a otro pedido pendiente:**
- Root cause: cliente con múltiples pedidos con `review_prompt_sent_at` activos. Al completar review de #9475, la respuesta "Muchas gracias" encontraba #4830 como `pendingReview` y lo bufereaba.
- Fix definitivo: ejecutar `pendingReview` y `recentCompleted` en paralelo. Si `review_completed_at > review_prompt_sent_at` del pending → silencio.
- Commit: `098030a`

**Bug #4.9 — review-classifier ofrecía compensación/descuentos:**
- El modelo generaba frases como "¿Podríamos compensarte en tu próximo pedido?" para reviews negativos.
- Fix: regla PROHIBIDO ABSOLUTO en system prompt — nunca ofrecer compensación, descuento, reembolso, cortesía ni beneficio.
- Commit: `480deaa`

### Commits de esta sesión
- `a90ce66` — fix: kapso-webhook — register webhook + fix event type
- `8a72b1c` — fix: kapso-webhook v2 payload compat — phone_number_id routing + text extraction
- `42525cb` — fix: kapso-webhook — stay silent after review_completed_at
- `098030a` — fix: kapso-webhook — check recentCompleted before routing (cross-order fix)
- `480deaa` — fix: review-classifier — prohibit compensation/discounts/refunds

### Estado de deploys
- `kapso-webhook` v23 ✅ deployado
- `review-classifier` v5 ✅ deployado
- `main` sincronizado con `origin/main` ✅

### Validación E2E (múltiples pruebas reales)
- Flujo completo: feedback WA → respuesta negativa → IA responde con empatía sin compensación → silencio tras completion
- Silencio cross-order confirmado: "Muchas gracias" post-review no se rutea a otro pedido
- Hard cap 3 customer turns activo y probado

### Pendiente
- 3 rondas de prueba adicionales (Oscar maneja manualmente con reset vía SQL)
- El Charakato: QA visual light theme + cambiar password TempPass2026!
- Soli Sushi: cobro (retrasado 9+ días)
- Felipe equity: propuesta firmable + revisión legal no-competencia PedidosYa
- Platanus: video demo 2-3 min
- docs/bugs-abiertos.md: actualizar con bugs #4.4-#4.9 resueltos

### GOTCHAs nuevos

- **Kapso v2 payload — NO hay `customer_id`**: El evento `whatsapp.message.received` NO tiene `customer_id` en ningún nivel. Usar `phone_number_id` (top level) para lookup de restaurante.
- **`message.text` es objeto, no string**: En Kapso v2, `message.text = {body: "..."}`. Para extraer el texto usar `message.kapso.content` (mejor, pre-procesado) o `message.text.body`. `String(message.text)` = `"[object Object]"`.
- **Webhook Kapso requiere registro explícito**: La conexión OAuth no registra el webhook de mensajes entrantes. Requiere `POST /platform/v1/whatsapp/phone_numbers/{phone_number_id}/webhooks` con `{whatsapp_webhook: {url, events: ['whatsapp.message.received'], secret_key}}`.
- **Cross-order silence**: Comparar `review_completed_at` vs `review_prompt_sent_at` del pending. Si completed es más reciente → silencio, aunque exista otro pedido pendiente del mismo cliente.
- **Sistema de reset para pruebas**: Para reiniciar el flujo de review de un pedido: DELETE pedido_review_turns, UPDATE pedidos con todos los campos de review = NULL + feedback_sent=false + delivered_at=NOW()-31min, luego invocar kapso-feedback-scheduler manualmente.

---

## Sesión 2026-04-22 (sesión 5) — Nuevo tenant Al Dente + scraper Uber Eats

### Tipo: 🔀 Mixta — nuevo scraper + demo deployada + skill upgrade

### Completado

- **Nuevo scraper `tools/ubereats_scraper.py`**: Playwright, JSON-LD para catálogo, DOM para imágenes. 24 productos / 19 imágenes para Al Dente Antofagasta.
- **Nuevo tenant Al Dente**: importado via `/kitcha-import-pedidosya` con seed SQL `20260422_seed_al-dente-pasta-al-paso-antofagasta.sql`. 3 categorías (Pastas/Bebidas/Postres), 24 productos.
  - User ID: `3df99915-51e6-4961-8b27-47c635c3839e`
  - Slug: `al-dente-pasta-al-paso-antofagasta`
  - Login: `aldentepastaalpasoantofagasta@kitchat.cl` / `TempPass2026!`
  - Customer: `https://white-cassini-sigma.vercel.app/?local=al-dente-pasta-al-paso-antofagasta`
- **Bug fix horarios demos**: seed generaba `horarios_semana` con formato incorrecto → restaurante aparecía cerrado. Fix: `horarios_semana = NULL` → `useStoreStatus.ts:50` devuelve `isOpen:true` inmediatamente. Aplicado en Al Dente y corregido en skill + seed guardado.

### Pendiente
- Subir logo de Al Dente → `restaurant-assets/3df99915-51e6-4961-8b27-47c635c3839e/logo.png`
- 5 productos sin imagen (Benedictino x2, Jumex, Tiramisú x2) — probablemente no tienen foto en UE

---

## Sesión 2026-04-22/23 (sesión 3) — Review IA E2E debugging + validación

### Tipo: 🔧 Técnico — debug pipeline review completo

### Completado

**Review IA E2E — 4 bugs encontrados y resueltos:**

**Bug #4.1a — kapso-send retornaba 401 desde el scheduler:**
- Root cause: `kapso-feedback-scheduler` v13 (desplegado 2026-04-20) era stale — desplegado ANTES del commit `22e67f0` (2026-04-21) que agregó el header `x-internal-secret`. Sin el header, `internalSecret = ''` → `isServiceRole = false` → fallback a user JWT → 401.
- Fix: redesplegar scheduler → v14. No requirió cambio de código.

**Bug #4.1b — kapso-send retornaba 500 tras redesploy del scheduler:**
- Root cause: `safeCompare()` en kapso-send llamaba `crypto.subtle.timingSafeEqual` — función que NO existe en Deno Web Crypto API (solo en Node.js). Al llamarla por primera vez → `TypeError` → 500.
- Fix: reemplazado con XOR loop manual sobre `Uint8Array` de SHA-256 digests. Commit `023abfa`.

**Bug #4.3 — Mensaje de feedback enviado dos veces al mismo cliente:**
- Root cause: Dos pedidos (`#9475` y `#4830`) con el mismo `telefono` en `clientes`. El scheduler procesaba ambos en el mismo ciclo sin deduplicar.
- Fix: Set `phonesMessaged` con clave `restaurante_id:telefono`. Si ya se envió en este ciclo, se marca `feedback_sent=true` y se omite. Commit `b6249cb`.

**Bug #4.2 — Respuesta del cliente ("me gustó") no disparaba la IA:**
- Root cause: `kapso-webhook` construía `phoneVariants` con solo `['56982717201', '982717201']`. DB almacena `+56982717201` (con `+` prefix). El lookup en `clientes` fallaba → no se encontraba `clienteRow` → `review_pending_message` nunca se seteaba → flusher no corría → sin reply IA.
- Fix: siempre incluir `'+' + rawDigits` en phoneVariants + variantes `+` en todas las ramas de normalización. Commit `b6249cb`.
- El mensaje "me gustó" fue perdido (llegó antes del fix). Se inyectó manualmente vía SQL UPDATE para desbloquear el test E2E.

**Commits:**
- `023abfa` — fix: kapso-send safeCompare Deno-compatible (XOR SHA-256)
- `b6249cb` — fix: webhook phone variants + scheduler dedup

**Review IA E2E VALIDADO ✅:**
- Pedido entregado → scheduler envía feedback WA → cliente responde → webhook buferea → flusher invoca review-classifier → Claude Haiku genera reply empático → kapso-send envía al cliente.
- Confirmado por Oscar: "Funciona con comentarios"
- `pedido_review_turns` populada correctamente (turno assistant inicial + turno user + turno reply IA).

### Pendiente inmediato
- `git push origin main` — 2 commits adelante de origin/main (023abfa + b6249cb)
- Update `docs/bugs-abiertos.md` — marcar #4.1/#4.2/#4.3 resueltos, Review IA E2E validado
- El Charakato: QA visual light theme + cambiar password TempPass2026!
- Soli Sushi: cerrar cobro (retrasado 9+ días)
- Felipe: enviar propuesta firmable + contactar abogado no-competencia PedidosYa
- Platanus: grabar video demo 2-3 min (login → onboarding → pedido en vivo → feedback WA)
- Días 3-8 del plan: onboardings #5-10, bug #2.2 dashboard $0, BSUID migration (opcional)

### GOTCHAs nuevos

- **Supabase Edge Functions NO se redesplegan automáticamente con git push.** Siempre verificar que la versión en `supabase functions list` (campo UPDATED_AT) sea posterior al commit relevante. Si hay duda: redesplegar explícitamente.
- **`crypto.subtle.timingSafeEqual` NO existe en Deno Web Crypto API** — solo en Node.js. Para comparación timing-safe en Deno usar XOR loop sobre `Uint8Array` de SHA-256 digests (patrón ya implementado en kapso-send `safeCompare()`).
- **`clientes.telefono` almacena con prefijo `+`** — siempre incluir `'+' + rawDigits` al construir `phoneVariants` en el webhook. Omitirlo rompe silenciosamente el lookup de clientes.
- **Deployments stale → cascada de errores difíciles de depurar.** El patrón: 401 → 500 → funcionalidad ausente — cada error tenía una causa distinta en la misma cadena. Primer diagnóstico: verificar versión deployada vs fecha del commit fix.

---

## Sesión 2026-04-22/23 — Auditoría + reconciliación + bugs 🔴

### Tipo: 🔧 Técnico — auditoría documental + fixes customer-app

### Completado

**Auditoría completa + reconciliación (Part B del plan):**
- `docs/decisiones-canonicas.md` creado — ADR con pricing 3 planes, billing MP, naming Kitchat, 8 edge functions, 15 migraciones
- `docs/bugs-abiertos.md` creado — fuente única QA con todos los bugs 🔴🟡🟢
- `supabase/functions/.env.example` creado — 7 variables documentadas
- `CLAUDE.md` actualizado: 6→8 edge functions, 2→4 tenants, Sprint 5 mergeado, bugs #3.2/#3.3 resueltos, §12 deuda técnica
- `estado.md` actualizado: Hillfood + equipo Platanus completado
- `pitch-platanus-2026.md`: pricing 3 planes (sin Esencial), bug #3.2 marcado resuelto
- `kitchat-gtm-report.md`: eliminado plan Esencial
- `onboarding-felipe-2026-04-21.html` → v1.1: 8 fixes (timezone 7h, billing=MP, dominio customer correcto, 4 tenants, equipo Platanus completada, roadmap-interno archivado)
- 12 docs obsoletos movidos a `docs/archive/`, 4 archivos legacy JS movidos a `legacy/`
- `supabase/migrations/20260422_seed_hillfood.sql` commiteado (era untracked)
- Worktrees obsoletos (track-b, customer-redesign) limpiados
- Commits: `1ca996e` (reconciliación principal), `949fd8e` (onboarding v1.1), `a35c5cb` (bugs + archive cleanup)

**Bug #1.11 RESUELTO (customer-app):**
- `useOrderTracking.ts`: reemplazado `useEffect+deps[activeOrderId.value]` por `useEffect(() => effect(()=>{...}), [])` — garantiza que el polling arranque cuando se coloca un pedido en-sesión sin necesidad de reload
- Root cause: `useEffect` con signal value como dep no garantiza re-run en @preact/signals v2.x cuando el component retornaba null inicialmente

**Bug #1.2 CONFIRMADO YA RESUELTO:**
- `useStoreStatus.ts` ya usa `Intl.DateTimeFormat` con `timeZone: 'America/Santiago'` — la timezone era correcta en el código

**Bug #1.9 PARCIALMENTE RESUELTO:**
- `CheckoutModal.tsx` línea 98: typo `(mesa || !deliveryActive) ? 'Retiro' : 'Retiro'` → `'Retiro' : 'Delivery'` (la segunda rama siempre era 'Retiro')
- `components.css` `#checkoutModal .modal-body`: agregado `min-height: 0; overflow-y: auto;` para que el botón "Pedir" no quede fuera del viewport en mobile
- Métodos de pago extra: no es bug de código — es configuración (activar `bank_active`/`card_active` en Settings)

### Pendiente inmediato
- `git push origin main` → Vercel despliega customer-app con los 3 bug fixes (Oscar debe hacer el push)
- Validar bug #1.11 con pedido real post-deploy
- Review IA E2E con pedido real (criterio pitch Platanus)
- El Charakato: QA visual light theme + cambiar password TempPass2026! → activar
- Soli Sushi: cerrar cobro (retrasado 9+ días)

### GOTCHAs nuevos
- `@preact/signals` v2.x + `useEffect` deps: usar `effect()` signal-native para auto-tracking en lugar de pasar `signal.value` como dep de `useEffect` — más robusto para detectar cambios
- `CheckoutModal` persiste estado entre aperturas (componente siempre montado, no remonta) — el `deliveryType` se resetea al defecto inicial solo en primera carga de app


---

## Sesión 2026-04-22 — Pitch Platanus: equipo + deck HTML

### Tipo: 🤝 Agencia — sin código ni deploys

### Completado

**`pitch-platanus-2026.md` actualizado:**
- Sección 4 (equipo) desbloqueada: Oscar Vergara (CEO/técnico) + Felipe Ignacio Hernández Morales (cofundador comercial)
- Felipe: 7 años PedidosYa KAM Sr., Ing. Comercial UCN, Diplomado E-commerce PUC 2024, ex-cofundador Mr.Salad Chile (2017), ex-gerente Chicken Love You (2023), @felipe_efood
- One-liner canónico: "SaaS para restaurantes: menú digital, pedidos por WhatsApp y reviews automáticos con IA — sin comisiones, sin marketplaces."
- OlaClick corregido: "~60 rest. Chile, baja tracción" en todas las menciones (antes decía "sin presencia")
- Modelo financiero: tabla valuaciones 300/800/1500/2000 clientes
- 4ª razón "por qué ganamos": equipo con PMF humano
- Respuesta Kalio "¿Por qué este equipo?" rellena
- Nota no-competencia PedidosYa · Carta de intención añadida al checklist

**`pitch-platanus-2026.html` CREADO:**
- Deck Reveal.js 12 slides, paleta Kitchat verde (#22c55e / #0a0f1e)
- Portada → Problema → Solución → Por qué ahora → Tracción → Mercado → Equipo → Por qué ganamos → Unit economics → Ask $200K → Roadmap 6 meses → Cierre
- Slide 10: respuesta sobre Appio (complementario, no competidor)
- Listo para Chrome (F = full-screen, ?print-pdf = PDF)

### Decisiones clave

- Escenario B (Felipe con comisión en PedidosYa) **NO va en pitch** — debilita señal de compromiso
- Equity Felipe: **18% definitivo** según `propuesta-cofundador-felipe.docx` (fuente de verdad)
- Mr.Salad + Chicken Love You **SÍ se incluyen** — credencial "piel en el juego" que Platanus valora
- OlaClick framing: "baja tracción = argumento más fuerte" (Kitchat crece más rápido con 1 cliente)

### Pendientes Platanus (antes del 30 de abril)

| Pendiente | Urgencia | Responsable |
|---|---|---|
| Carta de intención Felipe firmada | 🔴 | Oscar + Felipe |
| Verificar no-competencia PedidosYa | 🔴 | Oscar + Felipe |
| Bug #3.2 mensajes Kapso (demo reviews IA) | 🔴 | Oscar |
| QA visual pitch HTML en Chrome | 🟡 | Oscar |
| Revenue exacto acumulado en CLP | 🟡 | Oscar |
| Video demo 2-3 min | 🟡 | Oscar |
| 3-4+ clientes referidos pagando | 🟡 | Felipe |
| Publicar HTML en creactivestudio.agency/propuestas/ | 🟢 | Oscar (opcional) |

### Gotchas nuevos

- OlaClick Chile: usar "~60 rest., baja tracción" (nunca "sin presencia") — la realidad es el argumento más fuerte
- Equity Felipe: `propuesta-cofundador-felipe.docx` tiene 18% definitivo; `estrategia-fundadores` tenía rango 15-20% como pre-negociación. Propuesta.docx gana.
- Re-branding plantilla CreActive→Kitchat: solo cambiar valores de CSS vars (--red→verde, --teal→verde, --blue→verde). Las clases helper siguen funcionando sin renombrar.
- Ba-grid con 2 problemas (no problema/solución): usar `style` inline en segundo panel para forzar rojo semántico (#ef4444). Ver slide 2 del pitch HTML.

---

## Sesión 2026-04-21 (tarde) — Nuevo tenant El Charakato + light theme

### Completado

**Nuevo tenant cargado:**
- Usuario `charakato@kitchat.cl` creado en Supabase Auth (`id: bed44b55-e92c-42a3-be15-8b19f7cbde2f`)
- Restaurante creado: `id: 96e6ac8a-9e1e-45f8-a26c-66a063a001c6`, slug `el-charakato`
- Migración `supabase/migrations/20260421_seed_el_charakato.sql` ejecutada y commiteada
- 9 categorías, 53 productos con fotos de PedidosYa CDN
- Config: tema `light`, color `#D32F2F`/`#B71C1C`, 16:00–22:00 todos los días, delivery+retiro, $1.000 delivery, $8.000 min, 35 min prep, Efectivo/Tarjeta en entrega
- Logo actualizado en DB: `https://assets.cdn.filesafe.space/EkZ4WH72KLjDMADUvy8s/media/69e7e4735e482c379bc17929.jpg`
- Password temporal: `TempPass2026!` (debe cambiar)

**Feature: light theme dinámico en customer app (`commits d2e0d31 + a61fa63`):**
- `customer-app/src/hooks/useBranding.ts`: fondo hardcodeado negro → condicional por `config_marca.tema`
  - `light`: bg `#fff`, surface `#f5f5f5`, text `#111`, muted `#6b7280`, border `#e5e7eb`
  - `dark`: comportamiento anterior (El Padrino y Soli Sushi sin cambios)
- `customer-app/src/signals/store.ts`: agregado `tema?: 'light' | 'dark'` al tipo `config_marca`
  - El primer build de Vercel falló por TS2339 (campo `tema` no declarado) — se corrigió en commit `a61fa63`

### Acceso
- Demo customer: `https://white-cassini-sigma.vercel.app/?local=el-charakato`
- Admin: `admin.kitchat.cl` → `charakato@kitchat.cl` / `TempPass2026!`

### Pendiente de esta sesión
1. ⏳ Verificar QA visual del demo con tema light en Vercel (deploy en progreso)
2. ⏳ Crear skill de onboarding de nuevo cliente (quedó pendiente — próxima sesión)
3. ⏳ Push admin-react a Vercel (toasts de error de Bug #3.3 — pendiente desde sesión anterior)

### GOTCHAs nuevos
- **`useBranding.ts` tema hardcodeado:** Tenía comentario "Customer app always uses dark theme" — el campo `config_marca.tema` existía en DB pero nunca se aplicaba en la customer app
- **Tipo `config_marca` incompleto:** `store.ts` no declaraba `tema` → TS2339 en build de Vercel. Siempre verificar que los campos nuevos estén en la interfaz `Restaurant`
- **URLs de fotos PedidosYa:** Son accesibles directamente desde `pedidosya.dhmedia.io` — se pueden usar en `imagen_url` sin re-hostear para demos
- **Seed demo con duplicados:** El Charakato repite "Pollo al horno" y "Tortilla" en Los Elegidos y Colaciones — fue decisión explícita del cliente para reflejar su menú de PedidosYa

---

## Sesión 2026-04-21 — Bug #3.3 RESUELTO (kapso-send 401 silencioso)

### Root cause
El commit `d7a2da9` (Bug #3.2) removió `--no-verify-jwt` de `kapso-send`. El gateway de Supabase empezó a rechazar todos los user JWT del admin con 401 en 50-150ms (antes de entrar al código). Los handlers del admin capturaban el error con `console.warn` silencioso — invisible para el usuario.

Evidencia definitiva: edge logs mostraban decenas de 401 consecutivos en kapso-send v23. Todas las otras funciones (con `--no-verify-jwt`) devolvían 200.

La config del tenant "El Padrino Pizza" estaba perfecta (connected=true, todos los toggles, phone_number_id correcto) — no era un bug de datos.

### Fix (commit `22e67f0`)
- **`kapso-send/index.ts`**: reemplaza `jwtRole()` por `x-internal-secret` header + `safeCompare()` SHA-256 para callers internos. User JWT sigue usando `auth.getUser(token)`. Redeploy con `--no-verify-jwt`.
- **`kapso-feedback-scheduler`, `kapso-review-flusher`, `kapso-webhook`**: agregan header `x-internal-secret: $INTERNAL_WEBHOOK_SECRET` al invocar kapso-send. Todos redeploy.
- **`OrdersPage.jsx`, `OrderDetailModal.jsx`, `ConversationsPage.jsx`**: `console.warn` → toasts de error visibles. (⚠️ código committed pero admin-react NO pusheado a Vercel todavía)
- **`CLAUDE.md`**: corregidas instrucciones contradictorias — todas las edge functions requieren `--no-verify-jwt`.
- **INTERNAL_WEBHOOK_SECRET**: generado y seteado en Supabase Secrets (proyecto gjkaboosygjitxgqcawy).

### Pendiente de esta sesión
1. **QA prod:** Crear pedido de prueba en El Padrino → cambiar estado a "preparando" → verificar que llega WA "pedido aceptado"
2. **Push + Vercel deploy admin-react:** `git push origin main` → Vercel despliega toasts de error automáticamente

---

## Sesión 2026-04-20 (noche) — Bug #3.2 RESUELTO + cierre

### Completado
- **Bug #3.2 root cause:** `timingSafeEqual(token, SUPABASE_SERVICE_ROLE_KEY)` en `kapso-send` fallaba silenciosamente porque el env var tenía trailing `\n` → length mismatch → `return false` inmediato → caía al path de user JWT → 401
- **Fix:** Reemplazado por `jwtRole(token) === 'service_role'` (decodifica el payload del JWT y lee el claim `role`). El gateway de Supabase valida la firma (verify_jwt=true) — la función solo lee el claim.
- **kapso-send ahora deploya SIN `--no-verify-jwt`** — única función con verify_jwt=true
- **Commits:** `d7a2da9` (fix auth) + `0d3511e` (CLAUDE.md actualizado)
- **Diagnóstico previo confirmado:**
  - El Padrino: todos los toggles `true`, `feedback_delay_minutes` no configurado (defaults 60 min)
  - Soli Sushi: `connected: null` — no usa Kapso
  - pg_cron logs: `processed:4, sent:0` — confirmaba auth failure, no scheduler failure
  - curl test post-fix → auth pasa, Kapso retorna error 24h (ventana real expirada en test)
- **24h window NO es problema en producción:** Clientes siempre escriben primero en Kitchat. No se necesitan templates HSM.
- **4 pedidos stuck** (#7182, #4513, #3738, #1761): auto-limpiados por cleanup step del scheduler (>24h)

### Pendiente inmediato (Oscar)
- Configurar El Padrino en SettingsPage → Integraciones → Encuesta Post-Entrega: `google_review_url`, toggle ON
- QA review flow: esperar pedido real El Padrino → verificar WA 60 min post-entrega → responder → ver clasificación en dashboard

### Próximo paso exacto
**Sesión 3B — Kitcha Landing** (recomendado, cero riesgo prod): `/pro-prd-landing --cliente=kitcha` con `docs/kitchat-landing-brief.md` + `docs/kitchat-gtm-report.md`

**Sesión 3A — Multi-sucursal** (requiere prep): 48h aviso a tenants + backup DB + ventana mantenimiento. Plan: `sequential-strolling-cerf.md`

---

## Sesión 2026-04-20 (tarde) — Tarea BSUID Kapso guardada en memoria

- Revisado migration guide de Kapso sobre Business-Scoped User IDs (BSUIDs)
- Guardado checklist de 8 items en `project_white_cassini_bsuid_migration.md`
- Tarea a ejecutar esta semana: adaptar schema + parsers + matching logic en Kitcha

---

## Sesión 2026-04-20 — Ajustes UX customer app + fix orden Sándwich

**Commit `d2813c9` — pusheado a main (Vercel desplegando)**

1. **`~ → aprox.`** en 3 ocurrencias de la customer app:
   - `HeroSection.tsx:40,46` — chips del hero
   - `CustomerForm.tsx:52` — subtítulo botones Delivery/Retiro en checkout

2. **Fix bug crítico: `.order('orden')` faltaba en query de productos** (`useStore.ts:64`)
   - Sin este fix, el drag-reorder del admin no tenía efecto en la customer app
   - Las otras 4 tablas del mismo `Promise.all` ya lo tenían — solo productos estaba roto

3. **UPDATE orden 28 productos Sándwich (El Padrino) en DB** (via Management API)
   - Churrasco Apolloni y Lomito Apolloni: `orden=9999` → posiciones 2 y 8 respectivamente
   - Orden final 0–27: Churrascos → Lomitos → Mechadas → Hamburguesas → Ave → Vegetarianos → Crispy

**GOTCHA nuevo:** El bug de `.order('orden')` era silencioso — Postgres retornaba casi siempre insertion order (que coincidía con el orden deseado). Solo se hizo evidente cuando se agregaron productos nuevos con `orden=9999` al final.

---

## Sesión 2026-04-15 — Fix bugs WhatsApp/Kapso

### Bug #2 RESUELTO — kapso-conversations per_page
- **Fix:** `per_page=50` → `per_page=100` en `supabase/functions/kapso-conversations/index.ts:87`
- **Deploy:** `supabase functions deploy kapso-conversations --project-ref gjkaboosygjitxgqcawy --no-verify-jwt` ✅
- **Resultado:** Panel de conversaciones ahora muestra 20-30 activas en vez de ~10

### Bug #1 PARCIALMENTE RESUELTO — kapso-feedback-scheduler

**Root cause:** La función NUNCA se invocaba. No había pg_cron, no había cron job, no había ningún invocador. Además el deploy original tenía `verify_jwt=true`.

**Fixes aplicados en DB (via Management API):**
1. `CREATE EXTENSION pg_cron` — habilitado (pg_net ya estaba)
2. Trigger `set_delivered_at` ampliado: cubre `enviado` Y `entregado` (salto directo)
3. Índice parcial `idx_pedidos_feedback_scheduler` reemplazado: cubre `estado IN ('enviado','entregado')` + `delivered_at IS NOT NULL`
4. Cron job registrado: `cron.schedule('kapso-feedback-scheduler-tick', '*/15 * * * *', net.http_post(...))`

**Nueva migración:** `supabase/migrations/20260415_feedback_scheduler_fixes.sql` (en repo)

**Scheduler reescrito** (`supabase/functions/kapso-feedback-scheduler/index.ts`):
- Query: `IN ('enviado','entregado')`, `NOT NULL cliente_id`, ventana 90min-24h
- Usa `supabase.functions.invoke` (NO raw `fetch`) — gateway Supabase NO propaga `Authorization` header en llamadas inter-función vía URL pública; `invoke` usa routing interno
- Error handling: éxito → mark done; skipped 204 → mark done; 4xx/5xx → retryable (no marca); network → retryable
- Cleanup al final: expira pedidos > 24h que siguen pendientes
- Deploy: `--no-verify-jwt` ✅

**Estado actual:**
- `processed: 1, sent: 0, feedback_sent: false` → auth funciona, error viene de Kapso API (externo, retryable)
- El scheduler corre cada 15 min y reintenta
- **Bug #3.2 externo (pendiente):** "Mensajes automáticos Kapso no llegan, manual sí funciona" — necesita diagnóstico via Supabase Dashboard → Edge Functions → kapso-send → Logs. Ver qué responde la API de Kapso cuando se llama con `type: 'feedback'`

**CLAUDE.md del proyecto actualizado:**
- Sección 3 tabla: `kapso-feedback-scheduler` corregido a `SÍ` verify_jwt = NO (usa `--no-verify-jwt`)
- Nota de deploy corregida: "Todas las Edge Functions requieren `--no-verify-jwt`"
- Nuevo gotcha: inter-function auth via `invoke` no `fetch`
- Sección 9: bug marcado como resuelto (con nota sobre #3.2 pendiente)

---

## Sesión 2026-04-15 (tarde) — Feature Review Flow Automático Post-Entrega DISEÑADO

### Qué se diseñó
Flujo completo post-venta vía WhatsApp usando Claude Haiku 4.5:
- 60 min post-entrega (configurable por restaurante): scheduler envía "¿Cómo estuvo tu pedido?"
- Webhook acumula respuestas en buffer (debounce 30s para agrupar mensajes fragmentados)
- Flusher (pg_cron cada 1 min) procesa el buffer y llama a `review-classifier`
- Claude Haiku 4.5 clasifica sentimiento, genera respuesta empática contextual (1-2 oraciones)
- Positivo: invita a dejar reseña en Google con link configurado
- Negativo: pide detalles y escala al admin
- Hard cap 3 turnos de cliente (code-enforced, anti-prompt-injection)
- Dashboard admin: badges de sentimiento, historial de turnos, botón "resolver"

### Plan guardado
`~/.claude/plans/rippling-wondering-fern.md` — plan completo con código esqueleto, migración SQL, checklist de tests de seguridad (prompt injection, cap de turnos) y anti-regresión.

### Decisiones técnicas clave
- **Modelo:** `claude-haiku-4-5` (elección explícita por costo: ~$0.0025/review vs $0.0125 Opus)
- **Sin adaptive thinking** — Haiku 4.5 no lo soporta
- **Debounce:** 30s + flusher cada 1 min (pg_cron `* * * * *` estándar, compatible con cualquier versión)
- **Anti-injection:** cap en código TypeScript + wrap de mensajes en `<customer_message>` tags + instrucción explícita en system prompt
- **~50K invocaciones/mes** — 10-12% del free tier Supabase

### Archivos NUEVOS a crear
- `supabase/migrations/20260416_review_flow.sql`
- `supabase/functions/review-classifier/index.ts`
- `supabase/functions/kapso-review-flusher/index.ts`

### Archivos EXISTENTES a modificar
- `supabase/functions/kapso-send/index.ts` — nuevo type `custom_text`
- `supabase/functions/kapso-feedback-scheduler/index.ts` — delay per-restaurant, registro turno inicial
- `supabase/functions/kapso-webhook/index.ts` — router a buffer (no llama Claude directo)
- `admin-react/src/pages/SettingsPage.jsx` — campos `google_review_url` + `feedback_delay_minutes`
- `admin-react/src/pages/OrdersPage.jsx` — badge sentiment
- `admin-react/src/components/orders/OrderDetailModal.jsx` — sección Review

---

## Sprint 5 — Rediseño customer app + QA fixes (COMPLETO, pendiente merge)

**Rama activa:** `feature/customer-redesign` (último commit `ed57573`). Worktree: `.worktrees/customer-redesign/`.

### Commits del sprint (en orden)

| Hash | Descripción |
|------|-------------|
| `4e0bd7c` | feat: home con categorías + menú scroll anclado |
| `4ddef62` | docs: CLAUDE.md actualizado |
| `580e79b` | fix: 3 bugs QA (navbar sticky, nav sheet modal, search desde home) |
| `4f5a2d9` | fix: tab bar spacing (48→56px) |
| `ed57573` | feat: auto-collapse grupos modificadores al completar selección |

### Fix de datos en producción (sin commit, directo en DB)
- "Gohan Acevichado" movido de categoría "Arma tu Gohan" → "Elige tu Menú" en Soli Sushi

### Próximo paso exacto (sprint 5)

**QA visual final + merge a main:**
1. Vercel preview ya desplegado (último push: `ed57573` → `origin/feature/customer-redesign`)
2. Validar con `?local=elpadrino` y `?local=soli-sushi` el checklist de 7 puntos
3. `gh pr create` → merge a main → Vercel deploy a producción

**Checklist QA:**
1. Carga arranca en HomeView con grid de categorías
2. Click en card → MenuView scrolleado a la categoría correcta
3. Tab bar sticky: highlight automático al scrollear, sin overlap con navbar
4. Botón tres puntos → bottom sheet visible (centrado en viewport, no al fondo)
5. Back-to-home en navbar (solo en MenuView)
6. Search desde HomeView → cambia a MenuView y muestra resultados
7. ProductModal con grupos: al seleccionar mínimo requerido, el grupo colapsa y muestra el resumen
8. Carrito, checkout, modal de producto: sin regresiones

---

## Fase 2 — Multi-sucursal (PRÓXIMA — plan aparte)

Decisiones ya documentadas en el plan `sequential-strolling-cerf.md`. NO empezar hasta que `feature/customer-redesign` esté mergeado.

---

## Pendientes

### Bug #3.2 — Mensajes automáticos Kapso (INVESTIGAR)
- "Mensajes automáticos no llegan al cliente, manual sí funciona"
- Para diagnosticar: Dashboard Supabase → Edge Functions → `kapso-send` → Logs
- Ver qué devuelve la API de Kapso cuando el type es `feedback` o cualquier automático
- Posibles causas: rate limit Kapso, phone_number_id errado, template no aprobado en Meta, token expirado

### Soli Sushi (cliente)
- Cambiar password temporal `TempPass2026!`
- Reemplazar `telefono_whatsapp = '+56900000000'` con número real
- Confirmar horarios reales en Settings → Horarios
- Subir fotos de productos
- Decidir si activan delivery y configurar zonas

### El Padrino (pendiente de siempre)
- Configurar `pickup_time` y `delivery_time` en Settings > Operaciones
- Impresora térmica (#7) — bloqueada, falta info de hardware

### Producto (backlog)
- Bugs conocidos en producción documentados en `docs/Revision flujo.md`
- Mercado Pago — requiere credenciales por restaurante + SDK MP
- Merge `feature/customer-redesign` → main (QA visual pendiente)
- **Filtro de fecha en dashboard admin:** selector de rango → muestra órdenes → descarga CSV. Complejidad media-baja (~1-2 días). Decisión clave: server-side query ad-hoc separada del Realtime (estado `filteredOrders` vs `liveOrders`). HeroUI tiene `DateRangePicker` nativo. Archivos a tocar: `OrdersPage.jsx`, `DataContext.jsx`.

---

## Sesión 2026-04-22 — Flujo demo PedidosYa→Kitcha

### Completado

**Nuevo tenant demo: Hillfood**
- Usuario `hillfood@kitchat.cl` creado en Supabase Auth (`id: 7e9bd199-939d-4bb1-9833-958185c9ec63`)
- Seed `supabase/migrations/20260422_seed_hillfood.sql` aplicado — 5 categorías, 21 productos, fotos PedidosYa CDN
- Colors: `#D32F2F` / `#B71C1C` / `dark` (branding demo Kitcha estándar)
- Demo customer: `https://white-cassini-sigma.vercel.app/?local=hillfood`
- Password: `TempPass2026!`

**Infraestructura de demos creada:**
- `tools/pedidosya_scraper.py` → ahora genera JSON (no CSV) con estructura Supabase-compatible
- `.claude/commands/kitcha-import-pedidosya.md` → skill que toma el JSON y activa el demo end-to-end (crea user + aplica seed)
- Flujo completo: URL PedidosYa → scraper (~10s) → `/kitcha-import-pedidosya` → demo vivo en Kitcha

### Decisiones
- Colores de demo siempre fijos: `#D32F2F` / `#B71C1C` / `dark` (no se leen del restaurante)
- Email de demo: `{nombre_normalizado}@kitchat.cl`
- SQL seed sigue convención `YYYYMMDD_seed_{slug}.sql`

### GOTCHAs nuevos
- `jq -n` con strings SQL que tienen comillas dobles falla (Postgres las interpreta como identificadores). Usar `jq -Rs` con heredoc.

---

## URLs de producción

| App | URL |
|-----|-----|
| Admin panel (dominio custom) | https://admin.kitchat.cl |
| Admin panel (vercel) | https://white-cassini-admin.vercel.app |
| Customer app | https://white-cassini-sigma.vercel.app |
| El Padrino | https://white-cassini-sigma.vercel.app/?local=elpadrino |
| Soli Sushi | https://white-cassini-sigma.vercel.app/?local=soli-sushi |
| El Charakato | https://white-cassini-sigma.vercel.app/?local=el-charakato |
| Hillfood (demo) | https://white-cassini-sigma.vercel.app/?local=hillfood |
| Supabase Dashboard | https://supabase.com/dashboard/project/gjkaboosygjitxgqcawy |
| Supabase project ref | `gjkaboosygjitxgqcawy` |

---

## GOTCHAs consolidados

**Supabase MCP:** `mcp__supabase__` es Nutrisco (`kkkqpkyltekphrurjzwp`). `mcp__supabase-white-cassini__` es este proyecto pero suele no estar disponible. Usar Management API con token del keychain: `security find-generic-password -s "Supabase CLI" -a "supabase" -w | sed 's/go-keyring-base64://' | base64 -d`. Endpoint: `https://api.supabase.com/v1/projects/gjkaboosygjitxgqcawy/database/query`.

**Crear usuario por API:** Auth Admin API directamente con service_role key: `POST https://gjkaboosygjitxgqcawy.supabase.co/auth/v1/admin/users`.

**`variantes_producto` no tiene `restaurante_id`** — las inserciones de variantes van sin ese campo.

**Supabase migrations drift:** Si `db push` falla, usar Management API directa. Los archivos con prefijo `20260405` confunden al CLI.

**Edge Functions — ALL require `--no-verify-jwt`:** Todas las 6 funciones kapso-* se despliegan con `--no-verify-jwt`. Sin él retornan 401 silenciosamente. Esto incluye `kapso-feedback-scheduler` (nota incorrecta en versiones anteriores del CLAUDE.md).

**Inter-function calls — usar `invoke` no `fetch`:** El gateway de Supabase NO propaga el `Authorization` header cuando una Edge Function llama a otra via URL pública (`fetch('https://xxx.supabase.co/functions/v1/kapso-send', ...)`). Siempre usar `supabase.functions.invoke('kapso-send', { body: {...} })` para llamadas entre funciones internas.

**CategoryNavSheet:** No usa `.modal.active` wrapper — tiene `position: fixed` propio (`.category-nav-overlay` y `.category-nav-sheet`). Si se refactorizan los modales del sistema, no asumir que este sigue el mismo patrón.

**Navbar height fija:** `.navbar` tiene `height: var(--navbar-height, 56px)` + `padding: 0 1rem`. NO volver a poner `padding: 0.75rem 1rem` — daría 62px real vs token 56px y rompería el sticky offset del tab bar.

**STICKY_OFFSET en TS = 112:** Matches `--sticky-offset: 112px` en tokens.css (56px navbar + 56px tab bar). Si cambia alguno de los dos, actualizar en `MenuView.tsx`, `CategoryTabsSticky.tsx` y `tokens.css` al mismo tiempo.

**Auto-collapse en ProductModal:** `toggleEnGrupo` computa el nuevo Set localmente (no usa el updater de React/Preact) para poder hacer dos `setState` en la misma llamada. Solo auto-colapsa si `min_seleccion > 0`. El `pm-group-summary` es un `<p>` fuera del `.option-list` (que se oculta con `display:none` al colapsar), por lo que siempre es visible cuando el grupo está colapsado y tiene selecciones.

**Categoría "Arma tu Gohan":** Solo debe contener el producto builder "Arma tu Gohan". "Gohan Acevichado" fue movido a "Elige tu Menú" en DB (2026-04-13). El seed original lo tenía mal asignado.

**Fase 2 multi-sucursal:** ✅ Desbloqueada — `feature/customer-redesign` mergeado a main (2026-04-20, commit `97704fa`). La Fase 2 puede arrancar en Sesión 3. Requiere ventana de mantenimiento y backup DB antes de tocar schema.

**feedback_90min + bug #3.2:** El scheduler ahora corre cada 15 min y llama correctamente a `kapso-send`. Si `sent` sigue siendo 0, el problema es en la integración Kapso (API externa) no en el scheduler. Ver logs de `kapso-send` en el dashboard para diagnosticar.

**Anthropic SDK — NO existe `output_config`:** El plan de diseño del review-classifier incluía `output_config.format.type = 'json_schema'` pero ese parámetro NO existe en `@anthropic-ai/sdk`. Para JSON estructurado con Haiku 4.5, se usa el system prompt con instrucción explícita de devolver JSON. Claude respeta el formato si el prompt es claro y el JSON schema está en el system prompt.

**`pedidos.cliente` NO es JSONB:** El plan tenía un índice `ON pedidos ((cliente->>'telefono'), ...)` pero `pedidos` NO tiene columna JSONB `cliente`. La columna `cliente` que aparece en queries JS es un alias PostgREST del join con la tabla `clientes` (via `cliente_id` FK). El índice fue corregido a `ON pedidos (cliente_id, review_prompt_sent_at DESC)`. La búsqueda en el webhook usa 2 queries: primero busca en `clientes` por `telefono`, luego busca en `pedidos` por `cliente_id`.

**kapso-send auth — INTERNAL_WEBHOOK_SECRET (post Bug #3.3):** Callers internos (scheduler, flusher, webhook) envían header `x-internal-secret: $INTERNAL_WEBHOOK_SECRET`. kapso-send verifica con SHA-256 (`safeCompare()` — evita el bug de `timingSafeEqual` con bytes de env var). User JWT del admin se valida con `auth.getUser(token)` internamente. Deploy CON `--no-verify-jwt` (igual que todas las demás). Secret seteado en Supabase Secrets.

**TODAS las edge functions requieren `--no-verify-jwt`:** Sin el flag, el gateway rechaza el request con 401 en 50-150ms (antes de ejecutar el código). Esto incluye kapso-send desde Bug #3.3 (2026-04-21). Ver tabla sección 3 del CLAUDE.md.

**Kitcha Landing:** La versión vieja está en iCloud Trash (`/Users/oz/Library/Mobile Documents/.Trash/kitcha-landing/`), no es repo git, y tiene inconsistencia de planes (Freemium/Pro/Custom vs Starter/Pro). Decisión: partir de cero con `/pro-prd-landing`. Insumos rescatados al repo: `docs/kitchat-landing-brief.md` y `docs/kitchat-gtm-report.md`.

---

## Sesión 2026-04-22 — Documento de onboarding para cofundador Felipe

### Completado

**Output principal:**
- `Proyectos Internos/white-cassini/docs/onboarding-felipe-2026-04-21.html` — HTML standalone, 1.515 líneas, 81 KB
  - 16 secciones completas con transparencia total (bugs, deuda técnica, equity)
  - Paleta Kitchat (#22c55e), dark hero, sticky TOC con scroll-spy, print-friendly
  - Sección ⚠️ CONFIDENCIAL: equity Felipe 14-19% vesting 4 años cliff 1 año, riesgo legal PedidosYa
  - Pricing GTM definitivo: Pro $49.900 / Business $89.900 / Business XL $139.900 (sin Esencial)

**Investigación generada:**
- 3 Explore agents en paralelo: arquitectura técnica + inventario funcional + estado ejecutivo
- Inventario completo de 8 Edge Functions, 14 migraciones, schema 11 tablas, 9 páginas admin, 24 componentes customer

### Pendiente inmediato (Oscar)

1. ⏳ Revisar HTML en browser y dar feedback visual
2. ⏳ Decidir si se commite al repo (ahora está sin commitear)
3. ⏳ Acordar equity con Felipe **antes** de compartir el doc — sección 15 es CONFIDENCIAL
4. ⏳ Revisar contratos no-competencia de Felipe y Jorge con PedidosYa antes de mover clientes
5. ⏳ Escribir sección "equipo" del formulario Platanus (vacía — bloqueante para 30-abr)
6. ⏳ Validar Review IA end-to-end con pedido real (Bug #3.2/#3.3 resueltos pero E2E no verificado)

### Decisiones tomadas

| Decisión | Elección |
|---|---|
| Pricing | GTM sin Esencial — Pro/Business/Business XL únicamente |
| Destinatario del doc | Felipe específicamente (no genérico) |
| Sección equity | Integrada con marca CONFIDENCIAL en el mismo HTML |
| Formato | HTML standalone Kitchat (no PDF CreActive) |

### GOTCHAs nuevos

- **CLAUDE.md del proyecto desactualizado:** El Charakato ya es el tercer tenant (seed 20260421) pero el `CLAUDE.md` de white-cassini solo lista Padrino + Soli Sushi en la tabla §8. Actualizar en próxima sesión técnica.
- **Drift costo Anthropic:** $0.0013 (pitch-platanus-2026.md) vs $0.0025 (estado.md). El número correcto para Haiku 4.5 debe verificarse con logs reales. No citarlos como hecho en comunicaciones externas hasta medir.
- **estado.md del proyecto desactualizado:** El archivo `estado.md` en el repo local tiene fecha 2026-04-15 — está muy desactualizado vs el estado real. Actualizar en próxima sesión técnica.

---

## Sesión 2026-04-20 — Plan maestro 3 sesiones + Preflight + Merge Sprint 5

### Completado

**Plan maestro:**
- Plan de 3 sesiones diseñado y aprobado: `~/.claude/plans/trabajaremos-en-white-cassini-elegant-dahl.md`
- Orden confirmado: Sesión 2 → Sesión 1 → Sesión 3 (invertido del original por dependencias)

**Preflight — Commits `f4f2b0a` y `8f58030` pusheados a main:**
- `kapso-feedback-scheduler`: reescritura mayor (enviado+entregado, ventana 24h, cleanup, retryable)
- `kapso-conversations`: per_page=50 → per_page=100
- `kapso-send`: template order_accepted — "aprox. X min" → "X min aproximadamente"
- `supabase/migrations/20260415_feedback_scheduler_fixes.sql`: commiteada (pg_cron + índice + cron job)
- `CLAUDE.md`: documentación actualizada
- `docs/kitchat-landing-brief.md` + `docs/kitchat-gtm-report.md` + `estado.md`: commiteados

**Sesión 2 — Sprint 5 mergeado:**
- Build 0 errores TS verificado en worktree
- QA 7/7 puntos pasados en Vercel preview (El Padrino + Soli Sushi)
- PR #2 creado y mergeado — commit `97704fa` en main
- Nueva UI en producción: `https://white-cassini-sigma.vercel.app`

**Backlog:**
- BKL-01 agregado a `estado.md`: foto de categoría editable desde admin (campo `imagen_url` en `categorias` + upload en `CategoriesTab`)

### Próximo paso exacto — Sesión 1: Review Flow Automático

Ejecutar plan `~/.claude/plans/rippling-wondering-fern.md` completo:
1. Migración SQL (`20260416_review_flow.sql`) — 9 columnas + tabla `pedido_review_turns`
2. Secret `ANTHROPIC_API_KEY` en Supabase
3. Edge Functions nuevas: `review-classifier` + `kapso-review-flusher`
4. Modificar: `kapso-send`, `kapso-feedback-scheduler`, `kapso-webhook`
5. Admin UI: `SettingsPage`, `OrdersPage`, `OrderDetailModal`
6. Checklist 15 pasos del plan (seguridad + anti-regresión)

---

## Sesión 2026-04-20 (segunda tarde) — Sesión 1: Review Flow Automático COMPLETADO

### Completado

**Commits pusheados a main:**
- `2903779` — feat: Review Flow Automático Post-Entrega (main commit)
- `29fc787` — chore: update CLAUDE.md con nuevas funciones

**DB (migración aplicada vía Management API):**
- 10 columnas nuevas en `pedidos`: `review_prompt_sent_at`, `review_sentiment`, `review_topics`, `review_needs_escalation`, `review_completed_at`, `review_resolved_at`, `review_classifier_calls`, `review_pending_message`, `review_pending_since`, `review_response`
- Tabla `pedido_review_turns` creada con RLS (owner + service_role bypass)
- 2 índices: `idx_pedidos_review_buffer_ready` (flusher), `idx_pedidos_awaiting_review` (webhook)

**Edge Functions — todas deployadas con `--no-verify-jwt`:**
- `review-classifier`: Claude Haiku 4.5, hard cap 3 turnos (code-enforced), circuit breaker `review_classifier_calls >= 4`, anti-injection XML tags
- `kapso-review-flusher`: debounce 30s, optimistic concurrency, usa `supabase.functions.invoke`
- `kapso-send`: nuevo type `custom_text` (texto directo sin template)
- `kapso-feedback-scheduler`: delay configurable per-restaurant (`feedback_delay_minutes`), registra turno inicial en `pedido_review_turns`, setea `review_prompt_sent_at`
- `kapso-webhook`: router review antes del welcome — buferea mensajes en `review_pending_message`

**Infraestructura:**
- `ANTHROPIC_API_KEY` secret guardado en Supabase (nunca en código)
- pg_cron `kapso-review-flusher-tick` registrado (jobid 2, `* * * * *`)
- pg_cron `kapso-feedback-scheduler-tick` sigue activo (jobid 1, `*/15 * * * *`)

**Admin UI (deployará en próximo push Vercel):**
- `SettingsPage.jsx`: campos `google_review_url` + `feedback_delay_minutes` bajo toggle Encuesta Post-Entrega
- `OrdersPage.jsx`: badge 👍/👎 en KanbanCard según `review_sentiment`
- `OrderDetailModal.jsx`: sección "Review del cliente" con bubbles de conversación, chips de topics, botón "Marcar resuelto"

### Pendiente inmediato (para que el review flow funcione en prod)
1. **El Padrino:** Configurar en SettingsPage → Integraciones → Encuesta Post-Entrega:
   - `google_review_url`: URL de Google Reviews de El Padrino
   - `feedback_delay_minutes`: 60 (default)
   - Toggle: activado
2. **QA del flujo:** Esperar un pedido real en El Padrino → verificar que a los 60 min llega el WA de review → responder → ver clasificación en dashboard
3. **Bug #3.2** (mensajes automáticos Kapso): Diagnóstico pendiente. Ver logs de `kapso-send` en Dashboard. El fix del scheduler ahora SERÍA visible si #3.2 se resuelve.

### Próximo paso exacto — Sesión 3: Multi-sucursal + Kitcha Landing

1. **Sesión 3A:** Multi-sucursal — ventana mantenimiento + backup DB + tabla `locations` + `location_id` en 6 tablas + customer app `?sede=` + admin `LocationsPage`. Plan: `~/.claude/plans/sequential-strolling-cerf.md`
2. **Sesión 3B:** Kitcha Landing desde cero con `/pro-prd-landing` → insumos en `docs/kitchat-landing-brief.md` + `docs/kitchat-gtm-report.md`
