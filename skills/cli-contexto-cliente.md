# Contexto de Cliente — Skill de CreActive Studio

## Overview
Genera el archivo `CLAUDE.md` de contexto para un cliente nuevo a partir del transcrito de su reunión inicial. Este es el **primer paso obligatorio** antes de ejecutar cualquier otro skill de proyecto. También actualiza el `CLAUDE.md` raíz de la agencia con el nuevo cliente.

## Purpose
- Estandarizar el ingreso de clientes nuevos — mismo formato, misma calidad, sin omisiones
- Asegurar que todo skill posterior (PRD, estructura, plan, build) tenga contexto rico del cliente
- Mantener el CLAUDE.md raíz como fuente de verdad actualizada de la agencia
- Dejar explícito todo lo que quedó pendiente definir

## Input Requirements

### Requerido
1. **Cliente slug** — identificador único del cliente (ej: `fwc-ellinger`, `ph-labs`)

### Cómo se usa
```
/cli-contexto-cliente --cliente=<slug>
```

El skill leerá automáticamente el transcrito desde `clientes/{slug}/Transcritos/` (cualquier archivo .txt o .docx que encuentre).

---

## Execution Steps

### Step 1: Leer fuentes de contexto

1. Leer el CLAUDE.md raíz (`/CLAUDE.md`) para entender el contexto de la agencia
2. Leer el transcrito completo desde `clientes/{slug}/Transcritos/`
3. Si ya existe un `clientes/{slug}/CLAUDE.md` con contenido, leerlo también (puede ser una actualización)

### Step 2: Extraer información estructurada

Leer el transcrito e identificar todo lo siguiente. Para cada campo, si no está en el transcrito, marcarlo como `🔲 Pendiente`.

**Datos básicos del cliente:**
- Nombre de la empresa y del contacto principal
- Ubicación y zona de operación
- Canal de comunicación preferido
- Perfil técnico del contacto (¿entiende de digital? ¿qué herramientas usa?)

**Sobre el negocio:**
- Descripción del negocio en sus propias palabras (citar textual si es posible)
- Modelo de negocio (cómo gana dinero)
- Tipos de clientes que atiende
- Propuesta de valor principal
- Diferenciadores vs. competencia mencionados
- Objeciones comunes que ya identificaron

**Estado del proyecto:**
- Etapa actual del negocio (lanzamiento, crecimiento, estable, etc.)
- Qué servicios CreActive va a prestarle
- Modelo comercial acordado (retainer, proyecto, revenue share, pro bono/caso de éxito)
- Deadlines o fechas importantes mencionadas

**Identidad visual:**
- Colores de marca (con códigos HEX si se mencionaron)
- Logo (disponible o pendiente)
- Estilo visual descrito o referencias mencionadas
- Assets disponibles

**Flujos y automatizaciones:**
- Flujos de conversión que se discutieron (formularios, calendarios, CTAs)
- Integraciones mencionadas (CRM, GHL, WhatsApp, etc.)

**Pendientes del cliente:**
- Todo lo que el cliente debe entregar o confirmar antes de que empiece el trabajo
- Clasificar por urgencia: Alta (bloquea el trabajo) / Media (necesario pronto) / Baja (para fases posteriores)

**Comunicación con el cliente:**
- Tono de la relación (formal, informal, de mentoría, etc.)
- Jerga o estilo de lenguaje específico
- Cómo toma decisiones (necesita el "para qué", decide rápido, necesita validación, etc.)
- Cómo hacer seguimiento

**Notas internas:**
- Contexto personal relevante mencionado en la reunión
- Oportunidades de negocio detectadas (servicios adicionales, expansión, etc.)
- Observaciones sobre la relación cliente-CreActive
- Cualquier dato que no encaje en las secciones anteriores pero sea valioso

### Step 3: Detectar gaps

Listar explícitamente todo lo que NO quedó definido en la reunión y que será necesario antes de avanzar. Estos son los pendientes que van en la sección 6 del CLAUDE.md.

### Step 4: Generar el CLAUDE.md del cliente

Escribir `clientes/{slug}/CLAUDE.md` con la siguiente estructura:

```markdown
# Contexto de Cliente — [Nombre Empresa]
**Slug:** `{slug}`
**Última actualización:** [Mes Año]
**Responsable CreActive:** Oscar Vergara Barros

---

## 1. Datos del cliente
[empresa, contacto, ubicación, idioma, canal, perfil técnico]

## 2. Sobre el negocio
[descripción en sus propias palabras (citar textual), eslogan si hay, modelo de negocio,
tipos de clientes, propuesta de valor, diferenciadores, objeciones comunes]

## 3. Estado del proyecto
[etapa actual, tabla de servicios contratados con estado, modelo comercial, deadlines]

## 4. Identidad visual
[tabla de colores con estado ✅/🔲, estilo visual, assets disponibles]

## 5. Flujos y automatizaciones
[flujos de conversión acordados — omitir sección si no aplica aún]

## 6. Pendientes del cliente
[tabla: #, pendiente, urgencia 🔴/🟡/🟢, para qué]

## 7. Cómo comunicarse con [nombre]
[tono, jerga, nivel técnico, estilo de decisiones, cómo hacer seguimiento]

## 8. Notas internas
[contexto personal, oportunidades detectadas, observaciones relacionales]

## 9. Decisiones tomadas por CreActive
[tabla: #, decisión, opción elegida, razón — solo si hay decisiones ya tomadas]

---
*Generado por CreActive Studio — [Mes Año]*
*Fuente: Reunión inicial con [nombre] (transcrito en `clientes/{slug}/Transcritos/`)*
```

**Reglas de calidad:**
- Nunca inventar información — solo lo que está en el transcrito
- Si algo no se mencionó, marcarlo con 🔲
- Usar citas textuales cuando el cliente describe su propio negocio
- El tono del CLAUDE.md es interno — puede ser directo y honesto sobre la situación del cliente

### Step 5: Actualizar el CLAUDE.md raíz de la agencia

Después de generar el CLAUDE.md del cliente, actualizar `/CLAUDE.md`:

**En la sección 4 (Clientes activos):**
Agregar una fila a la tabla de "CreActive Studio (clientes directos)" con:
- Nombre del cliente
- Servicios contratados (resumen en 3–4 palabras)
- Modelo comercial (retainer / revenue share / setup / pro bono)
- Valor mensual (o 🔲 si no quedó definido)

**En la sección 11 (Convenciones de archivos):**
Agregar la carpeta del cliente al árbol de directorios bajo `clientes/`.

**En la sección 12 (Skills disponibles):**
No modificar — esta sección la actualiza quien construye el skill, no este proceso.

---

## Output esperado

```
✅ clientes/{slug}/CLAUDE.md — generado con contexto completo
✅ CLAUDE.md raíz — tabla de clientes actualizada
```

---

## Flujo de uso recomendado

Este skill es siempre el primer paso. Una vez aprobado el CLAUDE.md:

```
/cli-contexto-cliente --cliente=slug   ← este skill
→ /sal-followup --cliente=slug         ← correo de seguimiento post-reunión
→ /pro-prd-landing --cliente=slug      ← PRD de la landing (si aplica)
→ /pro-estructura-landing --cliente=slug
→ /pro-plan-trabajo --cliente=slug
→ /pro-build-landing --cliente=slug
```

---

## Notas

- Si el cliente ya tiene un CLAUDE.md con contenido, este skill lo actualiza en lugar de sobreescribirlo — preservar información existente y agregar/corregir con el nuevo transcrito
- Si hay múltiples transcritos (varias reuniones), procesarlos todos y consolidar — indicar en el header la fecha del más reciente
- El skill no genera el correo de seguimiento — eso es `/sal-followup`
