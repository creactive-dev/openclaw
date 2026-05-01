# Plan de Trabajo Landing — Skill de CreActive Studio

## Overview
Genera el plan de ejecución completo para construir la landing page una vez que el PRD y la estructura están aprobados. Define fases, responsables, entregables por etapa, y criterios de aceptación. Es el documento que Oscar usa para ejecutar y el cliente usa para hacer seguimiento.

## Purpose
- Tener total claridad sobre qué hace quién y cuándo
- Detectar dependencias (qué necesitamos del cliente para poder avanzar)
- Proteger a CreActive del scope creep con fases y aprobaciones claras
- Dar al cliente visibilidad sin generar ansiedad

## Input Requirements

### Requerido
1. **Archivo PRD** — con pendientes del cliente ya identificados
2. **Cliente slug**

### Opcional
3. `--fecha-inicio` — cuándo empieza el trabajo (default: hoy + 2 días hábiles)
4. `--fecha-entrega` — deadline final (si no está en el PRD)

---

## Execution Steps

### Step 1: Leer PRD y estructura
- Identificar pendientes del cliente (qué deben entregar y cuándo)
- Identificar complejidad técnica (número de secciones, integraciones, flujos)
- Revisar fecha límite

### Step 2: Estimar esfuerzo por fase

Usar estas estimaciones base para una landing de CreActive:

| Fase | Días hábiles base | Variables que suman |
|------|------------------|---------------------|
| Setup (WordPress + GHL) | 1 día | +0.5 si es dominio nuevo |
| Diseño visual (estructura aprobada → diseño) | 2 días | +1 si hay muchas secciones custom |
| Desarrollo (diseño → HTML/CSS/WP) | 2-3 días | +1 por cada integración GHL |
| Contenido (copy final + imágenes) | 1 día | +1 si hay contenido AI que generar |
| QA y revisión | 1 día | siempre |
| Ajustes post-revisión | 1 día | siempre |
| Buffer | 20% del total | siempre |

### Step 3: Generar cronograma con dependencias

Marcar explícitamente qué tareas dependen de assets del cliente.

### Step 4: Generar checklist de QA final

Lista completa de lo que se verifica antes de entregar.

---

## Output

### Estructura del documento

```markdown
# Plan de Trabajo — Landing [Nombre Cliente]
**Versión:** 1.0
**Fecha inicio:** [fecha]
**Fecha entrega estimada:** [fecha]
**Estado del proyecto:** En ejecución

---

## Resumen de fases

| Fase | Inicio | Fin | Responsable | Estado |
|------|--------|-----|-------------|--------|
| 0. Assets del cliente | | | Cliente | Pendiente |
| 1. Setup técnico | | | CreActive | No iniciado |
| 2. Diseño visual | | | CreActive | No iniciado |
| 3. Desarrollo | | | CreActive | No iniciado |
| 4. Contenido | | | CreActive | No iniciado |
| 5. QA interno | | | CreActive | No iniciado |
| 6. Revisión cliente | | | Cliente | No iniciado |
| 7. Ajustes | | | CreActive | No iniciado |
| 8. Entrega final | | | CreActive | No iniciado |

---

## Fase 0 — Assets requeridos del cliente
> El trabajo no puede comenzar hasta tener estos materiales.

- [ ] [asset específico 1] — necesario para [fase X]
- [ ] [asset específico 2] — necesario para [fase X]
[etc.]

**Fecha límite para recibir assets:** [fecha]

---

## Fase 1 — Setup técnico
**Duración:** X días
**Entregable:** Ambiente WordPress + GHL configurados y conectados

Tareas:
- [ ] Configurar dominio / subdominio
- [ ] Instalar WordPress con tema base
- [ ] Conectar GHL: formularios, calendario, pipeline
- [ ] Configurar automatizaciones de email base
- [ ] Test de integraciones

---

## Fase 2 — Diseño visual
**Duración:** X días
**Entregable:** Mockup de la landing lista para aprobación

Tareas:
- [ ] Diseño de hero section
- [ ] Diseño de secciones de contenido
- [ ] Diseño de formularios y CTAs
- [ ] Versión mobile
- [ ] Presentación al cliente para aprobación [GATE: no avanzar sin ok]

---

## Fase 3 — Desarrollo
**Duración:** X días
**Entregable:** Landing funcional en staging

Tareas:
- [ ] Desarrollo HTML/CSS de cada sección
- [ ] Integración GHL (formularios → CRM)
- [ ] Integración calendario
- [ ] Automatizaciones de email / respuestas automáticas
- [ ] Optimización velocidad y SEO básico

---

## Fase 4 — Contenido
**Duración:** X días
**Entregable:** Todo el copy y medios cargados

Tareas:
- [ ] Copy final para cada sección
- [ ] Imágenes / íconos / gráficos
- [ ] Generación de imágenes IA si aplica
- [ ] Videos o demos si aplica

---

## Fase 5 — QA interno
**Duración:** 1 día
**Entregable:** Landing auditada y sin bugs

Checklist QA:
- [ ] Todos los links funcionan
- [ ] Formularios envían y guardan en GHL
- [ ] Calendario funciona y agenda correctamente
- [ ] Emails automáticos se disparan
- [ ] Responsive en mobile, tablet, desktop
- [ ] Velocidad de carga < 3 segundos
- [ ] Sin errores de consola
- [ ] Copy sin errores ortográficos
- [ ] Imágenes con alt text
- [ ] Google Analytics / pixel Meta conectado (si aplica)

---

## Fase 6 — Revisión cliente
**Duración:** 2-3 días (tiempo del cliente)
**Entregable:** Lista de ajustes del cliente (máximo 2 rondas incluidas)

> **Nota:** Esta propuesta incluye [X] rondas de ajustes. Cambios estructurales fuera de lo acordado en la estructura aprobada se cotizan por separado.

---

## Fase 7 — Ajustes
**Duración:** 1 día
**Entregable:** Ajustes implementados y confirmados

---

## Fase 8 — Entrega final
**Entregable:** Landing en producción + entrega de accesos

- [ ] Página en vivo en dominio definitivo
- [ ] Entrega de accesos: WordPress admin, GHL, dominio
- [ ] Documento de entrega con instrucciones básicas
- [ ] Capacitación breve (30 min) si aplica

---

## Fuera de alcance
[Lista explícita de lo que no está incluido y qué pasaría si el cliente lo pide]
```

### Guardar el archivo
`clientes/{cliente-slug}/plan-trabajo-landing-v1.md`

### Confirmar al usuario
1. Fecha de entrega estimada
2. Dependencias críticas del cliente
3. Total de días de trabajo (sin buffer)
4. Próximo paso: compartir plan con cliente + esperar assets

---

## Quality Standards
- [ ] Las fechas tienen buffer del 20%
- [ ] Cada fase tiene un entregable concreto y verificable
- [ ] Los gates de aprobación están explícitos (no avanzar sin ok del cliente)
- [ ] El scope está claramente delimitado (qué está incluido y qué no)
- [ ] El documento puede enviarse al cliente sin edición adicional
