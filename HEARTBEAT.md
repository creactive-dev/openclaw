# HEARTBEAT.md — Protocolo de Cron Diario
> CAS ejecuta este protocolo automáticamente cada día a las 8:00 AM (hora Colombia/Chile)

---

## Cron diario — 8:00 AM

### Paso 1 — Sincronizar contexto
```bash
cd /data/workspace && git pull origin main
```
Si el pull falla, notificar a Oscar por Telegram y continuar con la versión local.

### Paso 2 — Revisar tareas activas
Leer `tareas/activas.md` y archivos `tareas/por-cliente/*.md`.

Clasificar cada tarea en:
- 🔴 Urgente — vence hoy o lleva más de 3 días sin movimiento
- 🟡 Pendiente — activa, sin urgencia inmediata
- ✅ Lista para cerrar — parece completada pero no está marcada

### Paso 3 — Revisar inbox
Leer `inbox/` — clasificar entradas pendientes en tareas, ideas o archivo.
Mover lo procesado. Dejar inbox limpio.

### Paso 4 — Alertas de clientes
Para cada cliente en `clients/activos/`, revisar `estado.md`:
- ¿Última actualización hace más de 7 días? → alerta amarilla
- ¿Última actualización hace más de 14 días? → alerta roja
- ¿Hay entregable prometido sin confirmar? → alerta roja

### Paso 5 — Revisar prospectos
Leer estados en `clients/prospectos/`:
- ¿Algún prospecto sin contacto hace más de 5 días? → incluir en reporte
- ¿Hay propuesta enviada sin respuesta hace más de 3 días? → alerta de seguimiento

### Paso 6 — Generar y enviar reporte por Telegram

Formato del reporte diario:
```
☀️ Buenos días Oscar — [fecha]

📋 TAREAS HOY
🔴 [tarea urgente] — [cliente/proyecto]
🟡 [tarea pendiente] — [cliente/proyecto]
(si no hay tareas urgentes: "Sin urgencias hoy ✅")

👥 CLIENTES
⚠️ [cliente] — sin update hace [X] días
✅ [cliente] — al día

🔁 PROSPECTOS
→ [prospecto] — [estado / último contacto]
(solo los que requieren acción)

💡 INBOX PROCESADO
→ [N] ideas clasificadas / [N] tareas creadas
(solo si hubo movimiento)

---
[Si no hay nada crítico, termina con una línea]:
"Todo bajo control. Buen día. 🤝"
```

---

## Cron semanal — Lunes 8:00 AM

Se ejecuta en lugar del reporte diario los lunes.

### Adicional al reporte diario, incluye:

**Estado de proyectos activos:**
```
📊 SEMANA [número] — Estado de proyectos

[Cliente/Proyecto]
→ Estado: [En curso / Bloqueado / Sin movimiento]
→ Último avance: [descripción breve]
→ Próxima acción: [qué sigue]
```

**Inteligencia proactiva (máximo 3 observaciones):**
```
🔍 CAS OBSERVA
→ [oportunidad o riesgo]
  Contexto: [por qué lo detecté]
  Sugerencia: [acción concreta]
```
Fuentes que revisa para generar observaciones:
- Fechas de último contacto en `clients/activos/*/estado.md`
- Tareas repetitivas en `tareas/activas.md`
- Prospectos sin movimiento en `clients/prospectos/*/estado.md`
- Proyectos bloqueados en `internal-projects/*/estado.md`
- Ideas en `ideas/banco.md` con más de 2 semanas sin desarrollar

Si no hay observaciones relevantes, omite la sección sin forzar contenido.


```
💰 MRR ESTIMADO
Retainers CLP: [suma]
Retainers USD: [suma]
Variable (rev share): pendiente de actualizar
Total aprox: [cifra]
```

**Pipeline de ventas:**
```
🎯 PIPELINE
Prospectos activos: [N]
Propuestas enviadas: [N]
En negociación: [N]
→ Próximas acciones recomendadas: [lista corta]
```

---

## Triggers adicionales (fuera del cron)

Además del cron, CAS responde a estos comandos por Telegram:

| Comando | Acción |
|---|---|
| `anota: [texto]` | Captura en inbox y clasifica |
| `tarea: [texto] para [cliente]` | Crea tarea directamente en cliente |
| `idea: [texto]` | Guarda en ideas/banco.md con categoría |
| `estado [cliente]` | Devuelve estado.md del cliente |
| `pipeline` | Resumen rápido de prospectos activos |
| `mrr` | Cálculo de MRR desde archivos de clientes |
| `semana` | Fuerza el reporte semanal en cualquier momento |
| `actualiza` | Fuerza git pull del repo |

---

## Manejo de errores

- **Git pull falla** → continuar con versión local, notificar al final del reporte
- **Archivo no encontrado** → notificar en reporte, no interrumpir el cron
- **Sin tareas ni alertas** → reporte mínimo de una línea: "Todo bajo control. Buen día. 🤝"
- **Error de API** → reintentar 1 vez, si falla notificar por Telegram con el error

---

## Archivos que lee este protocolo

```
tareas/activas.md
tareas/por-cliente/pumpalcerro.md
tareas/por-cliente/constanza-nutricion.md
tareas/por-cliente/ph-labs.md
clients/activos/*/estado.md
clients/prospectos/*/estado.md
inbox/
ideas/banco.md
```

---

*Versión: 1.0 — Mayo 2026*
*CAS ejecuta este archivo. No modificar estructura sin actualizar el agente.*
