# Estructura Landing Page — Skill de CreActive Studio

## Overview
Convierte el PRD aprobado en una estructura detallada sección por sección. Define qué va en cada bloque, en qué orden, con qué copy base y qué elementos visuales. Este documento es lo que se presenta al cliente para aprobación antes de que empiece el desarrollo.

## Purpose
- Tener un blueprint detallado antes de tocar código o diseño
- Que el cliente apruebe la estructura antes de invertir tiempo en construcción
- Definir el copy base de cada sección (no copy final, pero sí la dirección)
- Especificar elementos interactivos, formularios, y animaciones

## Input Requirements

### Requerido
1. **Archivo PRD** — ruta al PRD generado con `/prd-landing`
2. **Cliente slug** — para leer contexto adicional del cliente

### Opcional
3. `--estilo` — preferencia de estilo visual base (dark/light/mixed). Default: inferido del PRD

---

## Execution Steps

### Step 1: Leer PRD y contexto del cliente
- Leer el PRD completo desde la ruta indicada
- Leer `clientes/{slug}/CLAUDE.md` si existe
- Identificar: objetivo principal, CTAs, referencias visuales, audiencia

### Step 2: Definir arquitectura de secciones

Para cada sección definir:
- **Nombre** — identificador interno
- **Posición** — orden en la página
- **Objetivo** — qué debe lograr esta sección en el visitante
- **Componentes** — qué elementos contiene (headline, subheadline, imagen, CTA, lista, etc.)
- **Copy base** — primer borrador de texto para cada elemento
- **Notas de diseño** — animaciones, colores específicos, layouts sugeridos

### Step 3: Definir flujos interactivos

Para cada CTA y formulario:
- Qué pasa cuando el usuario hace clic
- Qué campos tiene el formulario
- Qué mensaje de confirmación ve
- Qué automatización se dispara en GHL

### Step 4: Generar wireframe textual

Representación ASCII/textual de cómo se ve la página completa de arriba a abajo.

### Step 5: Quality check
- [ ] Cada sección tiene un objetivo claro y único
- [ ] El flujo de lectura lleva naturalmente al CTA principal
- [ ] Las objeciones del cliente (listadas en el PRD) están addressadas en alguna sección
- [ ] El copy base es coherente con la voz de marca del cliente
- [ ] No hay secciones redundantes

---

## Output

### Estructura del documento

```markdown
# Estructura Landing — [Nombre Cliente]
**Basado en:** PRD v[X]
**Fecha:** [hoy]
**Estado:** Pendiente aprobación cliente

---

## Wireframe general
[Representación visual de la página completa en texto]

---

## Secciones detalladas

### S1. [Nombre sección]
**Posición:** 1
**Objetivo:** [qué debe lograr]
**Layout:** [descripción del layout]

**Componentes:**
- **Headline:** [copy base]
- **Subheadline:** [copy base]
- **CTA:** [texto del botón] → [acción]
- **Elemento visual:** [descripción]

**Notas de diseño:**
[animaciones, colores, comportamiento responsive]

**Automatización asociada:**
[si hay formulario: qué pasa en GHL]

---
[repetir para cada sección]

---

## Flujos de conversión

### Flujo 1: [nombre]
[diagrama o descripción paso a paso]

### Flujo 2: [nombre]
[diagrama o descripción paso a paso]

---

## Pendientes para aprobar
[Lista de decisiones que el cliente debe tomar antes de que empiece el desarrollo]
```

### Guardar el archivo
`clientes/{cliente-slug}/estructura-landing-v1.md`

### Confirmar al usuario
1. Número de secciones definidas
2. Número de flujos de conversión
3. Pendientes de decisión del cliente
4. Próximo paso: aprobar estructura y ejecutar `/plan-trabajo`

---

## Quality Standards
- [ ] Wireframe refleja fielmente las referencias visuales del PRD
- [ ] Copy base es específico al negocio del cliente, no genérico
- [ ] Todos los CTAs tienen flujo definido hasta GHL
- [ ] El documento puede enviarse al cliente sin edición adicional
