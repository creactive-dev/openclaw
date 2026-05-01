# Follow-up — Skill de CreActive Studio

## Overview
Genera un correo de seguimiento post-reunión para un cliente, basado en el contexto de su CLAUDE.md. El output queda guardado como borrador listo para enviar, en la carpeta del cliente.

## Purpose
- Asegurar que cada reunión quede cerrada con un correo profesional al cliente
- Documentar los acuerdos y pendientes en un formato que el cliente entienda y pueda releer
- Mantener el momentum y dejar claro qué hace cada quien
- Output persistente: el correo queda en la carpeta del cliente para referencia futura

## Input Requirements

### Requerido
1. **Cliente slug** — identificador del cliente (ej: `fwc-ellinger`, `ph-labs`)

### Opcional
2. `--reunion` — tipo de reunión (ej: `inicial`, `revision`, `entrega`) — por defecto `reunion`
3. `--fecha` — fecha de la reunión en formato YYYY-MM-DD — por defecto la fecha actual

### Cómo se usa
```
/sal-followup --cliente=<slug>
/sal-followup --cliente=<slug> --reunion=inicial --fecha=2026-03-24
```

---

## Execution Steps

### Step 1: Leer contexto del cliente

1. Leer `clientes/{slug}/CLAUDE.md` completo
2. Si hay transcritos recientes en `clientes/{slug}/Transcritos/`, leer el más reciente para extraer detalles específicos de la reunión

### Step 2: Identificar los elementos del correo

Del CLAUDE.md extraer:
- **Tono y jerga:** sección 7 "Cómo comunicarse con [cliente]" — el correo debe sonar exactamente igual
- **Pendientes del cliente:** sección 6 — estos van en el correo como lista de acción
- **Servicios acordados:** sección 3 — contexto de qué se está construyendo
- **Próximos pasos de CreActive:** qué prometió Oscar entregar y cuándo

### Step 3: Generar el correo

El correo debe tener esta estructura:

```
ASUNTO: [Asunto relevante — breve, sin "Re:" ni "Fwd:"]

[Saludo en el tono correcto del cliente]

[1–2 oraciones resumiendo lo que se conversó en la reunión — sin listar todo, solo el espíritu]

[Lo que sigue de parte de CreActive:]
- [acción concreta de Oscar] → [fecha o "esta semana"]
- [acción concreta de Oscar] → [fecha o "esta semana"]

[Lo que necesito de tu parte:]
- [pendiente del cliente] → [urgencia / "cuando puedas"]
- [pendiente del cliente] → [urgencia / "cuando puedas"]

[Cierre motivador en el tono del cliente — sin corporativo]

[Firma]
Oscar
CreActive Studio
[contacto si aplica]
```

**Reglas del correo:**
- El tono debe ser exactamente el del perfil de comunicación del cliente — si es informal, el correo es informal
- Los pendientes del cliente deben estar en lenguaje simple, no técnico
- Máximo 3 pendientes del cliente por correo — si hay más, priorizar los urgentes
- El correo no puede sonar a plantilla — debe sentirse escrito para esta persona específica
- Incluir UN próximo paso de CreActive claro con fecha o plazo concreto
- Sin adjuntos, sin links por ahora — el correo es el follow-up inicial

### Step 4: Guardar el output

Guardar el correo en:
```
clientes/{slug}/outputs/correos/followup-{YYYY-MM-DD}.md
```

Si la carpeta `outputs/correos/` no existe, crearla.

El archivo debe tener este formato:

```markdown
# Follow-up — [Nombre Cliente] — [Fecha]

**Para:** [email del cliente si está en el CLAUDE.md, sino: 🔲 pendiente]
**Asunto:** [asunto del correo]
**Estado:** borrador

---

[cuerpo del correo]

---
*Generado por CreActive Studio — [fecha]*
*Pendiente: copiar y enviar desde el correo de Oscar*
```

---

## Output esperado

```
✅ clientes/{slug}/outputs/correos/followup-{fecha}.md — borrador listo para revisar y enviar
```

---

## Roadmap futuro (v2)

Integrar con Gmail API via n8n para que el correo quede directamente en borradores de Gmail sin necesidad de copiar y pegar. El workflow sería:

```
/sal-followup → genera .md → n8n lee el .md → Gmail API crea borrador → Oscar revisa y envía
```

Esta integración requiere:
- Credenciales Gmail API (OAuth2)
- Workflow n8n configurado con trigger de archivo o webhook
- Campo "Para" siempre definido en el CLAUDE.md del cliente

---

## Flujo recomendado

```
/cli-contexto-cliente --cliente=slug   ← genera contexto del cliente
→ /sal-followup --cliente=slug         ← este skill — correo de seguimiento
→ [Oscar revisa el .md y lo envía desde Gmail]
→ /pro-prd-landing --cliente=slug      ← cuando aplica
```
