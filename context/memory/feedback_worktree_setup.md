---
name: Worktree location preference
description: Preferred location for git worktrees when using superpowers skills
type: feedback
---

Usar `.worktrees/` local al proyecto (no la ubicación global `~/.config/superpowers/worktrees/`).

**Why:** Más fácil de encontrar y limpiar. La opción global solo tiene sentido si se trabaja en múltiples repos desde directorios distintos simultáneamente.

**How to apply:** Cuando el skill pregunte dónde crear el worktree, seleccionar siempre `.worktrees/` local.
