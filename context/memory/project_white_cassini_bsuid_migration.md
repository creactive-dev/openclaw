---
name: White Cassini / Kitcha — Migración BSUIDs Kapso
description: Tarea pendiente esta semana: adaptar la integración Kapso de Kitcha para soportar Business-Scoped User IDs (BSUIDs) de WhatsApp
type: project
originSessionId: d8719af2-6b40-4a56-8948-9df79e34d049
---
Kapso envió guía de migración (2026-04-20) para BSUIDs de WhatsApp. Meta ya está rollando BSUIDs en webhooks entrantes — los `phone_number` y `wa_id` pueden llegar como `null`. Hay que adaptar Kitcha antes de que impacte en producción.

**Why:** Meta está reemplazando identidad por número de teléfono con BSUIDs. Inbound payloads de Kapso ya pueden traer BSUID sin phone. Si Kitcha sigue dependiendo solo de `phone_number`, puede fallar silenciosamente cuando lleguen usuarios BSUID-only.

**How to apply:** Esta semana adaptar la integración en `Proyectos Internos/white-cassini/`. Ver guía completa en `/migration-guide.md` (adjunta en el correo de Kapso del 2026-04-20).

## Checklist de migración (de la guía Kapso)

- [ ] Schema: hacer `wa_id` y `phone_number` nullable donde aplique (Supabase)
- [ ] Agregar campos: `business_scoped_user_id`, `parent_business_scoped_user_id`, `username`
- [ ] Lógica de matching: BSUID primero → phone/wa_id segundo
- [ ] Parsers de webhook: aceptar payloads con phone+BSUID y BSUID-only
- [ ] Manejar identity-change events: `user_id_update` y `user_changed_user_id`
- [ ] Outbound: seguir usando phone number (BSUID-targeted sending no está disponible aún en Kapso)
- [ ] Tests: phone+BSUID, BSUID-only, username+BSUID sin phone, status webhook con identity, identity-change event

## Timeline de Meta
- **Early April 2026**: BSUIDs ya aparecen en webhooks entrantes ← ESTAMOS AQUÍ
- **Early May 2026**: template button request-contact-information disponible
- **May 2026**: BSUID-targeted sending llega a Kapso
