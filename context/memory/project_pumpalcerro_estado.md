---
name: Pumpalcerro — estado campaña Meta Ads Valle del Elqui + email marketing
description: Estado de la campaña Meta Ads Valle del Elqui (mayo 2026) y email masivo Conguillío producido para GHL
type: project
originSessionId: 16287541-f139-4b8b-844f-96565e592dae
---
Flujo técnico completo construido, probado end-to-end y activo en producción (2026-04-08). Campaña Meta Ads lanzada (2026-04-15). Email masivo de confirmación viaje Conguillío producido y listo para enviar (2026-04-21).

**Why:** Primera campaña de pauta de Pumpalcerro — valida el modelo de comisión por resultado (10–15% sobre utilidad por venta).

**How to apply:** Todo el stack está funcionando. Email Conguillío listo para disparar desde GHL. Pendiente reporte Meta Ads.

## Estado al 2026-04-29

- **Landing:** `https://elqui.pumpalcerro.com` — Next.js 14, Vercel ✅
- **Campaña Meta Ads:** Lanzada 2026-04-15 ✅
- **Email masivo Conguillío:** Producido y listo ✅ — `clientes/pumpalcerro/outputs/correos/viaje-conguillio-confirmado-v3.html`
- **Email promocional Valle del Elqui:** Producido para GHL ✅ — `clientes/pumpalcerro/outputs/correos/viaje-elqui-confirmado.html`

## Email masivo Conguillío — v3 (2026-04-21)

Archivo: `clientes/pumpalcerro/outputs/correos/viaje-conguillio-confirmado-v3.html`

Características:
- Logo CDN GHL: `https://assets.cdn.filesafe.space/UsfN3aEssI2BBNrqhBjq/media/69b862f3dec742d6a3ca5242.png`
- Hero image CDN GHL: `https://assets.cdn.filesafe.space/UsfN3aEssI2BBNrqhBjq/media/69e79f456fc69286f39f50d8.jpeg`
- CTA botón → WhatsApp: `https://wa.link/ih0o09`
- Unsubscribe: `{{unsubscribe}}` (tag GHL nativo)
- "Todo incluye" corregido a single-column (emoji + texto inline) — mobile-safe
- Outlook VML + non-MSO para botón redondeado
- Voz Pumpalcerro: "Hola pumpita", "cordada", firma "Michi y el equipo"

## Flujo técnico Meta Ads (activo desde 2026-04-08)

```
Landing → PaymentModal (nombre/email/teléfono)
→ fbq('InitiateCheckout')
→ POST /api/lead
   ├── GHL Webhook A: crea contacto + oportunidad "Interesado"
   └── MP Preferences API: crea preferencia dinámica con external_reference=email
→ Redirect a init_point de MP
→ Cliente paga
→ Redirect /gracias → fbq('Purchase') client-side
→ MP IPN → n8n (async)
   ├── GET /v1/payments/{id}
   ├── IF type=payment AND status=approved
   ├── Code node: SHA256(email) + SHA256(teléfono)
   ├── Meta CAPI: Purchase con hashes
   └── GHL Webhook B: payment_confirmed
```

## Pendientes

- Michi dispara email masivo Conguillío desde GHL 🔴
- Cliente sube imagen hero a CDN para email de Valle del Elqui 🔴
- Reporte inicial Meta Ads (con plantilla CreActive) 🟡
- Access Token MercadoPago para n8n 🔴
- Documentar flujos GHL (Webhook A y B) 🟢
- Deadline ventas: 6 mayo 2026 — 11 cupos disponibles

## Archivos clave

- `clientes/pumpalcerro/outputs/pumpalcerro-landing/` — landing Next.js
- `clientes/pumpalcerro/outputs/correos/viaje-conguillio-confirmado-v3.html` — email masivo Conguillío
- `clientes/pumpalcerro/outputs/correos/viaje-elqui-confirmado.html` — email promocional Valle del Elqui
- `clientes/pumpalcerro/outputs/n8n-workflow-mp-ipn.json` — workflow n8n
- `plantillas/sistema-pagos-mp-n8n-capi-ghl/README.md` — plantilla reutilizable
