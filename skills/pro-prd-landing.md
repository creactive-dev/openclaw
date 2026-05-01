# PRD Landing Page — Skill de CreActive Studio

## Overview
Transforma un transcrito de reunión de onboarding en un PRD (Product Requirements Document) completo y estructurado para la construcción de una landing page. El output es el documento maestro que guía todo el proceso de diseño y desarrollo.

## Purpose
- Eliminar el trabajo manual de ordenar notas de reunión
- Asegurar que ningún detalle importante se pierda
- Generar un documento que el cliente pueda revisar y aprobar antes de que comience cualquier trabajo
- Servir como fuente de verdad para diseñadores y desarrolladores

## Input Requirements

### Requerido
1. **Transcrito de reunión** — texto completo o archivo .docx con la reunión de onboarding
2. **Cliente slug** — identificador del cliente (ej: `ph-labs`, `pumpalcerro`)

### Opcional
3. `--fecha-entrega` — fecha límite del proyecto (formato YYYY-MM-DD)

---

## Execution Steps

### Step 1: Extraer información del transcrito

Leer el transcrito completo e identificar:

**Sobre el negocio:**
- Nombre de la empresa y descripción en sus propias palabras
- Eslogan o tagline si lo menciona
- Modelo de negocio (cómo gana dinero)
- Tipos de clientes (B2B, B2C, segmentos específicos)
- Propuesta de valor principal
- Diferenciadores vs. competencia
- Objeciones comunes que mencionan

**Sobre la landing:**
- Objetivo principal de la página (qué quiere que haga el visitante?)
- CTAs específicos mencionados
- Flujos que deben existir (formulario, calendario, brochure, etc.)
- Integraciones requeridas (CRM, GHL, calendario, email automation)
- Contenido que el cliente ya tiene vs. lo que hay que crear
- Restricciones o cosas que NO quiere

**Sobre diseño y marca:**
- Referencias visuales mencionadas (URLs, nombres de empresas)
- Colores de marca mencionados
- Estilo visual descrito (oscuro, tecnológico, minimalista, etc.)
- Logo y assets disponibles
- Sensaciones/percepciones que quiere generar

**Sobre plazos y logística:**
- Fecha límite o deadline
- Materiales pendientes que el cliente debe entregar
- Accesos o cuentas que deben compartirse

### Step 2: Identificar gaps

Listar explícitamente todo lo que NO quedó definido en la reunión y que será necesario para el proyecto. Estos son los pendientes que el cliente debe resolver antes de que empiece la construcción. Incluye todo lo que no quedo resuelto en Step 1

### Step 3: Generar el PRD

Producir el documento completo con la estructura definida en Output más abajo.

### Step 4: Quality check

Antes de guardar, verificar:
- [ ] Toda la información del transcrito está capturada, nada inventado
- [ ] Los CTAs son específicos, no genéricos
- [ ] Los pendientes del cliente están listados con claridad
- [ ] Las referencias visuales tienen URL o descripción precisa
- [ ] El stack técnico está alineado con el stack de CreActive (GHL, WordPress, n8n)
- [ ] El tono del documento es claro y aprobable por el cliente

---

## Output

### Estructura del PRD

```markdown
# PRD — Landing Page [Nombre Cliente]
**Versión:** 1.0
**Fecha:** [hoy]
**Estado:** Borrador — pendiente aprobación cliente
**Responsable:** CreActive Studio

---

## 1. Resumen ejecutivo
[2-3 párrafos: quién es el cliente, qué necesitan, cuál es el objetivo de la landing]

## 2. Sobre el negocio
### 2.1 Descripción
### 2.2 Modelo de negocio
### 2.3 Tipos de cliente
### 2.4 Propuesta de valor
### 2.5 Diferenciadores clave
### 2.6 Objeciones comunes

## 3. Objetivo de la landing page
### 3.1 Objetivo principal
### 3.2 Objetivos secundarios
### 3.3 Lo que NO debe hacer la página

## 4. Audiencia objetivo
### 4.1 Perfil del visitante ideal
### 4.2 Desde dónde llega el tráfico

## 5. CTAs y flujos
### 5.1 CTA principal
### 5.2 CTAs secundarios
### 5.3 Flujos de conversión (diagrama o descripción paso a paso)

## 6. Estructura de contenido (secciones propuestas)
[Lista de secciones en orden, con descripción de qué va en cada una]

## 7. Referencias visuales
| URL / Nombre | Qué le gustó |
|---|---|

## 8. Identidad visual
### 8.1 Colores de marca
### 8.2 Tipografía (si aplica)
### 8.3 Estilo general
### 8.4 Assets disponibles

## 9. Sensaciones / percepción objetivo
[Cómo quiere que se sienta el visitante al entrar a la página]

## 10. Stack técnico
| Componente | Herramienta | Notas |
|---|---|---|
| CMS | WordPress | |
| CRM | GoHighLevel | |
| Calendario | GHL Calendar | |
| Automatización email | GHL Workflows | |
| Formularios | GHL Forms | |

## 11. Integraciones requeridas
[Lista de integraciones con descripción de qué debe hacer cada una]

## 12. Pendientes del cliente
[Lista numerada de todo lo que el cliente debe entregar antes de que empiece la construcción]

## 13. Pendientes de CreActive
[Lista de lo que debemos resolver o confirmar internamente]

## 14. Fechas clave
| Hito | Fecha |
|---|---|
| Entrega de assets por parte del cliente | |
| Presentación de estructura para aprobación | |
| Desarrollo | |
| Revisión cliente | |
| Entrega final | |

## 15. Fuera de alcance
[Lista explícita de lo que NO está incluido en este proyecto]
```

### Guardar el archivo
`clientes/{cliente-slug}/prd-landing-v1.md`

### Confirmar al usuario
1. Archivo guardado en: [ruta]
2. Gaps identificados: [número] — listados en sección 12
3. Próximo paso: revisar PRD con cliente y ejecutar `/estructura-landing`

---

## Quality Standards
- [ ] No hay información inventada — todo viene del transcrito o del CLAUDE.md del cliente
- [ ] Pendientes del cliente son específicos y accionables
- [ ] Secciones propuestas de la landing son coherentes con el objetivo del negocio
- [ ] El documento puede ser enviado al cliente para revisión sin edición adicional
