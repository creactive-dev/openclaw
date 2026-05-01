# /cierre-sesion

Cierra la sesión activa de forma ordenada cuando el contexto alcanza ~60–70%.
Documenta todo lo hecho y actualiza los archivos de estado correspondientes según el tipo de sesión.

Úsalo siempre antes de que el contexto llegue al 80% — no esperes a que Claude empiece a olvidar cosas.

---

## Instrucciones para Claude Code

Cuando el usuario ejecute `/cierre-sesion`, realiza los siguientes pasos **en orden**.

---

### FASE 0 — Detectar tipo de sesión

Analiza la conversación completa y clasifica la sesión en uno de tres tipos:

**🔧 TÉCNICA** — si la mayoría del trabajo fue:
- Código (Next.js, Supabase, n8n, scripts)
- Git commits, branches, worktrees
- Builds, deploys, debugging
- Configuración de herramientas

**🤝 AGENCIA** — si la mayoría del trabajo fue:
- Documentos de clientes (propuestas, PRDs, estructuras, briefs)
- Contenido (carruseles, captions, reels, threads)
- Estrategia, diagnósticos, seguimientos
- Reuniones, minutas, contexto de cliente
- Operaciones internas (workspace audit, skills, plantillas)

**🔀 MIXTA** — si hubo una mezcla significativa de ambas.

Las fases marcadas con 🔧/🤝 son opcionales según el tipo detectado. Las fases sin marca son **siempre obligatorias**.

---

### FASE 1 — Inventariar la sesión

#### Siempre (todos los tipos)

1. **¿En qué se trabajó?** — listar todos los proyectos, clientes, o temas tocados
2. **¿Qué se completó?** — outputs finalizados, tareas cerradas
3. **¿Qué quedó pendiente?** — con responsable (Oscar / cliente / externo)
4. **¿Qué decisiones se tomaron?** — opciones elegidas y por qué
5. **¿Qué aprendizajes o gotchas surgieron?** — cosas no obvias que conviene recordar

#### 🔧 Sesiones técnicas — además:

- **Commits nuevos** — de git log, identificar cuáles son de esta sesión
- **Fases completadas** — contrastar el plan con el estado actual del código
- Si hay build step: correr `npm run build` o `tsc --noEmit` para confirmar que compila
- Marcar: ✅ DONE (esta sesión) / ✅ DONE (anterior) / ⏳ PRÓXIMO / ⏳ pendiente
- **Bloqueantes técnicos activos**

#### 🤝 Sesiones de agencia — además:

- **Clientes tocados** — listar slugs involucrados
- **Outputs generados** — qué archivos se crearon o modificaron en `clientes/{slug}/outputs/`
- **Estado de relación** — pendientes del cliente / pendientes de CreActive hacia el cliente
- **Skills o plantillas modificadas** — si se editó algo en `.claude/commands/` o `plantillas/`

---

### FASE 2 — Leer estado previo

#### 🔧 Sesiones técnicas

1. Identificar ruta local del repo/proyecto, branch activo, worktree (si aplica), ruta del plan (`~/.claude/plans/*.md`) y archivo de memoria (`~/.claude/projects/.../memory/project_*.md`)
2. Si hay worktree activo:
   ```bash
   git log --oneline -15
   git status
   ```
3. Leer el archivo de memoria actual para saber el estado **antes** de esta sesión.

#### 🤝 Sesiones de agencia

Para cada cliente involucrado:
1. Leer `clientes/{slug}/CLAUDE.md`
2. Leer `clientes/{slug}/estado.md` si existe
3. Leer el archivo de memoria relevante en `~/.claude/projects/.../memory/`

---

### FASE 3 — Actualizar archivos de estado

#### 3A. Memoria del proyecto (siempre)

Para cada proyecto o cliente trabajado, abrir su `project_*.md` en `memory/` y:
- Actualizar el estado con lo completado en esta sesión
- Agregar outputs, commits, o entregables nuevos
- Actualizar "Próximo paso" con la siguiente acción exacta
- Agregar gotchas o aprendizajes nuevos
- Si no existe el archivo de memoria, crearlo

**Regla:** no eliminar información histórica — solo agregar y actualizar.

#### 3B. MEMORY.md index (siempre)

Actualizar la línea del proyecto/cliente en `MEMORY.md`. Si no tiene línea, agregarla.

#### 🔧 3C. Plan del proyecto técnico

Al final del plan (`~/.claude/plans/*.md`), agregar:

```markdown
---

## Sesión {{fecha}} — Notas de cierre

**Completado:** {{lista de fases/commits}}
**Próximo:** {{fase exacta}}
**Gotchas:** {{decisiones o problemas encontrados}}
```

#### 🤝 3D. Estado del cliente

Para cada cliente trabajado, actualizar o crear `clientes/{slug}/estado.md`:

```markdown
# Estado — {{Nombre Cliente}}
**Slug:** `{{slug}}`
**Última actualización:** {{fecha}}

## Estado actual
{{Una línea de dónde está el proyecto ahora}}

## Completado
{{Lista acumulada de hitos cerrados — nunca borrar, solo agregar}}

## Pendiente de CreActive
| Tarea | Urgencia | Para qué |
|-------|----------|----------|
| {{tarea}} | 🔴/🟡/🟢 | {{razón}} |

## Pendiente del cliente
| Pendiente | Urgencia | Bloquea |
|-----------|----------|---------|
| {{pendiente}} | 🔴/🟡/🟢 | {{qué bloquea}} |

## Próximo hito
{{Lo siguiente concreto que hay que hacer}}

## Historial de sesiones
| Fecha | Qué se hizo |
|-------|-------------|
| {{fecha}} | {{resumen de una línea}} |
```

**Regla:** Si ya existe `estado.md`, actualizar sin borrar el historial.

---

### FASE 4 — Confirmación final

```
✅ Memoria actualizada — {{lista de archivos memory/ modificados}}
✅ MEMORY.md index actualizado
✅ Plan actualizado — {{ruta}} (sesiones técnicas)
✅ estado.md actualizado — {{slugs}} (sesiones de agencia)
✅ Handoff generado — listo para copiar-pegar

Tipo de sesión detectado: 🔧 Técnica / 🤝 Agencia / 🔀 Mixta
Contexto al cierre: ~{{X}}%
Próxima sesión empieza en: {{primera acción concreta}}
```

---

## Cuándo usar este comando

- Cuando el contexto visual llega a ~60–70%
- Antes de parar en medio de un proyecto multi-fase
- Al final del día después de completar tareas importantes
- Cuando se va a cambiar de proyecto

## Señales de que es momento de usarlo

- Claude empieza a olvidar contexto temprano de la conversación
- La conversación tiene más de ~40 mensajes
- Se completó una fase o entregable importante
- El usuario pregunta "¿en qué quedamos?"

## Archivos que modifica

| Archivo | Acción | Tipo de sesión |
|---------|--------|---------------|
| `~/.claude/projects/.../memory/project_*.md` | Actualiza estado, outputs, gotchas | Todos |
| `~/.claude/projects/.../memory/MEMORY.md` | Actualiza línea del proyecto | Todos |
| `~/.claude/plans/*.md` | Agrega notas de sesión al final | 🔧 Técnica |
| `clientes/{slug}/estado.md` | Crea o actualiza estado del cliente | 🤝 Agencia |

No crea commits git. No modifica código del proyecto.
