---
name: Handoff White Cassini — 2026-04-13 (sesión 3ª)
description: Prompt listo para copiar-pegar al inicio de la próxima sesión de White Cassini
type: project
originSessionId: 40e9a8f0-5bfa-49ac-955c-f7dd062d50e3
---
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HANDOFF — White Cassini / Kitchat — 2026-04-13
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Contexto
SaaS multi-tenant de menú digital + pedidos para restaurantes (WhatsApp vía Kapso).
En producción con 2 tenants: El Padrino y Soli Sushi.
Sprint 5 (rediseño customer app) está completo en feature/customer-redesign, pendiente
merge a main. Siguiente objetivo: Fase 2 multi-sucursal.

## Estado al cerrar esta sesión

### Completado en esta sesión
- Auto-collapse grupos modificadores en ProductModal (commit `ed57573`)
  → Al seleccionar el mínimo requerido de un grupo, colapsa solo y muestra
    resumen de opciones elegidas en el header
- Fix de datos en DB: "Gohan Acevichado" movido de "Arma tu Gohan" → "Elige tu Menú"
  en Soli Sushi (Management API, sin commit)

### Completado en sesiones anteriores (Sprint 5)
- `4e0bd7c` — HomeView + CategoryHomeCard + MenuView + CategoryTabsSticky + CategoryNavSheet
- `580e79b` — Fix 3 bugs QA: navbar sticky, nav sheet al fondo, search desde home
- `4f5a2d9` — Tab bar spacing 48→56px + STICKY_OFFSET 104→112

### Siguiente paso exacto — QA visual + merge

1. Abrir Vercel preview (branch `feature/customer-redesign`)
   URL aproximada: white-cassini-sigma-git-feature-customer-redesign-*.vercel.app
2. Validar con `?local=elpadrino` y `?local=soli-sushi`:
   ✓ Carga en HomeView (grid de categorías)
   ✓ Click en card → MenuView scrolleado a sección correcta
   ✓ Tab bar sticky sin overlap con navbar, highlight automático al scrollear
   ✓ Botón tres puntos → bottom sheet visible y centrado (NO al fondo)
   ✓ Back-to-home en navbar (solo en MenuView)
   ✓ Search desde HomeView → cambia a MenuView + muestra resultados
   ✓ ProductModal: al completar grupo requerido, colapsa y muestra resumen
   ✓ Carrito, checkout, ProductModal: sin regresiones
3. `gh pr create --title "feat: rediseño customer app (Sprint 5)"` desde el worktree
4. Merge a main → Vercel deploy a producción

### Siguiente gran fase — Fase 2 multi-sucursal (plan aparte)
| Área | Trabajo |
|------|---------|
| DB | Nueva tabla `locations` + `location_id` en categorías/productos/pedidos + migration datos |
| Customer app | `?sede=` en URL, `useStore` carga locations, `LocationPicker.tsx`, cart key nuevo |
| Admin | Selector de sucursal en sidebar, `LocationsPage.jsx`, filtros por location |
| Edge functions | `kapso-send/setup/webhook` scoped por location |

## Rutas críticas
- **Repo:** `/Users/oz/Documents/CAS-CEO/creactive-studio/Proyectos Internos/white-cassini`
- **Worktree:** `.worktrees/customer-redesign/`
- **Branch:** `feature/customer-redesign` (commit `ed57573`)
- **Plan completo:** `~/.claude/plans/sequential-strolling-cerf.md`
- **Memoria:** `~/.claude/projects/-Users-oz-Documents-CAS-CEO-creactive-studio/memory/project_white_cassini_estado.md`

## Gotchas activos (leer antes de tocar código)
- **CategoryNavSheet** usa `position: fixed` propio (.category-nav-overlay + .category-nav-sheet).
  NO usa el patrón `.modal.active` del resto de overlays.
- **STICKY_OFFSET = 112** en 3 lugares que deben estar sincronizados:
  `tokens.css` (--sticky-offset), `MenuView.tsx`, `CategoryTabsSticky.tsx`
- **Navbar height**: `.navbar { height: var(--navbar-height, 56px); padding: 0 1rem }`.
  NO poner `padding: 0.75rem 1rem` — daría 62px real y rompería el sticky offset.
- **`pm-group-summary`** es un `<p>` fuera del `.option-list` (que se oculta con display:none).
  Siempre visible cuando el grupo está colapsado y tiene selecciones.
- **Fase 2** NO empezar hasta que feature/customer-redesign esté mergeado a main.
  Toca schema con clientes reales — requiere ventana de mantenimiento.
- **Supabase MCP**: `mcp__supabase__` = Nutrisco. `mcp__supabase-white-cassini__` = este proyecto
  (suele no estar disponible). Usar Management API directa con token del keychain.
- **Categoría "Arma tu Gohan"** en Soli Sushi: solo 1 producto (el builder). "Gohan Acevichado"
  ya fue movido a "Elige tu Menú". El seed original lo tenía mal — no revertir.

## Cómo continuar
1. Lee la memoria en `~/.claude/projects/-Users-oz-Documents-CAS-CEO-creactive-studio/memory/project_white_cassini_estado.md`
2. Lee el plan en `~/.claude/plans/sequential-strolling-cerf.md`
3. cd al worktree: `.worktrees/customer-redesign/`
4. Verifica build: `cd customer-app && npm run build`
5. Abre Vercel preview y ejecuta el checklist QA de 8 puntos
6. Si QA pasa: `gh pr create` desde el worktree → merge → producción
7. Luego: nueva sesión para diseñar el plan de Fase 2 multi-sucursal

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
