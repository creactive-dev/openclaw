---
name: White Cassini — Plan demo McDonald's
description: Plan documentado (no ejecutado) para dejar el tenant mcdonald-s-antofagasta-playa listo para demos presenciales
type: project
originSessionId: 24785bf0-f581-4ce6-b916-25d101e44532
---
Plan guardado en `~/.claude/plans/para-el-proyecto-users-oz-documents-cas-zany-dongarra.md` (2026-04-23). Parte del roadmap, aún sin ejecutar.

**Alcance del plan:**
- Cambiar login admin de McDonald's a `demo@kitchat.cl` / `Kitchat2026` vía Auth Admin API (UUID del user intacto).
- Agregar flag `config_operaciones.demo_mode = true` solo para este tenant.
- Crear `admin-react/src/lib/demoFixtures.js` con 8 conversaciones mock + mensajes (texto/foto/audio) + helper `invokeKapsoSendDemo()`.
- Editar `ConversationsPage.jsx` para cortocircuitar `fetchConversations`/`fetchMessages` y polling cuando `demo_mode`.
- Editar `OrdersPage.jsx` y `OrderDetailModal.jsx` para usar `invokeKapsoSendDemo` en modo demo (toast "Notificación enviada (demo)").
- Agregar badge "DEMO" en `Sidebar.jsx` + `MobileNav.jsx`.
- Crear migración `20260423_demo_orders_mcdonald-s-antofagasta-playa.sql` con 10 pedidos en todas las columnas del kanban + clientes demo. Teléfonos deben matchear últimos 9 dígitos con las conversaciones mock para que `findOrdersForConv` vincule chat ↔ pedido.

**Why:** Necesario para demos presenciales de Kitchat sin depender de conexión real a Kapso/WhatsApp. El tenant ya tiene menú completo seedeado (PedidosYa scrape) pero inbox y kanban están vacíos.

**How to apply:** Cuando se retome esta tarea, leer el plan completo en `~/.claude/plans/para-el-proyecto-users-oz-documents-cas-zany-dongarra.md`. Verificar que el seed de McDonald's sigue aplicado y que no haya regresiones en Kapso real para otros tenants al hacer los cambios en ConversationsPage/OrdersPage.
