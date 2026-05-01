---
name: pro-build-landing
description: Construye el código completo de una landing page en Next.js + Tailwind CSS + Framer Motion a partir de la estructura aprobada. Genera todos los componentes, copy final, animaciones, e integraciones GHL. Output listo para correr en local y deployar en Vercel.
argument-hint: [archivo-estructura] --cliente=slug [--lang=es|en]
---

# Build Landing Page — Skill de CreActive Studio

## Overview
Toma la estructura aprobada (`estructura-landing-v1.md`) y el contexto del cliente, y genera el código completo de la landing page. Cada sección se convierte en un componente React independiente, con su copy final, animaciones Framer Motion, y estilos Tailwind. El resultado es un proyecto Next.js listo para correr con `npm run dev`.

## Purpose
- Pasar de estructura aprobada a código funcional en un solo paso
- Generar componentes reutilizables y bien organizados
- Implementar animaciones y diseño de alto nivel sin trabajo manual
- Dejar la landing lista para review del cliente en staging (Vercel)

## Input Requirements

### Requerido
1. **Archivo estructura** — ruta al archivo `estructura-landing-v1.md` aprobado
2. **Cliente slug** — para leer `clientes/{slug}/CLAUDE.md` y obtener colores, logo, tono

### Opcional
3. `--lang` — idioma del copy (default: `es`)

---

## Execution Steps

### Step 1: Leer contexto completo
Antes de escribir una sola línea de código, leer:
- `CLAUDE.md` de la agencia (stack, estándares, tono)
- `clientes/{slug}/CLAUDE.md` (colores, estilo, referencias visuales, tono del cliente)
- `clientes/{slug}/outputs/estructura-landing-v1.md` (secciones, copy base, flujos)
- Cualquier imagen en `clientes/{slug}/Referencias Landing/` — analizarlas visualmente para capturar el estilo exacto que le gustó al cliente

### Step 2: Definir dirección de diseño

Antes de codear, comprometerse con una dirección estética específica basada en:
- La paleta de colores del cliente
- Las referencias visuales aprobadas
- El tono del negocio

**Para PH Labs y clientes tech/dark:** Dirección recomendada es "refined dark tech" — fondo azul oscuro profundo, acentos en verde, tipografía display moderna con peso variable, animaciones de entrada suaves pero con presencia, grid asimétrico en secciones de features.

Definir explícitamente:
- **Tipografía:** Par de fuentes específicas (no Inter, no Roboto, no Arial). Elegir algo que refuerce la identidad. Ej: `Syne` para display + `DM Sans` para body, o `Space Grotesk` si el cliente es más técnico/neutral.
- **Motion:** Qué animaciones van en qué secciones. Hero: staggered reveal. Features: scroll-triggered fade-up. CTA final: pulse suave en el botón.
- **Atmósfera:** Gradient mesh de fondo, noise texture overlay, o patrón geométrico sutil.

### Step 3: Generar estructura del proyecto

```
{cliente-slug}-landing/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   └── globals.css
├── components/
│   ├── sections/
│   │   ├── Hero.tsx
│   │   ├── [SeccionN].tsx     ← una por cada sección de la estructura
│   │   └── CTAFinal.tsx
│   ├── ui/
│   │   ├── Button.tsx
│   │   ├── Badge.tsx
│   │   └── GHLForm.tsx        ← formulario embebido de GHL
│   └── layout/
│       ├── Navbar.tsx
│       └── Footer.tsx
├── lib/
│   └── constants.ts           ← copy, colores, config en un solo lugar
├── public/
│   └── [assets del cliente]
├── tailwind.config.ts         ← colores del cliente como variables
├── package.json
└── README.md                  ← instrucciones para correr y deployar
```

### Step 4: Generar cada componente

Para cada sección de la estructura aprobada, generar un componente React completo con:

**Copy:** Usar el copy base de la estructura como punto de partida, refinarlo para que sea natural y convierta. No dejar placeholders — todo el texto debe estar escrito.

**Diseño:** Implementar el layout definido en el wireframe con Tailwind. Ser específico: padding exacto, tamaños de fuente, colores del cliente como variables de Tailwind.

**Animaciones:** Usar Framer Motion para:
- `initial` / `animate` / `exit` en elementos de hero
- `whileInView` para secciones que entran al hacer scroll
- `whileHover` para botones y cards
- `staggerChildren` para listas de features o pasos

**Responsividad:** Cada componente debe funcionar en mobile, tablet y desktop. Mobile-first con breakpoints `md:` y `lg:`.

### Step 5: Integraciones GHL

Para cada formulario definido en la estructura:

```tsx
// components/ui/GHLForm.tsx
// Embed del formulario de GHL como iframe o snippet JS
// El snippet_id viene de clientes/{slug}/CLAUDE.md o se deja como variable
export function GHLForm({ formId, height = 500 }: { formId: string, height?: number }) {
  return (
    <div className="w-full">
      <iframe
        src={`https://api.leadconnectorhq.com/widget/form/${formId}`}
        style={{ width: '100%', height: `${height}px`, border: 'none' }}
        scrolling="no"
      />
    </div>
  )
}
```

Para el calendario:
```tsx
// Embed de GHL Calendar
export function GHLCalendar({ calendarId }: { calendarId: string }) {
  return (
    <iframe
      src={`https://api.leadconnectorhq.com/widget/booking/${calendarId}`}
      style={{ width: '100%', height: '700px', border: 'none' }}
      scrolling="no"
    />
  )
}
```

Los IDs de formulario y calendario se dejan como variables de entorno en `.env.local`:
```
NEXT_PUBLIC_GHL_FORM_ID_FISICO=
NEXT_PUBLIC_GHL_FORM_ID_DIGITAL=
NEXT_PUBLIC_GHL_CALENDAR_ID=
```

### Step 6: Configuración de Tailwind con colores del cliente

```ts
// tailwind.config.ts
import type { Config } from 'tailwindcss'

const config: Config = {
  content: ['./app/**/*.{ts,tsx}', './components/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        // Colores del cliente — reemplazar con pantones reales
        brand: {
          primary: '#[COLOR_PRIMARIO]',
          bg: '#[COLOR_FONDO]',
          text: '#FFFFFF',
          muted: '#[COLOR_GRAFITO]',
          accent: '#[COLOR_ACENTO]',
        }
      },
      fontFamily: {
        display: ['[FUENTE_DISPLAY]', 'sans-serif'],
        body: ['[FUENTE_BODY]', 'sans-serif'],
      }
    }
  }
}
export default config
```

### Step 7: README con instrucciones

Generar un `README.md` con:
- Requisitos (Node 18+)
- Cómo correr en local (`npm install && npm run dev`)
- Variables de entorno necesarias (GHL IDs)
- Cómo deployar en Vercel (3 pasos)
- Estructura de carpetas explicada

### Step 8: Quality check

Antes de entregar, verificar:
- [ ] Todos los componentes tienen copy real, sin placeholders
- [ ] Los colores del cliente están aplicados correctamente via Tailwind
- [ ] Cada sección tiene animación Framer Motion implementada
- [ ] Los formularios GHL están embebidos (con variable de entorno para el ID)
- [ ] El proyecto corre con `npm run dev` sin errores
- [ ] Responsive en mobile verificado (breakpoints correctos)
- [ ] El `README.md` tiene instrucciones claras para deployar

---

## Output

### Archivos generados
Todo el código en: `clientes/{slug}/outputs/{slug}-landing/`

### Confirmar al usuario
1. Número de componentes generados
2. Secciones implementadas
3. Variables de entorno que debe completar (GHL IDs)
4. Comando para correr: `cd clientes/{slug}/outputs/{slug}-landing && npm install && npm run dev`
5. Próximo paso: revisar en local → completar GHL IDs → deploy en Vercel

---

## Quality Standards
- [ ] El diseño no es genérico — tiene una dirección estética clara y específica al cliente
- [ ] No hay Inter, Roboto, Arial ni gradientes purple/white genéricos
- [ ] Cada sección del wireframe está implementada como componente independiente
- [ ] Las animaciones tienen intencionalidad — no son decorativas sin propósito
- [ ] El código es limpio, tipado (TypeScript), y sin console.logs
- [ ] Un developer puede tomarlo y deployar sin preguntar nada (README completo)