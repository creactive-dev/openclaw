---
name: Preferencia cierre de sesión — sin handoffs
description: Oscar prefiere que /cierre-sesion actualice documentos sin generar handoffs largos, para ahorrar tokens
type: feedback
originSessionId: 29ef07b6-1b4c-40ba-8481-6147f577518b
---
No generar bloques de handoff al ejecutar `/cierre-sesion`.

**Why:** Los handoffs consumen muchos tokens sin agregar valor real — la documentación actualizada en los archivos es suficiente para recuperar contexto en la próxima sesión.

**How to apply:** Al ejecutar `/cierre-sesion`, enfocarse únicamente en actualizar `project_*.md`, `MEMORY.md`, `estado.md` y plan (si aplica). No generar texto largo de resumen para copiar-pegar.
