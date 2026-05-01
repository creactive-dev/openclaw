---
name: Kitchat — Propuesta comercial estándar
description: Template HTML A4 para enviar por WhatsApp a prospectos de Kitchat (dueños de restaurantes). Ruta: plantillas/propuesta-kitcha/template.html
type: project
originSessionId: 060a521f-f66a-4035-99cd-c97797bf9f5d
---
Template de propuesta comercial estándar para vender Kitchat a dueños de restaurantes por WhatsApp.

**Ruta:** `plantillas/propuesta-kitcha/template.html`
**Formato:** HTML A4 → PDF (Chrome Cmd+P)
**Variables:** solo 2 — `{{NOMBRE_RESTAURANTE}}` y `{{FECHA}}`

**Why:** Los prospectos de Kitchat son dueños de restaurantes tradicionales que esperan propuesta formal antes de decidir. Mercado rápido — se envía junto al link de la landing por WhatsApp.

**How to apply:**
```bash
cp plantillas/propuesta-kitcha/template.html \
   clientes/{slug}/outputs/propuestas/propuesta-kitcha-v1.html
# Cmd+H → reemplazar {{NOMBRE_RESTAURANTE}} y {{FECHA}}
# Chrome → Cmd+P → PDF → WhatsApp
```

## Estado (2026-04-23 sesión 2) — COMPLETADO ✅ v2

### Decisiones de diseño
- **Light theme** (no dark) — se lee mejor en móvil/WhatsApp
- **2 páginas** (no 5) — consumo rápido en 30 segundos
- **Branding 100% Kitchat** — eliminado todo lo que decía "CreActive" (footer, CTA sub, heading)
- **Sin prueba gratuita** — eliminado "7 días prueba sin tarjeta"; oferta principal es el plan anual
- **CTA global:** "Empezar a recibir pedidos" (heading + botón)
- **Demo link:** `mcdonald-s-antofagasta-playa.kitchat.cl`
- **Imágenes portada:** `computador.png` + `celular.png` — celular adelante-izquierda solapando laptop atrás-derecha con `margin-right: -80px`

### Contenido
- **Stats p.1:** $340.000 pedidos perdidos / 2.4 hrs gestión manual / 68% no vuelve (fuente: Problem.tsx de la landing)
- **3 pasos onboarding:** del HowItWorks.tsx — "Crea tu cuenta (5 min) → Sube tu menú (1-2h) → Recibe pedidos con poderes (inmediato)"
- **Planes:** 3 cards estilo landing — Pro (⭐ Más popular, borde verde), Business, Business XL — precios mensuales + anuales ("pagas 10")
- **Oferta principal:** Banner 🎁 "Paga el año y la implementación es gratis — pagas 10 meses, recibes 12"
- **Precios anuales:** Pro $449.004 / Business $809.004 / XL $1.259.004

### Mobile
- `@media screen and (max-width: 768px)` completo
- Stats colapsa a 1 columna, features a 2 col, timeline a 1 col apilado, planes a 1 col
- `.mockup-bleed` y `.plans-grid` como clases CSS para poder overridear inline styles con `!important`
- Headline escala de 46px → 28px, paddings reducidos a 20px

### Pendientes antes de usar en campo
| Pendiente | Urgencia | Dónde |
|-----------|----------|-------|
| QA visual Chrome → PDF (print preview) | 🔴 | Cmd+P → verificar 2 páginas sin cortes + overlap de imágenes |
| Ajustar `margin-right` solapamiento imágenes | 🔴 | En `celular.png` img → `margin-right: -80px` — subir si se ve poco overlap |
| Número WhatsApp real de Oscar | 🔴 | CTA btn `Empezar a recibir pedidos →` — actualmente sin href |
| Revisar precio anual Pro | 🟡 | Landing $449.004 vs posible $499.000 — fuente verdad: `lib/constants.ts` |

### Gotchas
- **PNG con espacio transparente:** `position: absolute` con % parecen separados aunque se solapen. Usar `margin-right` negativo en flexbox — es más confiable para forzar overlap visual.
- **Inline styles requieren `!important`** en `@media screen` — por eso se agregaron clases `.mockup-bleed` y `.plans-grid`.
- Las rutas de imagen son absolutas locales `/Users/oz/...` — solo funcionan en la máquina de Oscar. Para compartir HTML: base64 o CDN.
- El precio anual Pro en la landing es $449.004 (10 × $44.900 ≠ 10 × $49.900). Discrepancia menor — usar `lib/constants.ts` como fuente de verdad.
