# Estado del Proyecto — Easyway Chile
**Última actualización:** 16 de abril 2026 (v2 — respuestas de Claudia recibidas)
**Responsable:** Oscar Vergara Barros / CreActive Studio

---

## Estado actual: Plan de trabajo listo — flujo PRO al 80%

El flujo PRO avanzó al 80% el 16 de abril 2026. Se completaron los pasos 1, 2, 3 y 4. Claudia respondió las preguntas críticas. El próximo paso es ejecutar `/pro-build-landing` — única variable pendiente es la ciudad del seminario del 30 de abril.

---

## Progreso del flujo PRO

| Paso | Skill | Estado | Output |
|------|-------|--------|--------|
| 1 | `/cli-contexto-cliente` | ✅ Completado | `CLAUDE.md` del cliente |
| 2 | `/pro-prd-landing` | ✅ Completado | `outputs/prd-landing-v1.md` |
| 3 | `/pro-estructura-landing` | ✅ Completado | `outputs/estructura-landing-v1.md` |
| 4 | `/pro-plan-trabajo` | ✅ Completado | `outputs/plan-trabajo-landing-v1.md` |
| 5 | `/pro-build-landing` | ⏳ Pendiente | — |

---

## Información clave confirmada

| Campo | Valor |
|-------|-------|
| Color primario | `#ff3131` (rojo) |
| Precio seminario B2C | $280.000 CLP |
| Próxima fecha | 30 de abril 2026 |
| Assets disponibles | 6 archivos en `Assets/` (logo, 2x Claudia, seminario, Allen Carr promo, familia) |
| Stack decidido | Next.js 14 + Tailwind CSS + Framer Motion + Vercel |
| Agendamiento | GHL Calendar (embebido) — mockup Wix Bookings para mostrar diferencia |
| Modalidad 30 abril | Presencial |
| Lugares disponibles | 15 |
| Años experiencia Claudia | 20 años |

---

## Decisiones pendientes de Claudia

Estas respuestas desbloquean el Paso 5 (build):

| # | Pregunta | Urgencia | Respuesta |
|---|----------|---------|-----------|
| 1 | ¿Sistema de agendamiento? | 🔴 Alta | ✅ GHL Calendar (con mockup Wix) |
| 2 | ¿Modalidad del 30 de abril? | 🔴 Alta | ✅ Presencial |
| 3 | ¿Ciudad/lugar del seminario del 30 de abril? | 🔴 Alta | ⏳ Pendiente (asumimos Santiago) |
| 4 | ¿Cuántos lugares disponibles? | 🔴 Alta | ✅ 15 lugares |
| 5 | ¿Cuántos años lleva Claudia en Chile con el método? | 🟡 Media | ✅ 20 años |
| 6 | ¿Testimonios adicionales? (2-3 más para el grid) | 🟡 Media | ⏳ Pendiente |
| 7 | ¿El método online funciona igual que presencial? | 🟡 Media | ⏳ Pendiente |
| 8 | ¿Queremos secuencia de email nurturing? | 🟡 Media | ⏳ Pendiente |
| 9 | ¿Hay restricciones de diseño Allen Carr? | 🟢 Baja | ⏳ Pendiente |

---

## Próximo hito

**Confirmar ciudad del seminario** → ejecutar `/pro-build-landing --cliente=easywaychile`

Podemos hacer build YA con placeholder `[CIUDAD]` y completar cuando llegue la confirmación. Timeline: go-live **28 de abril**.

Para retomar la sesión, el agente debe leer:
1. Este `estado.md`
2. `CLAUDE.md` del cliente
3. `outputs/estructura-landing-v1.md`
4. `outputs/plan-trabajo-landing-v1.md` (el último output generado)

---

## Estructura de archivos del proyecto

```
clientes/easywaychile/
├── estado.md                          ← este archivo
├── CLAUDE.md                          ← contexto completo del cliente
├── Exploracion.md                     ← análisis de marca inicial (fuente de todo)
├── Assets/
│   ├── logo-header-ews.avif           ← logo oficial
│   ├── claudia.avif                   ← foto Claudia (principal)
│   ├── clauda 2.avif                  ← foto Claudia (alternativa)
│   ├── seminario 1.avif               ← foto de sesión
│   ├── allen car promotional assets.avif
│   └── familia allencar.avif
└── outputs/
    ├── prd-landing-v1.md              ← PRD completo (15 secciones)
    ├── estructura-landing-v1.md       ← estructura sección a sección + wireframe
    └── plan-trabajo-landing-v1.md    ← cronograma + checklist QA + timeline
```

---

## Contexto del cliente (resumen rápido)

- **Cliente:** Easyway Chile — franquicia Allen Carr's Easyway
- **Contacto:** Claudia Sarmiento (terapeuta directora)
- **WhatsApp:** +56 9 8342 3928
- **Email:** contacto@easyway.cl
- **Negocio:** Seminarios para dejar de fumar en 6 horas · 90% éxito · Garantía 100%
- **Plataforma actual:** Wix (se reemplaza con la nueva landing)
- **Modelo comercial:** 🔲 No definido aún — pendiente reunión formal

---

*Actualizar este archivo al inicio de cada sesión con el estado real del proyecto.*
