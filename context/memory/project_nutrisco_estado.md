---
name: Nutrisco MVP y Landing — estado
description: Estado 2026-04-28. DSv3 Fase 4.1 dashboard en working tree (SIN commit — git reset --soft pendiente). Próximo: git add 3 archivos + commit + npm run build + QA /scraps/ds-preview + Fase 4.2 check-in.
type: project
originSessionId: 7d9a5c0d-df85-44b3-9f21-a852c1b2ac9d
---

## Design System v3 — Sesión 4 (2026-04-28)

### Fase 4.1 — Dashboard — ⚠️ CÓDIGO LISTO, COMMIT PENDIENTE

**Estado git:** HEAD en `e1caab5`. Tres archivos modificados en working tree sin commitear.
`git reset --soft e1caab5` ya ejecutado — árbol volvió a completo.

**Archivos modificados (sin commit):**
- `app/src/app/(app)/dashboard/page.tsx` — 8ª query `users.escudos_disponibles` → `shields`. `habitChain: WeekDays` calculado desde `lunesSemana` + `energiaRows.adherencia`. Props `shields` y `habitChain` pasados al Client.
- `app/src/app/(app)/dashboard/dashboard-client.tsx` — Header con `<StreakPill days={streak} shields={shields}>` + `<ProgressRing done={completadasHoy.length} total={5} size={52}>`. Botón "Lo comí" → `variant="success"`. Fire-and-forget en QuickCheckin. `<HabitChain days={habitChain}>` al pie.
- `app/src/app/(app)/_components/app-shell.tsx` — FAB chat overlay eliminado (~60 líneas). Sidebar → `<Link href="/soporte">` "Hablar con Constanza". SoporteChat/Sparkles/ChatOverlay removidos.

**TypeScript:** `tsc --noEmit` exit 0. Build NO ejecutado (bloqueo git).

**Primera acción de la próxima sesión:**
```bash
cd .../Nutrisco
git add "app/src/app/(app)/_components/app-shell.tsx" \
        "app/src/app/(app)/dashboard/dashboard-client.tsx" \
        "app/src/app/(app)/dashboard/page.tsx"
git commit -m "feat(dashboard): DSv3 fase 4.1 — StreakPill + ProgressRing + HabitChain + eliminar FAB"
git ls-tree --name-only HEAD  # verificar árbol completo
npm run build
```

**Gotchas de Sesión 4:**
- 3 builds paralelos = OOM → git add corrompe tree del commit. Nunca lanzar >1 build simultáneo.
- Verificar `git ls-tree --name-only HEAD` tras cada commit — árbol incompleto es silencioso.
- `energiaRows` query extendida a `select("fecha, energia, adherencia")` — necesario para habitChain.
- ProgressRing valor estático del servidor (no live) — aceptado para Fase 4.1.

---

## Design System v3 — Sesión 3 (2026-04-27)

### Fase 3 — Retention components + backend — ✅ COMPLETADO
**Commit:** `e1caab5` — feat(retention): DSv3 fase 3 — componentes retención + lib/streaks + cron

**No se necesitó migración nueva** — `20260424000000_retention_v3.sql` ya tenía todo:
- `users.escudos_disponibles` (0-4), `users.racha_pausa_hasta`, `users.ultimo_escudo_ganado_at`
- Tabla `hitos_desbloqueados` con RLS
- RPCs `otorgar_escudo_si_aplica` + `usar_escudo` (SECURITY DEFINER)

**Componentes creados (10 nuevos):**
- `_components/streak-pill.tsx` — `{days, shields}` inglés, font-mono, sandia + celeste
- `_components/habit-chain.tsx` — adopta `"miss"` del V3 (no `"pending"`), Tailwind inline
- `_components/shield-badge.tsx` — lucide Shield icon, bg-celeste/10
- `_components/milestone-medal.tsx` — conic-gradient ambar→sandia, 3 sizes
- `_components/milestone-modal.tsx` — fullscreen intersticial, copy para 7/14/30/60/90 días
- `_components/phase-countdown-banner.tsx` — bg-ambar/8, usa Chip ambar
- `dashboard/progress-ring.tsx` — SVG ring V3 adaptado (font-mono en lugar de Inter)
- `dashboard/return-ladder.tsx` — 3 micro-steps (📋🥗🔥), bg-celeste/8
- `plan/meal-dots.tsx` — `MealDot + MealDots`, 5 estados: done/active/upcoming/missed/rest
- `progreso/weekly-recap-card.tsx` — Link → /progreso, adherencia% + energía avg

**Backend creado:**
- `lib/streaks.ts` — `incrementStreak` (RPC + milestones), `consumeShield`, `getStreakData`
- `api/streaks/increment/route.ts` — POST autenticado
- `api/cron/streaks/route.ts` — GET protegido, auto-consume shields para ausentes
- `vercel.json` — cron `55 2 * * *` (23:55 Chile = 02:55 UTC)
- `checkin-form.tsx` — fire-and-forget `fetch("/api/streaks/increment")` tras check-in exitoso

**Build:** ✓ exit code 0 · 27+ rutas · 0 errores TypeScript

### Gotchas de Sesión 3
- **`HabitChain` usa `"miss"`** (adoptado del V3 — más semántico que "pending")
- **`StreakPill` usa inglés** `{days, shields}` — el V3 `StreakShield` en el worktree usa español. Coexisten sin problema — no hay conflicto de nombres.
- **`otorgar_escudo_si_aplica` requiere `auth.uid()`** — solo funciona desde Route Handlers (no crons service-role). El cron usa UPDATE directo con service role.
- **`/scraps/ds-preview` sigue pendiente de QA visual** — Oscar debe abrirla en dev server y borrarla tras aprobar.

---

## Design System v3 — Sesión 2 (2026-04-27)

### Fase 2 — UI library v3 — ✅ COMPLETADO (2026-04-27)
**Commit:** `6271dd5` — feat(ui): DSv3 fase 2 — Chip, ConstanzaAvatar, Button success

**Archivos creados/modificados:**
- `app/src/components/ui/chip.tsx` — 6 tones (neutral/sandia/celeste/verde/ambar/solid), font-mono uppercase, pill shape. Texto celeste/verde/ambar oscurecido para WCAG AA: `#4A9CC5`, `#5A8D62`, `#B87D28`
- `app/src/components/ui/constanza-avatar.tsx` — celeste gradient (`from-celeste to-[#5BAED1]`), "C" en Playfair serif, 4 tamaños sm/md/lg/xl
- `app/src/components/ui/button.tsx` — `variant="success"` agregado (verde gradient + `shadow-verde/30`)
- `app/src/app/scraps/ds-preview/page.tsx` — página QA visual temporal en `/scraps/ds-preview` (eliminar tras aprobación visual de Oscar)

**Build:** ✓ exit code 0 · 27+ rutas · 0 errores TypeScript

**QA pendiente:** Oscar debe abrir `/scraps/ds-preview` en dev server y aprobar visual antes de continuar. Eliminar la página tras aprobación.

### Gotchas nuevos (Sesión 2)
- **Build lento (~6 min)** — 5 procesos notebooklm-mcp corriendo al 65% CPU. No es bug del código. Usar `tsc --noEmit` primero para validación rápida de TypeScript.
- **`next build | tail -20` no escribe al output file hasta que termina** — el archivo aparece vacío durante la ejecución. Usar TaskOutput con block=true para esperar.
- **V3 HabitChain usa `"miss"` (no `"pending"`)** — el DSv3 spec dice `"pending"` pero el V3 worktree usa `"miss"`. En Fase 3 hay que decidir cuál adoptar como canónico.
- **V3 StreakShield tiene `{dias, escudos}` (español)** — el DSv3 spec usa `{days, shields}` (inglés). Reconciliar en Fase 3 antes de importar.

---

## Design System v3 — Sesión 1 (2026-04-27)

### Bundle DSv3 leído e implementado
- Bundle en `Documentacion/DSv3 Nutrisco/project/` — README + Design System.html + design-system/{tokens,components,retention-loops,screens,perfil-comunidad}.jsx
- Plan 5 fases / 9 sesiones aprobado → `~/.claude/plans/read-the-users-oz-documents-cas-ceo-crea-steady-corbato.md`

### Fase 1 — Tokens v3 — ✅ COMPLETADO (2026-04-27)
**Commit:** `8bef2fe` — feat(tokens): DSv3 fase 1 — verde, ambar, JetBrains Mono
**Branch:** `main` (NO worktree)
**Archivos modificados:**
- `app/tailwind.config.ts` → `colors.verde = "#7BAE83"`, `colors.ambar = "#E5A23C"`, `fontFamily.mono`
- `app/src/app/layout.tsx` → `JetBrains_Mono` importado, `--font-mono` inyectado en `<html>`
**Build:** ✓ Compiled successfully · 0 errores TypeScript · `tsc --noEmit` limpio

### Decisiones confirmadas por el usuario
1. **Soporte IA:** mantener streaming Haiku 4.5. Solo eliminar el FAB chat overlay del app-shell.tsx
2. **Comunidad v3:** postergar a sesión futura — NO tocar `comunidad-client.tsx` en esta migración
3. **Cadencia:** una fase por sesión con QA entre cada una

### ⚠️ GOTCHA CRÍTICO — Colisión V3 branch vs DSv3
El branch `feature/ux-v3-enhanced` (PR #1, 25 commits, 55 rutas) ya tiene muchos de los componentes que el plan DSv3 marca como "nuevos":
- `components/ui/progress-ring.tsx` ← ya existe (vs DSv3 `dashboard/progress-ring.tsx`)
- `components/ui/streak-shield.tsx` ← ya existe (vs DSv3 `_components/streak-pill.tsx`, diferente nombre y spec)
- `components/ui/habit-chain.tsx` ← ya existe
- `components/ui/mono-label.tsx` ← ya existe
- `components/ui/hydration-bar.tsx` ← ya existe
- Migración `20260424000000_retention_v3.sql` YA APLICADA en remoto (columns `escudos_disponibles`, `racha_pausa_hasta`, RPC `otorgar_escudo_si_aplica`, `usar_escudo`, tabla `hitos_desbloqueados`)

**Implicación:** En Fase 3 (retention components + backend) hay que revisar el worktree `.worktrees/nutrisco-v3/` ANTES de crear componentes nuevos. El DSv3 (2026-04-27) es la spec definitiva; el V3 branch (2026-04-24) es la implementación previa que puede reutilizarse o ajustarse.

También: los tokens `verde`, `ambar`, `sandia-tint`, `celeste-tint`, `verde-tint` ya existen en el tailwind.config.ts del V3 branch. Los que acabo de agregar a `main` son un subset de esos.

### Próxima sesión (Fase 3 — Retention components + backend)
**Primera acción:** Auditar V3 worktree en detalle: leer `habit-chain.tsx`, `progress-ring.tsx`, `streak-shield.tsx` del worktree para decidir reusar vs recrear. Verificar qué columnas tiene `retention_v3.sql` ya aplicado.
**Objetivo:** Crear todos los retention components + `lib/streaks.ts` + migración streaks (solo lo que falta tras auditoría) + cron diario
**Advertencia:** `migration 20260424000000_retention_v3.sql` ya está aplicada en remoto — NO crear tabla `streaks` duplicada. Verificar con `mcp__supabase__list_tables` primero.
**QA previo requerido:** Oscar debe aprobar `/scraps/ds-preview` visualmente y eliminar la página antes de empezar Fase 3.

## UX Comunidad Chat-Style — 2026-04-24 (sesión 2)

### Commits
- `3a2d201` — fix(comunidad): InputBar siempre visible — posición fixed sobre la nav
- `beeb4de` — feat(comunidad): chat-style UX — sticky tabs, newest-at-bottom, thinner input, hide FAB
- **Ambos pusheados → Vercel auto-deploy triggerado**

### Cambios implementados
| Feature | Detalle |
|---------|---------|
| TabsFiltro + PinnedBar sticky | `sticky top-14 lg:top-0 z-10 bg-white` — siempre visibles al scrollear |
| Mensajes orden chat | `.reverse()` en render: más antiguo arriba, más reciente abajo (cerca del InputBar) |
| Auto-scroll al fondo | Mount + tab change + post → `setTimeout(() => window.scrollTo(0, document.body.scrollHeight), 0)` |
| Scroll preservation | Al cargar mensajes más antiguos: guarda `prevScrollHeight`, ajusta con `scrollBy(delta)` después |
| Sentinel al top | Sentinel movido al inicio del feed — scroll UP = cargar mensajes más antiguos |
| InputBar más delgada | `rows=1`, `minHeight=36px` (era rows=2, 48px) — crece hasta 4 filas al escribir |
| FAB IA oculto en /comunidad | `usePathname()` en AppShell → `{pathname !== '/comunidad' && <FAB />}` |

### Gotchas nuevos
- **`sticky top-14` para TabsFiltro mobile** — AppShell header = h-14 (56px). `lg:top-0` porque el header es `lg:hidden`.
- **`setTimeout(..., 0)` para scroll-to-bottom** — mejor que `requestAnimationFrame` porque garantiza que React flusheó el DOM antes de medir `document.body.scrollHeight`.
- **Top sentinel + scroll preservation** — con mensajes más recientes abajo, el sentinel va arriba. Al cargar más antiguos, se preserva la posición: `prevScrollHeight` antes, `scrollBy(delta)` después en `setTimeout`.
- **`usePathname()` en AppShell** — limpio y sin overhead. No requiere prop drilling ni context.

---

## Bug Fix Comunidad InputBar — 2026-04-24 (sesión 1)

### Commit
- `3a2d201` — fix(comunidad): InputBar siempre visible — posición fixed sobre la nav

### Causa raíz
`AppShell` usa `min-h-screen` (= `100vh`, iOS large viewport). Mismatch `100vh` vs `100dvh` en iOS Safari (64px) hacía que el InputBar quedara debajo del fold o tapado por la nav.

### Solución
InputBar `position: fixed` con `bottom: calc(3.5rem + env(safe-area-inset-bottom, 0px))`. Spacer `h-36` al final del feed.

### Gotcha clave
**`min-h-screen` + cualquier `h-[calc(100dvh-X)]` en iOS → siempre overflow.** Para layouts chat mobile, única solución confiable = `position: fixed` en el input.

---

## App SaaS (Nutrisco)

**DB:** Supabase `kkkqpkyltekphrurjzwp` — 26 pautas, 84 recetas, 52 FAQ.
**Repo:** `creactive-dev/nutrisco` — branch `main` → Vercel auto-deploy.
**Dev server (main):** `cd app && /opt/homebrew/opt/node@20/bin/node node_modules/.bin/next dev`
**Dev server (V3):** `cd .worktrees/nutrisco-v3/app && /opt/homebrew/opt/node@20/bin/node node_modules/.bin/next dev`
**Worktree V3:** `.worktrees/nutrisco-v3/` → branch `feature/ux-v3-enhanced`
**PR:** https://github.com/creactive-dev/nutrisco/pull/1 — **NO mergear** hasta demo con Constanza

---

## Sprint V3 UX Enhanced — COMPLETADO (2026-04-24)

**Branch:** `feature/ux-v3-enhanced` · 25 commits · Build: 55 rutas, 0 TS errors
**Worktree:** `.worktrees/nutrisco-v3/` — `.env.local` ya copiado al worktree

### Pantallas rediseñadas (V3)
| Pantalla | Cambio clave |
|---|---|
| `/dashboard` | ProgressRing + StreakShield + AhoraCard (one-tap log) + HabitChain |
| `/checkin` | Carrusel 3 pasos, slider 0-100, saltar con escudo, toast celebración |
| `/plan` | Hero "Hoy" con dots, selector días, chip CAMBIAR (modal stub), sticky shopping |
| `/progreso` | Antes-vs-Hoy comparator, recap banner, ConstanzaInsightCard |
| `/soporte` | Mensaje proactivo contextual + 4 chips, badge uso N/M |
| `/suscribirse` | Pill social proof, preview día 1, borde sandia, garantía 14d, footer 24h |

### Pantallas nuevas
- `/hito/[dias]` — medalla gradiente, delta stats (kg, fatiga, hinchazón, adherencia), share WhatsApp, marca compartido_at
- `/retorno` — bienvenida cálida, card racha protegida, usar escudo, ladder 3 pasos

### Backend nuevo (en worktree)
- Migration `20260424000000_retention_v3.sql` — **YA APLICADA en remoto** (supabase db push)
  - `users.escudos_disponibles int DEFAULT 1 CHECK (0..4)`
  - `users.racha_pausa_hasta date`
  - `users.ultimo_escudo_ganado_at timestamptz`
  - Tabla `hitos_desbloqueados` con RLS
  - RPC `otorgar_escudo_si_aplica(p_user)` — SECURITY DEFINER + auth guard
  - RPC `usar_escudo(p_user, p_dias)` — SECURITY DEFINER + auth guard
- Cron hitos extendido: `[7, 14, 30, 60, 90, 180]` + idempotencia via `hitos_desbloqueados`
- API `/api/retorno/estado` — GET detecta ausencia ≥3 días
- API `/api/retorno/usar-escudo` — POST consume escudo + actualiza last_active_at
- `streak.ts`: considera `racha_pausa_hasta` (días protegidos no rompen racha)

### Nuevos primitivos UI
- `components/ui/progress-ring.tsx` — SVG ring con accesibilidad
- `components/ui/streak-shield.tsx` — pill 🔥 días + ◆ escudos
- `components/ui/habit-chain.tsx` — 7 celdas L-M-M-J-V-S-D
- `components/ui/mono-label.tsx` — label uppercase 10px tracking
- `components/ui/hydration-bar.tsx` — 8 dots llenos/vacíos

### Tokens nuevos en tailwind.config.ts (V3)
`verde`, `ambar`, `sandia-tint`, `celeste-tint`, `verde-tint`, `surface-paper`, keyframe `celebration-burst`

### Gotchas V3
- **zsh + git add con paths `(app)`** → siempre usar quotes: `git add "app/src/app/(app)/..."` (sin quotes falla silenciosamente con "no matches found")
- **RPC `usar_escudo` retorna boolean** — `true` = consumido, `false` = sin escudos. NO lanza excepción para el caso "sin escudos". El código debe checar `data`, no `error`.
- **`deltaEnergia` era fatiga renombrada** — los quincenales no tienen campo `energia` numérico (solo `energia_comparada: string`). El stat de fatiga se muestra como `−N pts fatiga`, no "energía".
- **Adherencia date-scoped** — la fórmula usa `.gte("fecha", cutoffStr)` para el período del hito, no LIMIT 30 genérico.
- **setTimeout en Client Components** → siempre limpiar con `useRef` + cleanup effect para evitar leak en unmount.
- **Token `verde-tint: "#F0FBF4"`** agregado a tailwind.config (estaba hardcodeado inline, el reviewer lo detectó).

### Para la demo — seedear en Supabase
```sql
-- Pantalla Hito
INSERT INTO hitos_desbloqueados (user_id, hito_dias)
VALUES ('<uid>', 14) ON CONFLICT DO NOTHING;

-- Pantalla Retorno
UPDATE users SET last_active_at = now() - interval '5 days'
WHERE email = 'hola@creactivestudio.agency';
```

### Pendiente post-demo
- [ ] Demo con Constanza → decisión merge V3 → main
- [ ] Swap de comida real (flujo completo con 3 alternativas)
- [ ] Share card generador de imágenes (WhatsApp/IG 1080×1920)
- [ ] A/B test check-in slider vs emojis (necesita analytics)
- [ ] Sidebar streak display: actualizar con StreakShield (out of scope en V3, pendiente si se mergea)

---

---

## Fases completadas en código

| Fase | Features clave |
|------|----------------|
| Servicio Primera Clase Fase 1 | `voz.ts` fuente única copy · Resend client · 6 crons · email bienvenida · `/procesando` con delay 24h · nota Constanza en ajuste · notificaciones al responder ticket |
| Servicio Primera Clase Fase 2 | Cola alertas `/nutricionista/alertas` · cron detectar-sintomas · trigger caso clínico · inbox `/perfil/inbox` · perfil editable (alergias + exclusiones) · tarjeta Constanza en dashboard · badge notificaciones unread |
| Servicio Primera Clase Fase 3 | `lib/mercadopago/client.ts` · webhook `/api/webhooks/mercadopago` (HMAC-SHA256) · paywall `/suscribirse` · gate suscripción en `(app)/layout.tsx` |
| Oleada Beta 1.x-3.x | max_tokens soporte · resumen quincenal · Índice Antiinflamatorio · Racha visual central · memoria chat · diversidad plantas · alertas predictivas · hitos semana 1-2 · cron cerrar-semana · persistencia screening · lista compras Supabase · insights /procesando · Google login · Embudo beta nutricionista |
| **Módulo Comunidad (2026-04-20)** | Feed interno · reacciones emoji · replies · pin · alias · Realtime · push PWA · nav 6 ítems · rutas paciente + nutricionista |

---

## QA Task 13 — BUGS FIXEADOS (2026-04-22 sesión 5)

### Commit
- `74a30f6` — fix(comunidad): 5 bugs QA — pin, reply doble, reacciones +2, imagen click, categoría tab

### Build
- `tsc --noEmit` → 0 errores ✅ (confirmado al cierre de sesión)
- Push a `main` → Vercel auto-deploy en curso

### Resultados QA por bloque

**Bloque 1 — Setup básico** ✅
- Alias guardado persiste al reload — OK
- Publicar texto → aparece en feed via Realtime — OK

**Bloque 2 — Features del feed** ✅ (con bugs fixeados)
- Imagen: upload + preview OK; abrir al click → **FIXEADO** (`<a target="_blank">`)
- Categoría: badge + filtro tab → **FIXEADO** (prop `activeTab` en InputBar)
- Reacciones toggle (+1/-1) → **FIXEADO** (skip Realtime update si `user_id === currentUser.id`)
- Reply inline → **FIXEADO** (dedup por `reply.id` en handler Realtime)
- "Ver N respuestas" → detalle: OK
- Tabs Logros/Recetas/Dudas → filtra con # o con tab: OK

**Bloque 3 — Permisos** ✅
- Pin desde app → **FIXEADO** (typo `mensajeId` → `mensaje_id`)
- Delete mensaje ajeno (nutricionista): OK
- Paciente sin 📌/✕ en ajenos: OK

**Bloque 4 — Notificaciones** ✅ COMPLETADO (sesión 6, 2026-04-22)
- Push permission banner: OK
- Aceptar → row en `push_subscriptions`: OK
- Badge bell icon se incrementa y se limpia al abrir inbox: OK
- Push web notification llega al navegador/PWA: OK (tras 2 bugs fixeados — ver abajo)

### 5 bugs fixeados — detalle técnico

| Bug | Causa raíz | Archivos |
|-----|-----------|---------|
| Pin | `mensajeId` en body, API esperaba `mensaje_id` | `MensajeBubble.tsx` |
| Reply doble | Optimistic + Realtime sumaban el mismo reply | `comunidad-client.tsx` |
| Reacciones +2 | Optimistic + Realtime sumaban el mismo emoji | `comunidad-client.tsx` |
| Imagen sin click | `<img>` sin enlace | `MensajeBubble.tsx` |
| Categoría tab | InputBar sin `activeTab` prop | `InputBar.tsx` + `comunidad-client.tsx` |

### Gotchas nuevos (2026-04-22 sesiones 5 y 6)
- **Patrón doble-conteo Realtime:** Cualquier entidad con optimistic UI + Realtime necesita dedup. Para contadores: skip si `user_id === currentUser.id`. Para arrays: dedup por id. Reviewar si afecta otras tablas en el futuro.
- **TypeScript no detecta key typos en fetch body** — el cast `as unknown` hace invisible el bug de `mensajeId` vs `mensaje_id`. Siempre comparar keys del body con los que espera la API route.
- **Supabase nested SELECT solo trae los campos listados explícitamente** — `push_subscriptions(endpoint)` devuelve solo `endpoint`; `p256dh` y `auth` llegan `undefined` → push falla silenciosamente. Siempre listar todos los campos necesarios: `push_subscriptions(id, endpoint, p256dh, auth)`.
- **`notificaciones.origen` tiene CHECK constraint** — solo acepta `'sistema'`, `'constanza'`, `'cron'`. Usar `'test_manual'` lanza ERROR 23514. Para pruebas manuales usar `'cron'`.
- **VAPID keys faltaban del checklist pre-deploy** — estaban en `.env.local` pero no en Vercel. El cron fallaba silenciosamente (webpush recibía undefined). Agregadas a Vercel en esta sesión (2026-04-22). Añadir al checklist de futuros proyectos con push.

---

## QA Task 13 — PENDIENTE ANTERIOR (referencia histórica)

### Estado del build
- `572396e` deployado en Vercel (main). tsc 0 errores.
- Commits de esta feature: `9284e4e` (módulo) + `397b43a` (crash fix) + `572396e` (mobile fix)

### Checklist completo (ejecutar en `app.constanzanutricion.cl`)

**Bloque 1 — Setup básico**
- [ ] `/comunidad` carga sin error
- [ ] Alias onboarding modal aparece si alias es null
- [ ] Guardar alias → modal cierra, InputBar visible
- [ ] Publicar texto → aparece en feed (Realtime)
- [ ] Reload → InputBar visible SIN modal (alias persistido) ⚠️ si reaparece = RLS issue

**Bloque 2 — Features del feed**
- [ ] Publicar con imagen ≤5MB → upload OK, preview OK
- [ ] Publicar con categoría → badge en el mensaje
- [ ] Reaccionar → counter +1, emoji resaltado
- [ ] Desreaccionar → counter -1
- [ ] Reply inline → preview aparece bajo el mensaje
- [ ] 3+ replies → "Ver N respuestas" → navega a `/comunidad/mensaje/[id]`
- [ ] Tab Logros / Recetas / Dudas → filtra correctamente
- [ ] Tab Todos → feed completo

**Bloque 3 — Permisos (nutricionista = Constanza)**
- [ ] Pin → PinnedBar aparece arriba
- [ ] Despin → PinnedBar desaparece
- [ ] Delete mensaje ajeno → desaparece del feed
- [ ] Paciente: sin 📌 en mensajes ajenos
- [ ] Paciente: sin ✕ en mensajes ajenos

**Bloque 4 — Notificaciones**
- [ ] Push permission banner aparece en primer visita (browser nuevo)
- [ ] Aceptar → row en `push_subscriptions`
- [ ] Badge bell icon se incrementa (insertar fila manual en `notificaciones` para testear)

### Nota sobre nav badge
El nav item "COMUNIDAD" NO tiene badge rojo. Las notificaciones de `comunidad_mensajes_nuevos` van al bell icon del header (tabla `notificaciones`, campo `tipo='comunidad_mensajes_nuevos'`).

### Pendiente si alias modal reaparece al reload
Investigar RLS UPDATE en `users.alias_comunidad`:
- Policy `users_own_profile FOR ALL USING (auth.uid() = id)` debería cubrir UPDATE
- Verificar en Supabase Dashboard → Auth → Policies → tabla `users`
- Si falla: agregar policy explícita `FOR UPDATE USING (auth.uid() = id) WITH CHECK (auth.uid() = id)`

---

## Fix Crash Comunidad — COMMITEADO (2026-04-20 sesión 3)

### Commit
- `397b43a` — fix(comunidad): unwrap API responses en fetchPage y InputBar

### Bugs corregidos
- **InputBar.tsx** leía `res.json() as ComunidadMensaje` pero POST `/api/comunidad/mensajes` devuelve `{ mensaje: ComunidadMensaje }`. Wrapper pasado a MensajeBubble → `mis_reacciones` undefined → `.filter` crash.
- **comunidad-client.tsx `fetchPage`** leía `res.json() as ComunidadMensaje[]` pero GET devuelve `{ mensajes, nextCursor }`. `setMensajes(objeto)` → `mensajes.filter` no es función al cambiar tabs.

### Gotcha
- TypeScript `as` castings no detectan mismatches en runtime. Siempre usar destructuring: `const { mensajes } = await res.json()`.

### QA Task 13 — estado al cierre de sesión
- ✅ Deploy Vercel confirmado "Ready"
- ✅ `/comunidad` carga → modal alias aparece
- ✅ Alias guardado → modal cierra
- ✅ Publicar mensaje texto → fix deployado (no testeado post-fix aún)
- ⏳ Resto del checklist pendiente:
  - Publicar mensaje con imagen
  - Reacciones (toggle + contador)
  - Reply inline
  - "Ver N respuestas" → detalle
  - Tabs Logros/Recetas/Dudas
  - Pin (nutricionista)
  - Delete (nutricionista any / paciente own)
  - RLS: paciente NO puede pin/delete ajeno
  - Badge nav `comunidad_mensajes_nuevos`
  - Push Permission banner
  - Aceptar notif → fila en `push_subscriptions`

### Pendiente adicional a investigar
- Si InputBar sigue sin aparecer al recargar (alias null en DB a pesar de éxito aparente): verificar RLS UPDATE en tabla `users` para `alias_comunidad`. La policy `users_own_profile FOR ALL USING (auth.uid() = id)` debería cubrir UPDATE, pero si falla silenciosamente (0 rows, sin error), el alias no persiste.

---

## Módulo Comunidad — COMMITEADO Y EN DEPLOY (2026-04-20 sesión 2)

### Commits de esta sesión
- `9284e4e` — feat(comunidad): módulo comunidad completo — feed, realtime, push PWA (34 archivos, 3667 líneas)
- `51db206` — fix(crons): push-comunidad a diario (Hobby plan no permite sub-diario)

### Gotchas adicionales descubiertos
- Subagente sesión anterior creó ghost dir `src/app/\(app\)/` (backslashes literales) — causaba error Tailwind ENOENT en build local. Fix: `rm -rf "src/app/\\(app\\)/"`.
- Vercel Hobby plan: crons máximo 1 vez/día. `0 * * * *` bloquea el deploy → cambiado a `0 12 * * *`.
- Los archivos existían en filesystem local pero nunca en git — el Módulo Comunidad no estaba desplegado aunque `tsc --noEmit` pasaba.
- Local `npm run build` timeout en "collecting page data" para rutas `/api/ia/*` es normal (sin network a Anthropic). En Vercel no ocurre.

## Módulo Comunidad — COMMITEADO (2026-04-20 sesión 1)

### Archivos creados/modificados

**Migración:**
- `supabase/migrations/20260420000000_comunidad.sql` — 4 tablas + RLS + Realtime + bucket comunidad
- `supabase/migrations/20260420000002_comunidad_policy_fixes.sql` — fixes RLS nombre policies + delete reacciones nutricionista

**TypeScript:**
- `src/lib/types/comunidad.ts` — tipos ComunidadMensaje, ComunidadRespuesta, EmojiReaccion, etc.

**API Routes:**
- `src/app/api/comunidad/mensajes/route.ts` — GET (feed paginado cursor) + POST
- `src/app/api/comunidad/mensajes/[id]/route.ts` — DELETE (owner o nutricionista)
- `src/app/api/comunidad/replies/route.ts` — POST
- `src/app/api/comunidad/reacciones/route.ts` — POST (toggle)
- `src/app/api/comunidad/pin/route.ts` — PATCH (nutricionista only)
- `src/app/api/comunidad/alias/route.ts` — GET (check) + PUT (guardar)
- `src/app/api/push/subscribe/route.ts` — POST + DELETE
- `src/app/api/cron/push-comunidad/route.ts` — GET (cron horario, in-app + web push)

**Componentes:**
- `src/app/(app)/comunidad/_components/TabsFiltro.tsx`
- `src/app/(app)/comunidad/_components/PinnedBar.tsx`
- `src/app/(app)/comunidad/_components/ReaccionBar.tsx`
- `src/app/(app)/comunidad/_components/ReplyThread.tsx`
- `src/app/(app)/comunidad/_components/MensajeBubble.tsx`
- `src/app/(app)/comunidad/_components/InputBar.tsx`
- `src/app/(app)/comunidad/_components/AliasOnboarding.tsx`
- `src/app/(app)/comunidad/_hooks/useComunidadRealtime.ts`
- `src/app/(app)/_components/PushPermission.tsx`
- `src/lib/push/web-push-server.ts`

**Páginas:**
- `src/app/(app)/comunidad/page.tsx` — Server Component feed principal
- `src/app/(app)/comunidad/comunidad-client.tsx` — Client Component
- `src/app/(app)/comunidad/mensaje/[id]/page.tsx` — detalle con todos los replies
- `src/app/(app)/comunidad/mensaje/[id]/MensajeDetalle.tsx` — client wrapper
- `src/app/nutricionista/comunidad/page.tsx` — ruta espejo Constanza

**Modificados:**
- `src/app/(app)/_components/app-shell.tsx` — 6º nav item (Comunidad + MessageCircle)
- `src/app/(app)/_components/nav-item.tsx` — optional className prop
- `src/app/nutricionista/layout.tsx` — link /nutricionista/comunidad
- `src/app/(app)/layout.tsx` — monta `<PushPermission />`
- `src/app/sw.ts` — handlers push + notificationclick
- `vercel.json` — cron push-comunidad `0 * * * *`
- `.env.local` — VAPID_SUBJECT, VAPID_PUBLIC_KEY, VAPID_PRIVATE_KEY, NEXT_PUBLIC_VAPID_PUBLIC_KEY

**VAPID keys generadas:**
- Public: `BCdMJa9Xqver4SzahZxpE-HacpJCwFmQBy5CbrkqfSjw3lxQArMk-NKydDr4bI4S6GRcVQFQL-sh8MNZ0JwyNug`
- Private: `Vx1EOhKomYL_sDmoxHhKZl9WWqcU9oHROV5EZP4kadg`
- **Agregadas a Vercel** ✅ (Production + Preview)

**Estado deploy:** Deployado en Vercel ✅ — `tsc --noEmit` 0 errores.

### Gotchas del módulo Comunidad

- `comunidad_reacciones` usa **partial unique indexes** — NULL != NULL en Postgres. UNIQUE normal NO funciona con columnas nullable.
- Paleta: `sandia #E94555` (coral), `celeste #73C3E4`. Constanza: `bg-celeste/[0.08] border-l-celeste`.
- `notificaciones.tipo` tiene CHECK constraint → extender con DROP + ADD CONSTRAINT (ya hecho en migración).
- `(app)/layout.tsx` redirige nutricionista → ruta espejo en `/nutricionista/comunidad` (ya creada).
- Realtime primera vez en Nutrisco — patrón: `useRef` para callbacks (evita stale closures en subscriptions).
- MCP Supabase apunta a White Cassini (distinto proyecto) → migraciones Nutrisco via CLI `supabase db push`.
- `DELETE` silently blocked por RLS devuelve `{ ok: true }` si no se usa `{ count: 'exact' }` — bug ya corregido.
- `communidad_reacciones` alias policy: `paciente_insert_*` → renombrado a `authenticated_insert_*` en patch.
- PushPermission: `urlBase64ToUint8Array` con loop for (no spread) para evitar error TS downlevelIteration. `applicationServerKey: array.buffer as ArrayBuffer`.
- `NEXT_PUBLIC_VAPID_PUBLIC_KEY` marcada como Sensitive en Vercel — funcionará igual en runtime aunque no sea visible.

---

## Crons (vercel.json) — 7 total — ACTUALIZADO

| Path | Schedule | Propósito |
|------|----------|-----------|
| `/api/cron/entregar-planes` | `0 12 * * *` | Entrega planes |
| `/api/cron/recordar-checkin` | `0 15 * * *` | Recordatorio quincenal día 13 |
| `/api/cron/reengagement` | `0 16 * * *` | Pacientes >10 días sin actividad |
| `/api/cron/hitos` | `0 17 * * *` | Hitos 30/90/180 días |
| `/api/cron/detectar-sintomas` | `0 18 * * *` | Delta síntomas quincenales |
| `/api/cron/cerrar-semana` | `0 22 * * 0` | Email menú nueva semana (domingo) |
| `/api/cron/push-comunidad` | `0 12 * * *` | Web Push notif comunidad (diario — Hobby plan limit) |

⚠️ Si se upgradea a Vercel Pro → cambiar `push-comunidad` a `0 * * * *` para volver a horario.

## Migraciones aplicadas en remoto ✅

- `20260414100000_servicio_primera_clase.sql`
- `20260414200000_caso_clinico_trigger.sql`
- `fix_user_fk_cascade`
- `20260420000000_comunidad.sql` ✅
- `20260420000002_comunidad_policy_fixes.sql` ✅

---

## Deploy Vercel

**Branch:** `main` · Root Directory: `app`
**Env vars configuradas en Vercel:**
- `RESEND_API_KEY` ✅
- `EMAIL_REMITENTE` ✅
- `CRON_SECRET` ✅
- `NEXT_PUBLIC_APP_URL` ✅
- `MP_ACCESS_TOKEN` ✅
- `ANTHROPIC_API_KEY` ✅
- `NEXT_PUBLIC_SUPABASE_URL` ✅
- `NEXT_PUBLIC_SUPABASE_ANON_KEY` ✅
- `SUPABASE_SERVICE_ROLE_KEY` ✅
- `VAPID_SUBJECT` ✅ (2026-04-20)
- `VAPID_PUBLIC_KEY` ✅ (2026-04-20)
- `VAPID_PRIVATE_KEY` ✅ (2026-04-20)
- `NEXT_PUBLIC_VAPID_PUBLIC_KEY` ✅ (2026-04-20)

**Pendiente Vercel:**
- `MP_WEBHOOK_SECRET` → crear webhook en MP Dashboard → `/api/webhooks/mercadopago` → copiar secret

---

## Crons (vercel.json) — 7 total

| Path | Schedule | Propósito |
|------|----------|-----------|
| `/api/cron/entregar-planes` | `0 12 * * *` | Entrega planes |
| `/api/cron/recordar-checkin` | `0 15 * * *` | Recordatorio quincenal día 13 |
| `/api/cron/reengagement` | `0 16 * * *` | Pacientes >10 días sin actividad |
| `/api/cron/hitos` | `0 17 * * *` | Hitos 30/90/180 días |
| `/api/cron/detectar-sintomas` | `0 18 * * *` | Delta síntomas quincenales |
| `/api/cron/cerrar-semana` | `0 22 * * 0` | Email menú nueva semana (domingo) |
| `/api/cron/push-comunidad` | `0 * * * *` | Web Push notif comunidad (horario) |

---

## ✅ QA Task 13 — COMPLETADO AL 100% (2026-04-22)

Todos los bloques verificados. 7 bugs fixeados en 2 sesiones (commits `74a30f6` + `5140ed6`).

## Próxima sesión — Pendientes pre-beta (configuración)

**Todo lo pendiente es configuración externa — NO código:**

| Tarea | Responsable | Urgencia |
|-------|-------------|----------|
| `MP_WEBHOOK_SECRET` en Vercel Dashboard | Oscar | 🔴 Bloquea pagos |
| Google OAuth: Client ID/Secret en Supabase Auth | Oscar | 🟡 |
| WhatsApp link real de Constanza → `procesando-client.tsx` + `perfil/page.tsx` | Constanza | 🟡 |
| SET `estado_suscripcion='trial'` para beta users en Supabase Dashboard | Oscar | 🔴 Bloquea beta |
| Resend dominio `constanzanutricion.cl` verificado | ✅ (2026-04-17) | — |

**Primera acción próxima sesión:** Configurar `MP_WEBHOOK_SECRET` (crear webhook en MP Dashboard → `/api/webhooks/mercadopago` → copiar secret → agregar en Vercel).

---

## Landing Page de Venta (Nutrisco Landing)

**Repo:** https://github.com/creactive-dev/nutrisco-landing
**Ruta local:** `clientes/constanza-nutricion/outputs/nutrisco-landing/`
**Estado:** Build OK. Pendiente: assets de Constanza + deploy Vercel + dominio.

**Assets pendientes de Constanza:**
1. Foto profesional → `public/images/constanza.webp`
2. Testimonios reales del ebook (3-5)
3. Link MP plan $19.990/mes → `NEXT_PUBLIC_MP_PAYMENT_URL`
4. Número WhatsApp Business → `NEXT_PUBLIC_WHATSAPP_NUMBER`
5. Dominio (nutrisco.cl o subdomain)

---

## Patrones críticos del codebase

- RLS recursion fix: `public.current_user_role()` SECURITY DEFINER
- RLS INSERT: siempre `WITH CHECK` además de `USING`
- Tres clientes Supabase: `client.ts` (browser), `server.ts` (RSC/Route), `middleware.ts`
- Node.js v20 requerido (v24 incompatible con Next.js 14)
- Streaming: `anthropic.messages.stream()` → ReadableStream → `\n__META__{json}__META__` al final
- FK cascade: todas las tablas con `user_id` tienen `ON DELETE CASCADE`
- Partial unique indexes para columnas nullable (comunidad_reacciones)
- Realtime: useRef para callbacks en useComunidadRealtime (evita stale closures)
- MCP Supabase apunta a White Cassini → migraciones Nutrisco via `supabase db push` (CLI)
