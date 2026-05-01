---
name: White Cassini — subir límite de conversaciones WhatsApp en admin
description: COMPLETADO (2026-04-15). per_page=50→100 en kapso-conversations/index.ts:87. Desplegado con --no-verify-jwt. Panel ahora muestra 20-30 conversaciones activas.
type: project
originSessionId: cea5340a-58e6-462f-ad6e-9bba869ac95b
---
✅ EJECUTADO 2026-04-15 — Cambio aplicado y desplegado. Plan `peppy-exploring-llama.md` ya ejecutado.

**Why:** El admin panel de Kitcha mostraba solo ~10 conversaciones en `/conversations` y el usuario pidió ver 20-30. No es un límite hardcodeado: la Edge Function `kapso-conversations` pide `per_page=50` a Kapso y luego filtra las conversaciones con `status === 'ended'`. Como la mayoría están archivadas del lado de Kapso, quedan ~10 visibles tras el filtro.

**How to apply:** El fix es una sola línea — cambiar `per_page=50` → `per_page=100` en `Proyectos Internos/white-cassini/supabase/functions/kapso-conversations/index.ts:87`, luego redeploy con `supabase functions deploy kapso-conversations --project-ref gjkaboosygjitxgqcawy --no-verify-jwt`. El flag `--no-verify-jwt` es obligatorio (sin él el gateway responde 401 silenciosamente — ver CLAUDE.md sección 11). Frontend (`ConversationsPage.jsx`) no requiere cambios: ya renderiza todo lo que le devuelve la Edge Function, sin `.slice()` ni límite local. Si 100 no alcanza, evaluar subir a 150 o quitar el filtro de `ended` (requiere confirmar con usuario porque cambia el contrato archivar=ocultar).
