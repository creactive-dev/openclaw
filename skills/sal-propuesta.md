# Propuesta Comercial — Skill de CreActive Studio

## Overview
Genera una propuesta comercial profesional en 3 fases dentro de una sola ejecución: análisis del input → borrador en Markdown → HTML listo para exportar a PDF. El skill nunca inventa información — solo trabaja con lo que el usuario confirma.

## Purpose
- Estandarizar el formato de propuestas comerciales de CreActive Studio
- Asegurar que cada propuesta tenga precios, plazos y alcance confirmados antes de generarse
- Producir un HTML A4 profesional listo para exportar a PDF desde el navegador
- Documentar el borrador y la versión final en la carpeta del cliente

## Input Requirements

### Requerido
1. **Cliente slug** — identificador del cliente (ej: `ph-labs`, `pumpalcerro`)
2. **Transcrito o notas** — transcrito de reunión de discovery, notas del prospecto, o descripción del proyecto

### Cómo se usa
```
/sal-propuesta --cliente=<slug>
```
El usuario pega el transcrito o notas después de invocar el comando.

---

## Contexto que Claude debe leer

Antes de iniciar la Fase 1, leer siempre:
1. `CLAUDE.md` raíz — identidad, stack y modelos de precio de CreActive
2. `clientes/{slug}/CLAUDE.md` si el cliente ya existe en el sistema
3. `clientes/{slug}/estado.md` si existe

Si el cliente no existe en `/clientes/`, trabajar solo con el input del usuario.

---

## Execution Steps

### Fase 1 — Análisis y preguntas

**Objetivo:** Entender el proyecto y confirmar lo que falta antes de generar nada.

1. Leer el contexto entregado (transcrito, notas, o descripción)
2. Extraer lo que ya está claro:
   - Nombre del cliente / prospecto
   - Industria / nicho
   - Problema o necesidad principal
   - Módulos o servicios mencionados
3. Hacer preguntas de verificación **SOLO sobre lo que NO está claro o no fue mencionado**

**Preguntas obligatorias si no están en el input:**
- ¿Cuáles son los módulos o servicios exactos que incluye el proyecto?
- Por cada módulo: ¿qué funcionalidades específicas incluye? (listar solo las confirmadas)
- ¿Qué stack tecnológico se usará? (si no se menciona, proponer basado en el stack oficial de CreActive y pedir confirmación)
- ¿Cuál es el precio del setup one-time?
- ¿Cuál es el retainer mensual y desde qué mes inicia?
- ¿Cuántas semanas de plazo?
- ¿Cuántas fases tiene el proyecto y qué entrega cada una?

**Regla crítica:** Claude NO inventa funcionalidades, plazos ni precios. Solo trabaja con lo que el usuario confirma explícitamente. Si algo no está confirmado, pregunta. Nunca asume.

⏸️ **ESPERAR respuesta del usuario antes de continuar a Fase 2.**

---

### Fase 2 — Borrador en Markdown

Una vez que el usuario responde las preguntas, generar un borrador en Markdown con esta estructura:

```markdown
# Propuesta — {Nombre cliente}

## El desafío
{descripción del problema en 2-3 líneas, solo con lo que el cliente mencionó}

## Alcance del proyecto
### Módulo 01 — {nombre}
- {funcionalidad confirmada}
- {funcionalidad confirmada}
...

### Módulo 02 — {nombre}
...

## Stack tecnológico
{lista de herramientas confirmadas}

## Fases de entrega
### Fase 1 — {nombre} (semanas X–Y)
Entregables:
- {entregable confirmado}
...

## Inversión
- Setup one-time: ${monto} USD
- Retainer mensual: ${monto} USD/mes (desde mes {N})
- Total primer año: ${cálculo automático} USD

## Términos
- Pago: 50% al inicio, 50% al completar Fase 2
- Cambios fuera del alcance se cotizan por separado
- Validez de la propuesta: 15 días corridos
- El cliente aprueba explícitamente cada fase antes de avanzar

## Próximos pasos
1. Aprobación de la propuesta y firma del contrato
2. Pago del 50% inicial
3. Reunión de kick-off
4. Inicio Fase 1

---
_Generado por CreActive Studio · creactivestudio.agency_
```

Al terminar el borrador, preguntar:
> "¿Aprobás este borrador o hay algo que ajustar antes de generar el HTML?"

⏸️ **ESPERAR confirmación del usuario antes de continuar a Fase 3.**

---

### Fase 3 — Generación HTML A4

Una vez aprobado el borrador, generar el HTML final desde el template estandarizado.

**IMPORTANTE: No generes el HTML desde cero.**

#### Paso 1 — Leer el template base

Leer el template en:
```
plantillas/propuesta-comercial/template.html
```

#### Paso 2 — Reemplazar variables

Reemplazar estas variables con el contenido del borrador aprobado:

| Variable | Reemplazar con |
|----------|----------------|
| `{{CLIENTE_NOMBRE}}` | Nombre del cliente |
| `{{CLIENTE_TAGLINE}}` | Descripción corta del proyecto en una línea |
| `{{FECHA}}` | Fecha de hoy en formato "DD de mes de YYYY" |
| `{{DIAGNOSTICO}}` | HTML interno de la sección El desafío (solo el contenido dentro de `page-content`, sin el `div.page` ni `accent-bar` ni footer) |
| `{{ALCANCE}}` | HTML interno de la sección Alcance detallado |
| `{{CRONOGRAMA_INVERSION}}` | HTML interno del Cronograma + Inversión |
| `{{TERMINOS_CIERRE}}` | HTML interno de Términos, próximos pasos y firma |

**El CSS y la estructura base NO se tocan — solo el contenido de las secciones variables.**

**REGLA CRÍTICA DE CONTENIDO:**
El HTML solo puede contener información que esté en el borrador aprobado. Ninguna funcionalidad, fecha, precio o término puede aparecer en el HTML si no fue confirmado por el usuario en la Fase 1.

#### Paso 3 — Guardar los outputs

1. Guardar el borrador MD en:
   ```
   clientes/{slug}/outputs/propuestas/borrador-v1.md
   ```

2. Guardar el HTML en:
   ```
   clientes/{slug}/outputs/propuestas/propuesta-v1.html
   ```

Si la carpeta `outputs/propuestas/` no existe, crearla.

3. Confirmar al usuario con las rutas de ambos archivos
4. Indicar que puede exportar a PDF abriendo el HTML en el navegador

---

## Output esperado

```
✅ clientes/{slug}/outputs/propuestas/borrador-v1.md — borrador aprobado en Markdown
✅ clientes/{slug}/outputs/propuestas/propuesta-v1.html — HTML A4 listo para exportar a PDF
```

---

## Reglas generales

- Nunca inventar funcionalidades, precios, plazos ni términos
- Nunca asumir que algo está incluido si no fue mencionado
- Si hay ambigüedad, preguntar antes de generar
- El tono es cercano y directo — no corporativo
- Español por defecto
- Cada fase termina con una pregunta explícita al usuario antes de continuar

---

## Flujo recomendado

```
/cli-contexto-cliente --cliente=slug   ← genera contexto del cliente (si es nuevo)
→ /sal-followup --cliente=slug         ← correo de seguimiento post-discovery
→ /sal-propuesta --cliente=slug        ← este skill — propuesta comercial
→ [cliente aprueba]
→ /pro-prd-landing --cliente=slug      ← cuando el proyecto incluye landing
```
