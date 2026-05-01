---
name: Nutrisco — Servicio al paciente de primera clase (completo en código 2026-04-14)
description: Plan ejecutado íntegramente. Todo el código está en main. Pendiente: configuración externa (Resend DNS, MP webhook, WhatsApp link, beta users trial) + QA pasos 3-7.
type: project
originSessionId: 1fd2a7e0-7f79-4d08-9986-9d2919cb659b
---

**Plan file:** `/Users/oz/.claude/plans/jiggly-orbiting-phoenix.md`

**Estado al EOD 2026-04-14:** TODO el código implementado y en `main`. TypeScript: 0 errores. Pendiente únicamente configuración externa + QA final.

**Why:** La landing vendía "plan personal de Constanza con revisión humana" pero el fix beta había eliminado el delay 24h. Resend sin código. Crons sin configurar. Loops cerrados solo en DB. Los 290 del ebook conocen a Constanza como persona — el gap era el mayor riesgo de churn beta.

---

## Lo que está completo en código

### Fase 1
| Archivo | Qué hace |
|---------|---------|
| `lib/copy/voz.ts` | Fuente única de copy — 9 templates, firma "Constanza", nunca peso |
| `lib/email/resend-client.ts` | `enviarEmail()` + `crearNotificacion()` con retry + fire-and-forget safe |
| `vercel.json` | 6 crons configurados |
| `api/cron/entregar-planes` | Delay 24h — desbloquea planes y envía email planListo |
| `api/cron/recordar-checkin` | Recordatorio quincenal día 13 |
| `api/cron/hitos` | Celebra meses 1/3/6 — deduplicado |
| `api/cron/reengagement` | Inactivos >10 días — anti-spam |
| `api/auth/bienvenida` | Email bienvenida al registro |
| `(onboarding)/procesando/` | Server Component + WelcomeAsset flexible + instrucciones PWA |
| `api/nutricionista/ajustes/[id]/aprobar` | Nota obligatoria 20-300 chars + email + notificación |
| `nutricionista/ajustes/ajustes-client.tsx` | Textarea obligatoria, botón deshabilitado hasta 20 chars |
| `api/nutricionista/tickets/[id]/responder` | Email + notificación al responder ticket |
| `nutricionista/tickets/tickets-client.tsx` | Llama endpoint, no Supabase directo |
| `api/notificaciones` | GET lista + unread_count; POST marca leídas |
| `api/users/last-active` | PATCH debounced desde shell |
| `(app)/_components/app-shell.tsx` | Bell icon + badge + InboxOverlay + hook last_active_at |
| `nutricionista/dashboard/page.tsx` | Widget "Pacientes en riesgo" top 5 inactivos + WhatsApp CTA |

### Fase 2
| Archivo | Qué hace |
|---------|---------|
| `dashboard-client.tsx` | `ConstanzaCard` con frase rotativa diaria (determinista) |
| `nutricionista/alertas/page.tsx` + `alertas-client.tsx` | Cola priorizada alertas |
| `api/nutricionista/alertas/[id]/resolver` | POST idempotente |
| `nutricionista/layout.tsx` | Link "🚨 Alertas" en nav |
| `api/cron/detectar-sintomas` | Delta síntomas ≥3 → alerta `sintomas_empeorando` |
| `supabase/migrations/20260414200000_caso_clinico_trigger.sql` | Trigger SECURITY DEFINER |
| `(app)/perfil/inbox/page.tsx` | Historial completo notificaciones (últimas 100) |
| `perfil/page.tsx` | Link "Mensajes de Constanza" + `PerfilEdit` integrado |
| `(app)/perfil/perfil-edit.tsx` | Alergias + exclusiones editables |
| `api/perfil/alergias` + `api/perfil/exclusiones` | PATCH endpoints |

### Fase 3 (Mercado Pago)
| Archivo | Qué hace |
|---------|---------|
| `lib/mercadopago/client.ts` | Cliente REST MP |
| `api/webhooks/mercadopago/route.ts` | Webhook HMAC-SHA256 |
| `api/suscripciones/crear/route.ts` | Crea preapproval → init_point |
| `app/suscribirse/page.tsx` + `suscribirse-client.tsx` | Paywall Modern Apothecary |
| `(app)/layout.tsx` | Gate suscripción → redirige a `/suscribirse` |

### UX /procesando (sesión EOD 2026-04-14)
- Instrucciones PWA guardar app en inicio (iOS/Android) — detecta por userAgent en useEffect
- Orden: "Mientras tanto" → InstallCard → CTA comunidad WhatsApp
- Emoji 🍉 consistente, copy "mañana tendrás tu plan listo", nombre dinámico correcto

---

## Pendiente para mañana

### 1. Configuración externa (bloqueante para QA de emails)

| Acción | Dónde | Detalle |
|--------|-------|---------|
| Verificar dominio Resend | resend.com → Domains | Agregar TXT + DKIM en DNS de `constanzanutricion.cl` (beta) |
| DNS beta | Panel DNS de constanzanutricion.cl | CNAME `app` → dominio Vercel de Nutrisco |
| MP_WEBHOOK_SECRET | MP Dashboard → Webhooks | Crear webhook apuntando a `{APP_URL}/api/webhooks/mercadopago` → copiar secret → Vercel env var |
| WhatsApp link real | `procesando-client.tsx` href + `perfil/page.tsx` | Reemplazar `https://chat.whatsapp.com/` con link real de Constanza |
| Beta users trial | Supabase Dashboard → Table editor | `UPDATE users SET estado_suscripcion = 'trial' WHERE email IN (...)` |

### 2. QA pendiente (pasos 3-7 del checklist)

- [ ] **Cron entregar-planes:** Vercel Dashboard → Functions → Crons → "Run Now" → verificar email "plan listo"
- [ ] **Email → dashboard:** click en email → plan visible + animación
- [ ] **Ajuste sin nota:** botón deshabilitado confirmar en UI real
- [ ] **Ajuste con nota:** email + notificación al paciente → badge unread
- [ ] **Inbox:** bottom sheet con notificación visible, auto-read al abrir
- [ ] **Ticket respondido:** notificación + email al paciente
- [ ] **Paywall MP:** flujo completo `/suscribirse` → MP → webhook → acceso

### 3. Dependencias de Constanza (pedir en un correo)

1. Link real del grupo WhatsApp de beta
2. Decisión + grabación del activo de bienvenida para /procesando (video/foto/audio)
3. Revisión del copy de `voz.ts` (4 templates MVP)

---

## Decisiones clave tomadas

- Delay 24h: `asignaciones_pauta.visible_para_paciente=false`. Cron entrega a las ≥20h.
- Nota de Constanza en ajuste: obligatoria 20-300 chars. No opcional.
- Widget riesgo: usa `last_active_at` (no N+1 RPCs a `calcular_risk_score`).
- `crearNotificacion` swallows errors — fallo de notificación no revierte operación principal.
- `last_active_at` debounced via localStorage (1 vez / 10 min).
- `WelcomeAsset`: slot flexible — beta entra con CardEditorial; video se pasa como prop cuando esté listo.
- InstallCard: no usa `beforeinstallprompt` (no funciona en iOS). Instrucciones manuales siempre funcionan.
- Vercel Hobby: crons máx 1x/día. `entregar-planes` en `0 12 * * *` (no `*/15`).
