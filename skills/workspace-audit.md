# /workspace-audit

Analiza el workspace completo de CreActive OS y genera un archivo `workspace-estado.md` con el estado actual, gaps detectados e inconsistencias. Úsalo al inicio de cada sesión nueva o cuando quieras tener visibilidad total del sistema.

---

## Instrucciones para Claude Code

Cuando el usuario ejecute `/workspace-audit`, realiza los siguientes pasos **en orden**:

---

### FASE 1 — Escaneo del workspace

Lee y mapea todos los archivos relevantes del proyecto. Empieza con:

1. `CLAUDE.md` raíz (identidad y reglas del sistema)
2. Todos los archivos de clientes en `/clientes/` o equivalente:
   - `CLAUDE.md` por cliente
   - `estado.md` por cliente
   - `historial.md` por cliente
3. Skills/slash commands disponibles (carpeta `/skills/`, `/commands/`, o `.claude/`)
4. Archivos de código activo:
   - `/nutrisco/` → Next.js + Supabase
   - `/content-engine/` → Generador de carruseles
5. Cualquier otro `.md` que encuentres en la raíz o subcarpetas relevantes

Para cada archivo encontrado, registra:
- Ruta
- Fecha de última modificación (si disponible)
- Tamaño aproximado / líneas

---

### FASE 2 — Auditoría

Analiza lo que encontraste y detecta:

**Gaps estructurales**
- Clientes sin `estado.md` o sin `historial.md`
- Clientes con `CLAUDE.md` desactualizado o vacío
- Skills documentadas pero sin archivo de implementación (o viceversa)
- Proyectos de código sin `CLAUDE.md` propio

**Inconsistencias**
- Datos contradictorios entre archivos (ej: precio distinto en `estado.md` vs `CLAUDE.md`)
- Clientes activos en un archivo que no aparecen en otro
- Referencias a archivos que no existen

**Estado de proyectos de código**
- ¿Tiene `CLAUDE.md` propio el proyecto?
- ¿Hay un `README.md` o documentación de stack?
- ¿Hay tareas pendientes o bloqueantes registradas?

---

### FASE 3 — Síntesis

Genera un resumen ejecutivo con:

1. **Salud general del workspace** (escala: 🔴 crítico / 🟡 parcial / 🟢 ok)
2. **Inventario completo** (tabla: cliente/proyecto → archivos presentes → estado)
3. **Top 5 gaps prioritarios** (los que más bloquean el trabajo diario)
4. **Inconsistencias encontradas** (con referencia a los archivos en conflicto)
5. **Próximos pasos recomendados** (acciones concretas, ordenadas por impacto)

---

### FASE 4 — Output

Escribe el archivo `workspace-estado.md` en la raíz del proyecto con este formato:

```markdown
# Workspace Estado — CreActive OS
> Generado: {{fecha}}
> Auditor: /workspace-audit

## Salud general
{{emoji}} {{descripción de una línea}}

## Inventario

| Cliente / Proyecto | CLAUDE.md | estado.md | historial.md | Skills | Código | Estado |
|---|---|---|---|---|---|---|
| {{nombre}} | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | 🟢/🟡/🔴 |

## Gaps detectados (top 5)
1. {{gap}} — {{impacto}}
2. ...

## Inconsistencias
- **{{archivo A}} vs {{archivo B}}**: {{qué contradice qué}}

## Próximos pasos
1. [ ] {{acción concreta}} — {{archivo o cliente afectado}}
2. ...

## Notas del audit
{{observaciones adicionales relevantes}}
```

---

## Cuándo usar este comando

- Al inicio de una sesión nueva (antes de pedir cualquier tarea)
- Después de incorporar un cliente nuevo
- Cuando sientas que el workspace está "desorganizado" o tienes dudas sobre qué existe
- Antes de presentar el sistema a alguien más (partner, cliente, colaborador)

---

## Tiempo estimado de ejecución

Depende del tamaño del workspace. Típico: **30–90 segundos**.

---

## Archivos que genera

| Archivo | Ubicación | Descripción |
|---|---|---|
| `workspace-estado.md` | raíz del proyecto | Estado completo del workspace |

No modifica ningún archivo existente.