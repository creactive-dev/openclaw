# Contexto de Cliente — CreActive Studio (Proyecto interno)
**Slug:** `creactive-studio`
**Última actualización:** Marzo 2026
**Responsable CreActive:** Oscar Vergara Barros

---

## 1. Datos del cliente

**Empresa:** CREACTIVE STUDIO SPA (marca comercial: CreActive Studio)
**Web:** creactivestudio.agency
**Contacto principal:** Oscar Vergara Barros (fundador)
**Ubicación:** Colombia (operaciones) / Chile (registro legal)
**Idioma:** Español latinoamericano con spanglish técnico natural
**Canal de comunicación:** N/A — proyecto interno
**Perfil:** Proyecto propio de la agencia — el estándar de calidad debe ser el más alto porque esta landing ES nuestro portafolio y primera impresión.

---

## 2. Sobre el negocio

**Descripción en sus propias palabras:**
> "CreActive Studio es un consultor experto que transforma negocios con IA. No somos una agencia de diseño ni un estudio creativo tradicional. Somos el socio operacional que implementa sistemas reales — marketing, automatización, productos digitales — y los entrega funcionando, no en PowerPoint."

**Eslogan:** *Ejecutamos lo que otros solo proponen.*

**Servicios (6 líneas):**
1. **Transformación operacional con IA** (SERVICIO PRINCIPAL) — diagnóstico de procesos, implementación de workflows con IA, capacitación interna
2. Marketing digital — Meta Ads, contenido orgánico, estrategia de redes sociales
3. Desarrollo web y landing pages — WordPress, Next.js, diseño orientado a conversión, integración CRM
4. Automatizaciones — n8n, GHL workflows, WhatsApp Business API, integraciones entre plataformas
5. SaaS y productos digitales — desarrollo de webapps con Next.js + Supabase + Claude API, modelos de revenue share
6. Consultoría estratégica — sesiones de discovery, roadmaps, acompañamiento en decisiones de negocio

**Propuesta de valor:**
- No proponemos — ejecutamos e implementamos
- Background operacional real (PedidosYa, Mallplaza, ADP) no teórico
- Entrega MVP en 2-4 semanas, no en meses
- Precios fijos, sin scope creep
- Stack moderno probado en producción (GHL, n8n, Next.js, Supabase, Claude API)

**Nichos objetivo:**
1. Salud y bienestar (caso: Constanza Nutrición / Nutrisco)
2. Legal y servicios profesionales (caso: Rivas Legal)
3. Restaurantes y food (experiencia: PedidosYa — 70+ dark kitchens)
4. E-commerce y retail (experiencia: Mallplaza — 4M órdenes)
5. Educación y coaches

**Clientes activos (para social proof):**
- Pumpalcerro — Web + CRM + Meta Ads
- Rivas Legal — Web + AI chat
- Constanza Nutrición — Landing + automation + webapp Nutrisco (revenue share)
- PH Labs — Web + GHL calendar
- FWC Ellinger — Landing + Google Business Profile (pro bono)

---

## 3. Estado del proyecto

### Servicios (proyecto interno)
| Servicio | Detalle | Estado |
|----------|---------|--------|
| Landing page | Next.js + Tailwind CSS + Framer Motion + GHL | 🔨 En construcción |

**Stack:** Next.js 14 + Tailwind CSS + Framer Motion + Lucide React
**Deploy:** Vercel en creactivestudio.agency
**Modelo:** Proyecto interno — sin deadline externo, pero prioridad alta

---

## 4. Identidad visual

### Paleta de colores
| Color | Hex | Uso |
|-------|-----|-----|
| Brand Red | `#FF3231` | CTAs principales, energía, acción inmediata |
| Brand Blue | `#578BDE` | Headings secundarios, confianza, enlaces |
| Brand Teal | `#2FB8C5` | IA/innovación, badges, acentos terciarios |
| Background | `#F8FAFC` | Fondo principal |
| Background Alt | `#F1F5F9` | Fondo secciones alternas |
| Surface | `#FFFFFF` | Cards, modals |
| Text Primary | `#0F172A` | Headings |
| Text Body | `#334155` | Cuerpo de texto |
| Text Muted | `#64748B` | Labels, metadata |
| Border | `#E2E8F0` | Bordes de cards, inputs |

### Reglas de color
- Máximo 2 colores de marca por sección
- Brand Red SOLO para CTAs y elementos de acción
- Fondo siempre light — NO dark mode
- Secciones alternas entre `#F8FAFC` y `#FFFFFF`

### Tipografía
- **Headings:** Plus Jakarta Sans (600, 700, 800)
- **Body:** DM Sans (400, 500)
- **Mood:** Friendly, modern, tech, approachable, professional

### Estilo visual
- Light moderno — fondo claro, limpio, profesional
- Whitespace generoso
- Sombras sutiles en cards
- Sin imágenes decorativas genéricas
- Iconos: Lucide React (SVG, nunca emojis)
- Animaciones: Framer Motion — reveal on scroll, stagger children, card hover lift
- Border radius: 8px (buttons/inputs), 12px (cards), 16px (featured)

### Assets disponibles
- Logo CreActive Studio (pendiente confirmar formato SVG)
- Sin foto profesional de Oscar aún (usar placeholder o generar con IA)

---

## 5. Referencias visuales

| Referencia | Qué tomar |
|-----------|-----------|
| Stripe | Storytelling en bloques, limpio, tech |
| Linear | Light mode elegante, tipografía moderna |
| Vercel | Tech-forward, minimalismo con impacto |
| Loom | Friendly SaaS, accesible, trust through simplicity |

---

## 6. Flujos y automatizaciones requeridas

### Flujo único — Agendar llamada discovery
```
Visitante hace clic en CTA "Agendar discovery"
→ Scroll suave a sección de booking (#agendar)
→ Calendario GHL embebido (30 min, sin compromiso)
→ Confirmación automática por email
→ Reminder 24h antes
→ Contacto guardado en CRM con tag "lead-web-agency"
```

**No hay flujo secundario.** La landing tiene un solo objetivo: agendar la llamada.

---

## 7. Pendientes del cliente (internos)

| # | Pendiente | Urgencia | Para qué |
|---|-----------|---------|---------|
| 1 | Logo SVG definitivo | 🔴 Alta | Header y favicon |
| 2 | Foto profesional de Oscar | 🟡 Media | Sección "Sobre Oscar" |
| 3 | GHL Calendar ID para discovery | 🔴 Alta | Sección de booking |
| 4 | Aprobación de clientes para case studies | 🟡 Media | Sección "Casos reales" |
| 5 | OpenGraph image | 🟢 Baja | Social sharing |

---

## 8. Comunicación y tono (para el copy de la landing)

- **Cercano y conversacional** — hablamos como personas, no como corporación
- **Simple, sin jerga vacía** — nada de "sinergia", "valor agregado", "soluciones integrales"
- **Con datos y ejemplos concretos** — métricas reales, casos reales
- **Empático pero directo** — si algo no aplica, se dice claro
- **Spanglish natural** — "landing", "CRM", "workflow", "brief" en inglés dentro de texto en español
- **Target:** Dueños de PYME en LATAM que saben que necesitan IA/marketing/automatización pero no tienen tiempo ni equipo para hacerlo solos

---

## 9. Notas internas

- Esta landing ES el portafolio de CreActive — cada detalle de diseño y copy refleja la calidad del trabajo que hacemos para clientes
- El background de Oscar no es diseñador ni developer — es operador. Los entregables reflejan pensamiento sistémico y orientación a resultados
- Métricas de Oscar (no de CreActive): PedidosYa (+300% crecimiento, 70+ dark kitchens), Mallplaza (4M órdenes), ADP Chile (B2B SaaS sales)
- Métricas de CreActive: 5 clientes activos, 3 países, primer entregable en 2-4 semanas
- Meta financiera de Oscar: $5-10K USD/mes en ingresos recurrentes

---

## 10. Decisiones técnicas

| # | Decisión | Opción elegida | Razón |
|---|----------|---------------|-------|
| 1 | Estilo visual | Light moderno | Diferencia de PH Labs (dark), posiciona como accesible/profesional |
| 2 | CTA principal | Agendar llamada discovery (GHL) | Patrón probado de conversión |
| 3 | Foco de servicios | IA transformation como hero | Diferenciador principal vs. agencias genéricas |
| 4 | Tipografía | Plus Jakarta Sans + DM Sans | Modern + friendly + tech, NO Inter/Roboto |
| 5 | Iconos | Lucide React | Consistente, SVG, no emojis |
| 6 | Framework | Next.js + Tailwind + Framer Motion | Mismo stack de todos los proyectos, probado |
| 7 | Deploy | Vercel en creactivestudio.agency | Consistente con clientes |
| 8 | Componentes UI | 21st.dev Magic MCP | Componentes modernos de calidad |
| 9 | Design system | ui-ux-pro-max | Sistema de diseño profesional persistido |
| 10 | Idioma | Español LATAM | Target audience es LATAM |

---

*Generado por CreActive Studio — Marzo 2026*
*Proyecto interno — sin transcrito de reunión, brief sintético en `/Transcritos/`*
