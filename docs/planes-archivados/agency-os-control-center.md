# Plan: Agency OS — CreActive Studio Control Center

## Context

Oscar necesita una web app local (Agency OS) que sirva como panel de control de CreActive Studio. Hoy el trabajo está fragmentado: los datos de clientes viven en archivos CLAUDE.md, las skills se ejecutan manualmente desde la CLI, y no existe una vista consolidada del estado del negocio. El Agency OS resuelve esto con dos módulos MVP en paralelo: (1) dashboard de clientes y (2) skill launcher integrado con Claude API.

**Decisiones clave:**
- Local (localhost:3000), no hosteado
- Lee filesystem directamente — los CLAUDE.md son la fuente de verdad, sin base de datos
- Skills ejecutadas via Anthropic SDK (usuario tiene API key)
- Ambos módulos en el mismo MVP

---

## Ubicación del proyecto

```
/Users/oz/Documents/CAS-CEO/creactive-studio/agency-os/
```

Nuevo directorio dentro del workspace existente. No toca los proyectos de clientes.

---

## Stack

| Capa | Tecnología |
|------|-----------|
| Framework | Next.js 14 (App Router) |
| Lenguaje | TypeScript |
| Estilos | Tailwind CSS + shadcn/ui |
| IA | @anthropic-ai/sdk (streaming) |
| Filesystem | Node.js `fs` via API routes |
| Dev | tsx, next dev |

---

## Estructura de archivos

```
agency-os/
├── package.json
├── next.config.mjs
├── tailwind.config.ts
├── tsconfig.json
├── .env.local                          ← ANTHROPIC_API_KEY + CREACTIVE_BASE_PATH
├── src/
│   ├── app/
│   │   ├── layout.tsx                  ← root layout con sidebar
│   │   ├── page.tsx                    ← Dashboard principal
│   │   ├── globals.css
│   │   ├── clients/
│   │   │   └── [slug]/
│   │   │       └── page.tsx            ← Detalle de cliente
│   │   ├── skills/
│   │   │   └── page.tsx                ← Skill Launcher
│   │   └── api/
│   │       ├── clients/
│   │       │   ├── route.ts            ← GET: lista todos los clientes
│   │       │   └── [slug]/
│   │       │       ├── route.ts        ← GET: datos del cliente
│   │       │       └── outputs/
│   │       │           └── route.ts    ← GET: archivos en outputs/
│   │       ├── skills/
│   │       │   └── route.ts            ← GET: lista skills de .claude/commands/
│   │       └── execute-skill/
│   │           └── route.ts            ← POST: ejecuta skill via Claude API (streaming)
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Sidebar.tsx
│   │   │   └── AppShell.tsx
│   │   ├── dashboard/
│   │   │   ├── ClientCard.tsx
│   │   │   └── MRRBanner.tsx
│   │   ├── clients/
│   │   │   ├── ClientDetail.tsx
│   │   │   └── OutputsList.tsx
│   │   └── skills/
│   │       ├── SkillLauncher.tsx       ← form + streaming output
│   │       └── SkillCard.tsx
│   └── lib/
│       ├── fs-reader.ts                ← lee archivos del workspace
│       ├── claude-md-parser.ts         ← extrae datos estructurados de CLAUDE.md
│       └── anthropic.ts               ← cliente Anthropic + helpers de streaming
```

---

## Módulo 1: Dashboard

**Ruta:** `/`

**Layout:** sidebar izquierdo + contenido principal

**Componentes:**
1. `MRRBanner` — MRR total (suma de valores en CLAUDE.md raíz: $97K + $70K + $107K + PH Labs) + número de proyectos activos + pendientes urgentes
2. `ClientCard` × 5 — por cada carpeta en `clientes/`:
   - Nombre, empresa, estado (activo / en construcción / pro bono)
   - Servicios contratados (lista corta)
   - Valor mensual
   - Pendientes del cliente (extraídos de CLAUDE.md)
   - Próximo deadline
   - Botón "Abrir" → Client Detail
   - Botón "Ejecutar skill" → Skill Launcher con cliente preseleccionado

**Sidebar:**
- Logo CreActive Studio
- Nav: Dashboard / Clientes / Skills
- Estado del sistema: cuántos skills construidos (6/15)

---

## Módulo 2: Client Detail

**Ruta:** `/clients/[slug]`

**Secciones:**
1. Header: logo (si existe), nombre, empresa, badge estado, datos de contacto
2. Identidad visual: swatches de colores (extraídos del CLAUDE.md)
3. Servicios activos: tabla
4. Pendientes: lista con urgencia (Alta / Media / Baja)
5. Outputs generados: archivos en `clientes/{slug}/outputs/` con fecha y tipo
6. Acciones rápidas: botones para skills relevantes al cliente

---

## Módulo 3: Skill Launcher

**Ruta:** `/skills`

**Layout:** panel izquierdo (lista skills) + panel derecho (form + output)

**Panel izquierdo:**
- Tabs: Proyectos / Ventas / Clientes / Contenido
- Por cada skill: nombre, estado (✅ construido / 🔲 pendiente), descripción corta
- Click → carga el form en panel derecho

**Panel derecho — Form:**
- Dropdown "Cliente" (pre-populated desde URL param si viene del dashboard)
- Inputs dinámicos según skill:
  - `sal-followup` / `pro-prd-landing`: textarea para transcrito
  - `pro-plan-trabajo`: campos fecha inicio, fecha entrega
  - `cli-contexto-cliente`: textarea transcrito, nombre empresa
- Botón "Ejecutar" → llama a `/api/execute-skill`

**Panel derecho — Output:**
- Streaming response mostrado en tiempo real (markdown renderizado)
- Botón "Guardar en outputs/" → POST al filesystem
- Botón "Copiar"

---

## Módulo 4: API Routes

### `GET /api/clients`
- Lee `fs.readdirSync(CREACTIVE_BASE_PATH + '/clientes')`
- Por cada carpeta, lee su CLAUDE.md
- Pasa por `claude-md-parser.ts` para extraer campos estructurados
- Retorna array `Client[]`

### `GET /api/clients/[slug]`
- Lee `clientes/{slug}/CLAUDE.md`
- Retorna datos completos del cliente (parseados)

### `GET /api/clients/[slug]/outputs`
- Lee `clientes/{slug}/outputs/` recursivo
- Retorna lista de archivos con metadata (nombre, fecha, tipo, tamaño)

### `GET /api/skills`
- Lee `.claude/commands/*.md`
- Extrae nombre, descripción, estado (built/stub) del frontmatter o contenido
- Retorna array `Skill[]`

### `POST /api/execute-skill`
- Body: `{ skillSlug, clientSlug, inputs: Record<string, string> }`
- Lee `.claude/commands/{skillSlug}.md` (instrucciones del skill)
- Lee `clientes/{clientSlug}/CLAUDE.md` (contexto del cliente)
- Lee `CLAUDE.md` raíz (contexto de la agencia)
- Construye el system prompt: `[CLAUDE.md raíz] + [CLAUDE.md cliente] + [instrucciones del skill]`
- Llama `anthropic.messages.stream()` con los inputs del usuario
- Retorna `ReadableStream` (Server-Sent Events)
- Opcionalmente guarda en `clientes/{clientSlug}/outputs/`

---

## `claude-md-parser.ts` — Campos a extraer

El parser usa regex + sección por sección para extraer:
```typescript
interface ClientData {
  slug: string
  nombre: string
  empresa: string
  contacto: string
  email?: string
  telefono?: string
  ubicacion: string
  servicios: string[]
  modelo: string // retainer | revenue-share | one-time | pro-bono
  valorMensual: string
  estado: 'activo' | 'en-construccion' | 'pro-bono' | 'sin-contexto'
  colores: Array<{ nombre: string; hex: string; uso: string }>
  pendientes: Array<{ descripcion: string; urgencia: 'Alta' | 'Media' | 'Baja' }>
  proyectos: Array<{ nombre: string; estado: string; deadline?: string }>
  notas: string
}
```

---

## Diseño visual

- **Modo:** Dark (fondo #0F0F10, cards #1A1A1F)
- **Acento:** Verde (#10B981) — activo / ok
- **Warnings:** Amarillo (#F59E0B) — pendiente / atención
- **Destructivo:** Rojo (#EF4444)
- **Tipografía:** Inter (system font stack)
- **Estética:** OS-like, minimalista — inspirado en Linear/Raycast
- **Componentes:** shadcn/ui con tema dark customizado

---

## Fases de construcción

### Fase 1 — Setup + API routes (base)
1. Crear `agency-os/` con Next.js 14 + TS + Tailwind + shadcn/ui
2. `.env.local` con `ANTHROPIC_API_KEY` y `CREACTIVE_BASE_PATH=../`
3. `lib/fs-reader.ts` — funciones para leer archivos del workspace
4. `lib/claude-md-parser.ts` — parser de CLAUDE.md
5. API routes: `/api/clients`, `/api/clients/[slug]`, `/api/skills`

### Fase 2 — Dashboard + Client Detail
6. AppShell con sidebar
7. Página `/` con `MRRBanner` + grid de `ClientCard`
8. Página `/clients/[slug]` con `ClientDetail` + `OutputsList`

### Fase 3 — Skill Launcher + Claude API
9. `lib/anthropic.ts` con cliente y streaming helper
10. API route `/api/execute-skill` con streaming SSE
11. Página `/skills` con `SkillLauncher` (form + streaming output)
12. Guardar outputs al filesystem desde el browser

---

## Archivos críticos de referencia

| Archivo | Propósito |
|---------|-----------|
| `/Users/oz/Documents/CAS-CEO/creactive-studio/CLAUDE.md` | Contexto raíz — sistema de identidad y clients summary |
| `/Users/oz/Documents/CAS-CEO/creactive-studio/clientes/*/CLAUDE.md` | Datos de cada cliente — fuente de verdad |
| `/Users/oz/Documents/CAS-CEO/creactive-studio/.claude/commands/*.md` | Definiciones de skills |
| `/Users/oz/Documents/CAS-CEO/creactive-studio/clientes/constanza-nutricion/Nutrisco/app/` | Referencia de stack Next.js existente |

---

## Verificación

1. `cd agency-os && npm run dev` → abre en localhost:3000
2. Dashboard carga 5 clientes con datos reales (no mocks)
3. Click en cliente → detalle con colores, pendientes, outputs
4. Skill Launcher → selecciona cliente + `/sal-followup` + pega transcrito → genera output en streaming
5. Botón guardar → archivo aparece en `clientes/{slug}/outputs/correos/`
6. Sidebar muestra "6/15 skills construidos"
