# CreActive Studio — Agency OS Context

> Este archivo es el contexto maestro de CreActive Studio para Claude Code.
> Debe estar en la raíz del proyecto principal de la agencia.
> Cada skill hereda automáticamente este contexto.

---

## 1. Identidad de la agencia

**Nombre legal:** CREACTIVE STUDIO SPA  
**RUT:** 78.387.691-4  
**Representante legal:** Oscar Diego Vergara Barros  
**Domicilio tributario:** El Yodo 8180 DP 2603, Cumbres del Mar, Antofagasta  
**Inicio de actividades:** 01-04-2026  
**Régimen tributario:** Pro Pyme Transparente  
**Marca comercial:** CreActive Studio  
**Web:** creactivestudio.agency  
**Correo tributario:** hola@creactivestudio.agency  
**Ubicación operativa:** Colombia (base) / Chile (registro legal)  
**Fundador:** Oscar Vergara Barros  
**Tipo de operación:** Solopreneur con red de colaboradores externos  

**Posicionamiento:**
CreActive Studio es un consultor experto que transforma negocios con IA. No somos una agencia de diseño ni un estudio creativo tradicional. Somos el socio operacional que implementa sistemas reales — marketing, automatización, productos digitales — y los entrega funcionando, no en PowerPoint.

**Frase interna que define el trabajo:**
> "Ejecutamos lo que otros solo proponen."

---

## 2. Servicios

CreActive ofrece seis líneas de servicio que se combinan según el cliente:

1. **Transformación operacional con IA (Operación 90)** — consultoría 1:1 de alta intensidad. Diagnóstico pagado ($300-$500 USD) + implementación en 30-90 días ($1.5K-$3K USD setup + $500-$1K USD/mes retainer). Framework: Radiografía → Quick Win → Arquitectura → Deploy → Evolución. Garantía: resultado medible en 30 días o es gratis. Tiers: Activate / Accelerate (principal) / Transform. ICP: "El Operador Solo" — emprendedor 28-40, LATAM, negocio de servicios, $3M-$15M CLP/mes. Dolor: "el negocio no funciona sin mí."
2. **Marketing digital** — Meta Ads, contenido orgánico, estrategia de redes sociales, carruseles, videos, reels
3. **Desarrollo web y landing pages** — WordPress, diseño orientado a conversión, integración con CRM
4. **Automatizaciones** — n8n, GHL workflows, WhatsApp Business API, integraciones entre plataformas
5. **SaaS y productos digitales** — desarrollo de webapps con Next.js + Supabase + Claude API, modelos de revenue share
6. **Consultoría estratégica** — sesiones de discovery, roadmaps, acompañamiento en decisiones de negocio

---

## 3. Stack tecnológico oficial

Estas son las herramientas que CreActive domina y recomienda por defecto:

| Categoría | Herramienta | Uso |
|-----------|-------------|-----|
| CRM / Marketing automation | GoHighLevel (GHL) | Gestión de contactos, pipelines, calendarios, automatizaciones |
| Automatización | n8n | Workflows complejos, integraciones API, lógica de negocio |
| CMS / Web | WordPress | Sitios de clientes, landings, blogs |
| Backend / DB | Supabase | Proyectos SaaS, autenticación, storage |
| Pauta | Meta Ads | Campañas Facebook e Instagram |
| Mensajería | WhatsApp Business API | Automatizaciones conversacionales, notificaciones |
| Video IA | HeyGen / Higfield | Videos con avatares IA usando voz de Oscar |
| Documentación | Notion | Wikis de cliente, SOPs, seguimiento de proyectos |
| IA | Claude API (Anthropic) | Motor de inteligencia en productos y skills internas |
| Video / Media | ffmpeg | Compresión de video para web, generación de thumbnails |

**Regla:** Antes de proponer una herramienta nueva, verificar si alguna del stack ya resuelve el problema. Agregar herramientas solo cuando hay un gap real.

---

## 4. Clientes activos

### CreActive Studio (clientes directos)

| Cliente | Servicios | Modelo | Valor mensual |
|---------|-----------|--------|---------------|
| **Pumpalcerro** | Web + CRM + Meta Ads | Retainer | $97K CLP/mes |
| **Rivas Legal** | Web + AI chat | Retainer | $70K CLP/mes |
| **Constanza Nutrición** | Landing + PDF automation + Meta Ads + webapp (Nutrisco) | Revenue share 30% | Variable |
| **PH Labs** | Web + CRM (GHL calendarios, pipelines, flujos automáticos) + contenido | Setup + retainer | $500 USD + $97K CLP/mes |
| **FWC Ellinger** | Landing + Google Business Profile + firma correo + opt. redes | Pro bono (caso de éxito) | $0 |

### Prospectos activos
| Prospecto | Slug | Estado |
|-----------|------|--------|
| **Pizzas Pelikan Express** | `pizzas-pelikan-express` | Propuesta enviada — pendiente confirmación de Jessica. Proyecto: preparación y venta de negocio ($60M–$90M CLP). |
| **Fundación Terapia** | `fundacion-terapia` | Propuesta enviada — sin CLAUDE.md todavía |
| **Easyway Chile** | `easywaychile` | Análisis de marca completado — flujo PRO landing en proceso |

### Red / Contactos estratégicos
| Contacto | Slug | Descripción | Estado |
|----------|------|-------------|--------|
| **Héctor Partida Bazo** | `autoritas-ai` | Creador de ARENA — herramienta de testing de agentes IA. Madrid. Posible colaboración: Oscar testa agentes de Kitcha/Nutrisco con ARENA; Oscar apoya con feedback comercial. | Primera reunión 17-04-2026. Follow-up pendiente. |

### Ex clientes / inactivos
| Cliente | Slug | Nota |
|---------|------|------|
| **Mallku Consulting** | `mallku-consulting` | Relación terminada. Carpeta con outputs históricos en `/clientes/mallku-consulting/`. |

**Regla:** Al generar cualquier documento relacionado con un cliente, usar siempre su nombre, industria y contexto correcto. Nunca mezclar información entre clientes.

---

## 5. Proyectos en desarrollo

### Nutrisco
SaaS de nutrición co-desarrollado con Constanza Nutrición.
- **Stack:** Next.js + Supabase + Claude API + Mercado Pago + GHL
- **Modelo:** Revenue share con Constanza
- **MVP:** Planes nutricionales con IA, check-ins quincenales, comunidad WhatsApp
- **Estado:** MVP funcional al 90%. QA completado. Pendiente: pagos Mercado Pago + webhook. Beta ~18 abril 2026.

### Nutrisco Landing Page
Landing page de venta para Nutrisco — convierte a los 290 compradores del ebook en suscriptores fundadores.
- **Stack:** Next.js 14 + Tailwind CSS + Framer Motion
- **Repo:** https://github.com/creactive-dev/nutrisco-landing
- **Ruta local:** `clientes/constanza-nutricion/outputs/nutrisco-landing/`
- **Features:** Hero "El Siguiente Capítulo", bento 7 features, sección Constanza, testimonios, precio fundador ($19.990/mes), FAQ 8 preguntas, design system Modern Apothecary amplificado
- **Estado:** Build completado (0 errores TS). Pendiente: assets de Constanza (foto, testimonios, link MP), deploy Vercel, dominio.

### FWC Ellinger Landing
Landing page para Full View Content (Sebastián Ellinger) — producción audiovisual en Santiago.
- **Stack:** Next.js + Tailwind CSS + Framer Motion + Resend
- **Repo:** https://github.com/creactive-dev/fwc
- **Features:** Video hero, tour 360° Kuula embebido, formulario de cotización, WhatsApp, stats animados
- **Estado:** Build completado, feedback ronda 1 aplicado. Pendiente deploy Vercel + dominio .CL

### Kitcha (White Cassini — nombre interno)
SaaS multi-tenant de menú digital y gestión de pedidos para restaurantes con automatización WhatsApp vía Kapso. Marca comercial: **Kitcha**. Nombre técnico interno: White Cassini.
- **Stack:** Vanilla JS (customer app) + React 19 + Vite + Tailwind (admin panel) + Supabase (DB, Auth, Realtime, Edge Functions, Storage) + Kapso (WhatsApp Business API)
- **Repo app:** `Proyectos Internos/white-cassini/`
- **Landing de venta:** `Proyectos Internos/kitcha-landing/` — Next.js 16 + Tailwind v4 + Framer Motion. Precios: Starter $29.990/mes, Pro $59.990/mes. Pendiente: deploy Vercel + repo en `creactive-dev/kitcha-landing`
- **Deploy:** Admin en Vercel (`white-cassini-admin.vercel.app`), customer app en Vercel (`white-cassini-sigma.vercel.app`)
- **Estado:** En producción. Track A completado. Track B (migración customer app a Preact + Vite) — estado pendiente confirmar.

### ContentOps
SaaS de marketing operacional end-to-end: ideación → generación → preview → publicación → métricas → optimización. Primero para CreActive Studio (Operación 90 + marca personal de Oscar). Después multi-tenant para clientes.
- **Stack:** Next.js 14+ (App Router) + Tailwind CSS + shadcn/ui + Supabase + n8n + Claude API
- **Ruta local:** `Proyectos Internos/contentops/`
- **Dominio:** ops.creactivestudio.agency
- **Deploy:** Vercel
- **Documentación:** PRD.md completo (18 secciones + 3 apéndices) + CLAUDE.md del proyecto
- **Modelo de revenue:** Tres líneas — (1) uso interno para marketing de Operación 90, (2) implementación como servicio para clientes, (3) SaaS multi-tenant con suscripción mensual vía Mercado Pago
- **Estado:** PRD completado (v1.0). Pendiente ejecución Fase 0 (Foundation: schema Supabase + scaffold Next.js + deploy Vercel + seed data).

### CreActive Studio Web (web propia)
Landing page de la agencia — creactivestudio.agency.
- **Stack:** Next.js 14 + Tailwind CSS 3 + Framer Motion + TypeScript
- **Repo:** https://github.com/creactive-dev/creactive.git
- **Ruta local:** `clientes/creactive-studio/outputs/creactive-studio-landing/`
- **Features:** Hero con stats reales, AboutOscar con foto y quote, Services bento grid con CpuArchitecture animado, carrusel infinito de logos, HowWeWork AS IS/TO BE/EJECUTAR, 3 casos de éxito, testimonios pull-quote, footer neo-minimal
- **Estado:** En producción. i18n ES/EN + dark mode implementados. Toggles en Navbar (desktop + mobile). Sección Niches reconstruida ("Para quién trabajamos" — dos columnas: criterios de fit + sectores). Mobile corregido: overflow-x, hero badge, HowWeWork cards, CaseStudies borders, Footer wrap, AboutOscar. Pendiente: push a Vercel, conectar dominio .agency, OG image.

---

## 6. Modelos de precio

CreActive opera con cuatro modelos según el tipo de proyecto:

| Modelo | Cuándo usarlo |
|--------|---------------|
| **Retainer mensual fijo** | Servicios continuos: web + CRM + ads + soporte |
| **Revenue share** | Productos digitales donde CreActive co-construye y co-opera |
| **Proyecto one-time + mantenimiento opcional** | Landings, automatizaciones puntuales, setups |
| **Paquetes fijos (Starter / Growth / Full)** | Propuestas rápidas para nuevos prospectos |

**Regla:** Los precios son fijos. No hay scope creep. Si el cliente pide algo fuera del acuerdo, se cotiza por separado.

---

## 7. Cómo trabaja CreActive

### Filosofía de entrega
- **MVP primero, iteración después.** Entregar algo funcionando rápido es mejor que entregar algo perfecto tarde.
- **Documentar todo.** Cada proyecto tiene su brief, su PRD o scope, y su checklist de entrega.
- **Proponer más de lo que el cliente pide.** Siempre incluir al menos una recomendación proactiva en cada entregable.

### Reglas de oro (no negociables)
1. **Nunca prometer fechas sin buffer.** Toda fecha estimada lleva al menos 20% de margen.
2. **Siempre tener una propuesta visual antes de desarrollar.** Wireframe, mockup o estructura aprobada antes de escribir código o copy final.
3. **Todo proyecto necesita un brief escrito.** Sin brief, no empieza el trabajo.
4. **El cliente aprueba antes de avanzar cada fase.** No se asume aprobación por silencio.
5. **Los precios son fijos.** Sin scope creep. Cambios fuera del alcance = nueva cotización.

### Flujo estándar de un proyecto
```
Discovery (reunión + transcrito)
→ Brief escrito
→ Propuesta comercial
→ Aprobación del cliente
→ Desarrollo / producción (MVP)
→ Revisión interna (checklist)
→ Presentación al cliente
→ Ajustes aprobados
→ Entrega final
→ Onboarding / capacitación
→ Seguimiento mensual
```

---

## 8. Comunicación y tono

### Con clientes
- **Cercano y conversacional.** Hablamos como personas, no como corporaciones.
- **Simple, sin jerga innecesaria.** Si hay que usar un término técnico, explicarlo en la misma oración.
- **Con datos y ejemplos concretos.** Las afirmaciones van acompañadas de números o ejemplos reales.
- **Empático pero directo.** Si algo no funciona o no es viable, se dice claramente y se propone alternativa.

### Idioma
- **Español por defecto** en todo lo que va al cliente.
- **Spanglish técnico** en documentos internos: términos como "landing", "CRM", "workflow", "brief", "retainer" se usan en inglés dentro de texto en español — es natural en el contexto tech latinoamericano.
- **Inglés completo** solo cuando el contexto lo requiere explícitamente (cliente angloparlante, documentación técnica, prompts de skill).

### Qué evitar siempre
- Lenguaje corporativo vacío ("sinergia", "valor agregado", "soluciones integrales")
- Promesas sin sustento
- Respuestas genéricas que podrían ser para cualquier cliente
- Listas innecesariamente largas cuando un párrafo basta

---

## 9. Nichos objetivo

CreActive tiene expertise comprobado y casos de éxito en:

1. **Salud y bienestar** — nutricionistas, médicos, coaches de salud (caso: Constanza Nutrición)
2. **Legal y servicios profesionales** — abogados, consultores, contadores (caso: Rivas Legal)
3. **Restaurantes y food** — dark kitchens, delivery, gestión de pedidos (experiencia previa: PedidosYa)
4. **E-commerce y retail** — tiendas online, marketplaces, logística
5. **Educación y coaches** — infoproductores, mentores, academias online

**Regla:** Al hacer diagnósticos o propuestas para prospectos nuevos, priorizar referencia a casos del nicho correspondiente.

---

## 10. Contexto personal del fundador

**Oscar Vergara Barros**
- Nacido en 1991, autodidacta, sin título universitario formal
- Background: B2B SaaS sales (ADP Chile), operaciones a escala (PedidosYa — 70+ dark kitchens, +300% crecimiento), retail delivery multinacional (Mallplaza — 4M órdenes)
- Inglés nivel IELTS 7 — comunicación fluida en contextos profesionales
- Vivió en Australia; actualmente en Colombia
- Meta financiera: $5–10K USD/mes en ingresos recurrentes como consultor de transformación operacional

**Cómo afecta esto al trabajo:**
El background de Oscar no es el de un diseñador ni un desarrollador — es el de un operador. Los entregables de CreActive deben reflejar pensamiento sistémico, orientación a resultados, y capacidad de ejecutar a escala. Eso es lo que diferencia a CreActive de otras agencias.

---

## 11. Instrucciones para Claude Code

### Al ejecutar cualquier skill
1. Leer este CLAUDE.md primero para entender el contexto de la agencia
2. Si existe un CLAUDE.md específico del cliente en `/clientes/{slug}/CLAUDE.md`, leerlo también antes de generar output
3. Nunca generar contenido genérico — siempre personalizar con el contexto del cliente o proyecto

### Convenciones de archivos

- `clientes/{slug}/CLAUDE.md` — contexto del cliente
- `clientes/{slug}/estado.md` — estado actual + próximo hito (actualizar en cada sesión)
- `clientes/{slug}/outputs/` — todos los entregables generados
- `clientes/{slug}/Transcritos/` — grabaciones y transcritos de reuniones
- `Proyectos Internos/{nombre}/` — proyectos SaaS propios (Kitcha/white-cassini)
- `content-engine/brand/` — voz, pilares, patrones de contenido y design system de Oscar
- `plantillas/` — templates reutilizables (propuestas, etc.)
- `.claude/commands/` — slash commands (un .md por comando)

### Prioridades al generar outputs
1. **Relevancia sobre completitud** — mejor un output corto y preciso que uno largo y genérico
2. **Accionable sobre informativo** — cada output debe terminar con próximos pasos claros
3. **Cliente primero** — el lenguaje siempre habla al cliente, no al equipo interno
4. **Consistencia de marca** — tono cercano, ejemplos concretos, sin jerga vacía

### Cuándo pedir clarificación
- Si el transcrito de reunión está incompleto o ambiguo en puntos clave
- Si el cliente solicitado no existe en `/clientes/`
- Si hay contradicción entre lo que pide el usuario y las reglas de oro de la sección 7

---

## 12. Skills disponibles

> ✅ = construida y lista | 🔲 = pendiente de construir
> Ruta base: `.claude/commands/{nombre}.md`

### Proyectos (`proyectos/`) — prefijo `pro-`
| Comando | Estado | Descripción |
|---------|--------|-------------|
| `/pro-prd-landing` | ✅ | Genera PRD completo para landing page desde transcrito de reunión |
| `/pro-estructura-landing` | ✅ | Convierte PRD en estructura detallada de secciones con wireframe y copy base |
| `/pro-plan-trabajo` | ✅ | Genera cronograma de construcción con fases, gates de aprobación y checklist QA |
| `/pro-build-landing` | ✅ | Genera código completo Next.js + Tailwind + Framer Motion desde estructura aprobada |

**Flujo de uso:**
```
/cli-contexto-cliente --cliente=slug
→ /sal-followup --cliente=slug
→ /pro-prd-landing --cliente=slug
→ revisión + aprobación cliente
→ /pro-estructura-landing --cliente=slug
→ aprobación cliente
→ /pro-plan-trabajo --cliente=slug
→ /pro-build-landing --cliente=slug
→ entrega
```

### Contenido (`contenido/`) — prefijo `cnt-`
| Comando | Estado | Descripción |
|---------|--------|-------------|
| `/cnt-video-brief` | ✅ | Brief por escenas para producción con avatar HeyGen |
| `/cnt-content-plan` | ✅ | Plan de contenido semanal (IG + Reels + Threads) con búsqueda de tendencias |
| `/cnt-carrusel` | ✅ | Estructura y copy para carrusel de Instagram/LinkedIn — genera JSON + slides HTML |
| `/cnt-caption` | ✅ | Caption + hashtags listos para publicar |
| `/cnt-reel-guion` | ✅ | Guión completo para reel/HeyGen desde tema o idea |
| `/cnt-thread` | ✅ | Thread para Threads desde tema o carrusel existente |

**Contexto requerido por comandos cnt-:** `content-engine/brand/voz.md`, `content-engine/brand/pilares.md`, `content-engine/brand/hormozi-patterns.md`

### Ventas (`ventas/`) — prefijo `sal-`
| Comando | Estado | Descripción |
|---------|--------|-------------|
| `/sal-propuesta` | ✅ | Genera propuesta comercial en 3 fases → HTML A4 desde `plantillas/propuesta-comercial/template.html` |
| `/sal-diagnostico` | 📝 | Stub — estructura pendiente |
| `/sal-followup` | ✅ | Correo de follow-up post reunión — output en `outputs/correos/` |

### Clientes (`clientes/`) — prefijo `cli-`
| Comando | Estado | Descripción |
|---------|--------|-------------|
| `/cli-contexto-cliente` | ✅ | Genera CLAUDE.md del cliente desde transcrito + actualiza CLAUDE.md raíz |
| `/cli-onboarding` | 📝 | Stub — estructura pendiente |
| `/cli-reporte` | 📝 | Stub — estructura pendiente |
| `/cli-minuta` | 📝 | Stub — estructura pendiente |

### Documentos — skill `doc-oficial`
| Skill | Estado | Descripción |
|-------|--------|-------------|
| `doc-oficial` | ✅ | Genera PDFs profesionales con identidad visual CreActive (ReportLab). Incluye módulo base reutilizable en `.claude/skills/doc-oficial/scripts/creactive_pdf.py` |

### Plantillas reutilizables (`plantillas/`)
| Plantilla | Ruta | Descripción |
|-----------|------|-------------|
| Propuesta comercial | `plantillas/propuesta-comercial/template.html` | HTML A4 — usada por `/sal-propuesta` |
| **Presentación de consultoría** | `plantillas/presentacion-consultoria/template.html` | Reveal.js 12 slides dark mode CreActive — para sesiones de consultoría, propuestas y diagnósticos. Ver `COMO-USAR.md` en la misma carpeta. |

**Flujo para nueva presentación:**
```
cp plantillas/presentacion-consultoria/template.html \
   clientes/{slug}/outputs/presentacion-{tipo}-{fecha}.html
→ buscar/reemplazar todos los {{VARIABLES}}
→ cp al public/propuestas/ del repo creactivestudio.agency → push → live en Vercel
```

### Admin — prefijo ninguno
| Comando | Estado | Descripción |
|---------|--------|-------------|
| `/workspace-audit` | ✅ | Auditoría completa del workspace: inventario, gaps, inconsistencias y próximos pasos → genera `workspace-estado.md` |
| `/cierre-sesion` | ✅ | Cierra sesión al ~60–70% de contexto: documenta lo hecho, actualiza memoria del proyecto y genera handoff listo para copiar-pegar |

### Principio de mantenimiento del CLAUDE.md raíz
Cualquier cambio estructural de la agencia debe reflejarse aquí:
- **Nuevo cliente** → `/cli-contexto-cliente` lo actualiza automáticamente
- **Nuevo skill construido** → el proceso de construcción incluye actualizar la tabla de la sección 12
- **Nuevo proyecto en desarrollo** → agregar manualmente a la sección 5

---

*Última actualización: 2026-04-17*
*Mantener este archivo actualizado con cada nuevo cliente, skill, o cambio en el modelo de negocio.*