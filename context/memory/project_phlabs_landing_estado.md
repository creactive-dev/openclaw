---
name: PH Labs landing — estado actual
description: Estado del proyecto landing Ph Labs — favicon + correos GHL flujo B (2026-04-30)
type: project
originSessionId: c56ee67a-f49d-4554-9333-f63f6a9409e8
---

Landing de Ph Labs en producción (Vercel). Favicon añadido. Correos automáticos Flujo B redactados — pendientes de configurar en GHL.

**Why:** Deadline 1 mayo 2026. Gastón necesita landing + funnel operativos antes de que llegue el inversor Rodrigo (fines mayo/junio).

**How to apply:** Al retomar, el último commit es `7e9377e`. Landing funcional — los grandes pendientes son externos (documento Gastón, configuración GHL).

## Estado al 2026-04-30

- **Repo:** github.com/creactive-dev/phl — push a main = deploy automático en Vercel
- **Último commit:** `7e9377e` — "feat: add favicon and app icon from PHL logo"
- **Ruta local:** `clientes/ph-labs/outputs/ph-labs-landing-v2/`
- **Dev local:** `cd clientes/ph-labs/outputs/ph-labs-landing-v2 && npm run dev`

## Commits de esta sesión (2026-04-30)
- `7e9377e` — favicon + app icon desde logo PHL

## Commits de sesión anterior no registrada (2026-04-16 post-memoria)
- `2c0a4f7` — add Sport Padel Center y ROCKin' Mad logos al InfiniteSlider
- `53c0d93` — TrustedBy slider animado infinito
- `9388b35` — trigger Vercel redeploy

## Completado acumulado

### Landing — secciones
- Hero, WhatIs, HowItWorks, WhyPHLabs, Metrics, ForWho, FAQ, BookMeeting, Footer, Navbar
- TrustedBy rediseñada como InfiniteSlider animado (framer-motion + react-use-measure)
- Modal "Más información" (MasInfoModal) — Flujo B entry point
- Modal calendario GHL — Flujo A

### GHL integrado
- Formulario contacto (FORM_ID_INFO: `DlSiLLPTAXqZCgVgMQeT`)
- Calendario físico (CAL_ID: `d71nnUNjA8vuh5ZNYanL`)
- Calendario digital (CAL_ID: `iTiQRm6R2AF6rfO1ZAGQ`)

### Assets
- Favicon: `app/favicon.ico` (32×32 + 16×16) + `app/icon.png` (512×512)
  - Logo centrado en canvas cuadrado con fondo #1f2328, 80% del canvas
  - Generado con Python/Pillow — Next.js App Router lo detecta automáticamente
- 7 logos en `public/logos/`: CreActive, Hablemos Sin Saber, Agencia Cb, NFC Labs, Quiro Health, Sport Padel Center, ROCKin' Mad

### Correos automáticos Flujo B — REDACTADOS, pendiente GHL
- **Versión físico:** asunto "Todo lo que necesitas saber sobre Phygital Labs, {nombre}"
- **Versión digital:** asunto "Publicidad física que por fin se puede medir — aquí tienes el detalle, {nombre}"
- **Decisión:** un solo documento "Presentación Phygital Labs" para ambos tipos (no PDFs separados por categoría)
- Ambos breves: el doc hace el trabajo pesado, el correo solo motiva a abrirlo
- Trigger: tags `info-solicitada-fisico` / `info-solicitada-digital` en GHL

## Pendientes del proyecto

| # | Pendiente | Urgencia | Responsable |
|---|-----------|---------|-------------|
| 1 | Documento "Presentación Phygital Labs" para adjuntar en flujo B | 🔴 Alta | Gastón |
| 2 | Configurar correos flujo B en GHL (trigger, adjunto, link calendario) | 🔴 Alta | Oscar (una vez que Gastón entregue el doc) |
| 3 | Correo follow-up 48h sin abrir PDF (copy pendiente) | 🟡 Media | Oscar |
| 4 | Foto de pantallas físicas → imagen IA para hero | 🟡 Media | Gastón |
| 5 | Dominio definitivo de la landing | 🟡 Media | Gastón |
| 6 | Onboarding GHL con Gastón | 🟡 Media | Oscar |
| 7 | Google Business Profile (ejecutar cuando landing esté live) | 🟢 Baja | Oscar |

## Arquitectura técnica clave

### Sección TrustedBy — InfiniteSlider
- `components/ui/InfiniteSlider.tsx` — scroll infinito (framer-motion + react-use-measure)
- `components/ui/LogoCloud.tsx` — wrapper con fade en bordes
- Props InfiniteSlider: `gap={48} duration={30} durationOnHover={80}`
- Logos con `invert: true` en constants reciben clase CSS `invert` (logos negros → blancos)

### Fix técnico caché .next
Si dev server se queda colgado: `rm -rf .next && npm run dev`

### IDs GHL (en .env.local y Vercel)
| Variable | Valor |
|----------|-------|
| `NEXT_PUBLIC_GHL_FORM_ID_INFO` | `DlSiLLPTAXqZCgVgMQeT` |
| `NEXT_PUBLIC_GHL_CALENDAR_ID_FISICO` | `d71nnUNjA8vuh5ZNYanL` |
| `NEXT_PUBLIC_GHL_CALENDAR_ID_DIGITAL` | `iTiQRm6R2AF6rfO1ZAGQ` |
| `NEXT_PUBLIC_CONTACT_EMAIL` | `hola@ph-l.com` |

## Contexto clave
- **Deadline:** 1 mayo 2026
- **Inversor (Rodrigo):** viene fines mayo/junio — quiere 3 pantallas funcionando
- **Instagram ads:** bloqueados hasta landing + funnel listos (acordado con Gastón)
- **NFC Labs:** partner estratégico
- **Logo PHL:** 320×132px (apaisado) — siempre generar canvas cuadrado para ícono/favicon
