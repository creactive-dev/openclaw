# CLAUDE.md — Pumpalcerro
**Slug:** `pumpalcerro`
**Última actualización:** Marzo 2026
**Responsable CreActive:** Oscar Vergara Barros

> Contexto de cliente para uso interno de CreActive Studio Agency.
> Este archivo es parte del Agency OS. No compartir con el cliente directamente.

---

## 1. Datos del Cliente

| Campo | Detalle |
|---|---|
| **Empresa** | Pumpalcerro |
| **Web** | pumpalcerro.com |
| **Tipo de negocio** | Comunidad y agencia de trekking exclusiva para mujeres |
| **Fundación** | 2020 |
| **Ubicación operativa** | Santiago y Región del Maule, Chile |
| **Contacto principal** | Michi (María Isabel Astorga) — Socia Fundadora |
| **Email** | pumpalcerro@gmail.com |
| **WhatsApp** | +569 3860 2203 |
| **Idioma** | Español (Chile) |
| **Perfil técnico** | Rápida para aprender, muy motivada — entiende bien herramientas nuevas si se le explica el "para qué" |

---

## 2. Sobre el Negocio

**Descripción:** Pumpalcerro organiza aventuras de trekking exclusivas para mujeres, en un entorno seguro, guiado por mujeres certificadas, con fuerte sentido de comunidad.

**Tagline:** *"Aventuras de trekking para mujeres que transforman"*

**Concepto central:** No es solo trekking — es un espacio de superación personal, conexión con la naturaleza y formación de vínculos reales. La "cordada" (comunidad) tiene vida propia más allá de cada salida.

**Diferenciadores clave:**
- Guías mujeres, muchas certificadas (WAFA, UIMLA)
- Ambiente 100% femenino, libre de juicios
- Accesible para todos los niveles, sin experiencia previa requerida
- Protocolos de seguridad documentados
- Reconocidas por SERNATUR como iniciativa de trekking femenino con propósito (2026)

---

## 3. Audiencia Objetivo

**Perfil principal:** Mujeres adultas (25–55 años), residentes en Santiago o ciudades donde operan, que:
- Buscan actividad física con propósito y comunidad
- No tienen experiencia en montaña o quieren retomar el hábito
- Valoran la seguridad, la calidez del equipo y el ambiente femenino
- Están dispuestas a pagar por una experiencia guiada y profesional

**Perfil secundario:** Empresas que buscan actividades outdoor para equipos (tienen página dedicada `/empresas`)

---

## 4. Servicios / Productos

### Tipos de Aventura
| Tipo | Descripción |
|---|---|
| **Aventura AM** | Caminata de mañana, duración corta |
| **Aventura PM** | Caminata de tarde |
| **Full Day** | Jornada completa en montaña |
| **Aventura Nacional** | Destinos fuera de Santiago dentro de Chile (ej. Valle del Elqui, Maule, Achibueno) |
| **Aventura Internacional** | Expediciones fuera de Chile |

### Rango de precios (actividades actuales)
- Aventuras cortas (3 hrs): desde **$15.000 CLP**
- Full Day / aventuras largas: desde **$30.000 a $75.000 CLP**

### Otros productos
- **Tienda online** (equipo, merchandise)
- **Servicios para empresas** (team building outdoor)
- **Lead magnet:** Guía PDF gratuita "Cómo Hacer tu Primer Trekking"

---

## 5. Estado del Proyecto

| Servicio | Estado | Notas |
|---|---|---|
| Web (WordPress) | ✅ Entregada y activa | pumpalcerro.com |
| CRM (GHL) | ✅ Activo | Flujos corriendo, pendiente documentar |
| Landing Valle del Elqui | ✅ Live | elqui.pumpalcerro.com — Next.js + Tailwind + Framer Motion |
| Meta Ads — Valle del Elqui | 🔨 Lista para lanzar | Piezas aprobadas. Falta flujo de conversión (sesión 2026-04-08) |

### Campaña activa: Valle del Elqui
- **Producto:** Viaje grupal 21–23 mayo 2026. $690.000 CLP (reserva con $200.000). 11 cupos disponibles.
- **Doc campaña:** `outputs/campaña-meta-ads-valle-elqui-v1.md`
- **Landing:** `outputs/pumpalcerro-landing/` — live en `elqui.pumpalcerro.com`
- **Presupuesto:** CBO $10.000 CLP/día. Deadline ventas: 6 mayo 2026.
- **Piezas gráficas:** Aprobadas por Michi. Listas para subir a Meta Ads Manager.
- **Modelo de comisión CreActive sobre utilidad por venta:**

| Cupos vendidos | Comisión |
|---|---|
| 0 – 10 pax | 10% |
| 10 – 12 pax | 12% |
| 12 – 15 pax | 15% |

> ⚠️ La comisión es sobre **utilidad por venta**, NO sobre gestión del servicio.

### Flujo de compra (arquitectura)

```
Cliente en landing → PaymentModal (captura nombre/email/teléfono)
→ fbq('track', 'InitiateCheckout')
→ POST /api/lead → GHL (crea contacto + oportunidad)
→ Redirect a MercadoPago (link mpago.la/...)
→ Cliente paga
→ MP: redirect success → elqui.pumpalcerro.com/gracias
→ MP IPN → n8n webhook (async)
   ├── GET /v1/payments/{id} con Access Token MP
   ├── IF status = "approved"
   │   ├── Meta Conversions API → evento Purchase (server-side)
   │   └── GHL → actualiza oportunidad "Pagó" + dispara correo
→ /gracias: fbq('track', 'Purchase') client-side (respaldo)
```

### Links MercadoPago (hardcodeados en `lib/constants.ts`)

| Plan | Link | Precio |
|---|---|---|
| Reserva débito/transferencia | mpago.la/17Ncwvy | $200.000 |
| Pago completo débito/transferencia | mpago.la/2iTvU4u | $690.000 |
| Reserva crédito | mpago.la/1aL3kAF | $212.291 |
| Pago completo crédito | mpago.la/2eWjbQT | $770.347 |

### Pendientes técnicos — sesión 2026-04-08

| # | Tarea | Detalle |
|---|---|---|
| 1 | Pedir Access Token MP a Michi | Necesario para que n8n consulte el detalle del pago |
| 2 | Crear `/gracias` en la landing | Página post-pago con fbq Purchase client-side |
| 3 | Crear workflow n8n | Webhook → GET payment MP → IF approved → Meta Conversions API + GHL |
| 4 | Editar 4 links MP | Agregar success URL: `https://elqui.pumpalcerro.com/gracias` |
| 5 | Configurar IPN en cuenta MP | Cuenta → Configuraciones → Notificaciones IPN → URL webhook n8n |
| 6 | Setear env vars en Vercel | `NEXT_PUBLIC_META_PIXEL_ID` + `GHL_WEBHOOK_URL` |
| 7 | Pago de prueba end-to-end | Verificar que todo el flujo dispara correctamente |

---

## 6. Stack Tecnológico

| Componente | Tecnología |
|---|---|
| CMS | WordPress |
| Plugin de viajes | WP Travel Engine (Travel Monster) |
| Idiomas | Español (es_CL) / Inglés (en_US) vía TranslatePress |
| Pagos | MercadoPago |
| CRM | GoHighLevel (gestionado por CreActive) |
| Redes sociales | Instagram / TikTok — gestionadas por el cliente |
| Dominio web principal | pumpalcerro.com |
| Landing campañas | Next.js 14 + Tailwind + Framer Motion — elqui.pumpalcerro.com |
| DNS | Cloudflare |
| Hosting landing | Vercel |
| Automatización | n8n (flujo webhook MP → Meta + GHL) |

---

## 7. Identidad Visual y Tono de Marca

### Tono de comunicación
- **Cálido, cercano e inspirador** — hablan de "cordada", "pumpitas", "cerrito"
- Lenguaje femenino y empoderador, nunca condescendiente
- Mezcla de emoción y profesionalismo
- Usan emojis con moderación en redes sociales
- Valores centrales: seguridad, superación, conexión, comunidad
- **Evitar:** Lenguaje técnico de montaña sin explicar, tono masculino, elitismo deportivo

---

## 8. Equipo Pumpalcerro

| Nombre | Rol | Formación / Perfil |
|---|---|---|
| **María Isabel Astorga (Michi)** | Socia Fundadora y Guía — **contacto CreActive** | Trabajadora Social, scout hasta los 27 años, trekking desde los 8 años |
| **Magdalena Parada Bacco (Magda)** | Socia Fundadora y Guía | Arquitecta patrimonial, montañista desde los 20 años |
| **Elisa Sairafi (Eli)** | Guía | Profesora de Ed. Básica, exscout |
| **Fernanda Rodríguez (Feña)** | Guía | Profesora de inglés, birdwatcher |
| **Karol Córdova** | Guía | Guía de montaña UIMLA, cumbres +6000 msnm |
| **Gabriela Barrera (Gabi)** | Guía | Nutricionista, guía de trekking, monitora NDR |
| **Tania Menco Henríquez (Tania)** | Guía | Andinista y escaladora, +15 años de experiencia |
| **María Ignacia Contreras (Nacha)** | Guía | Ing. en gestión de expediciones y ecoturismo, instructora yoga |
| **Camila Espinoza Vargas (Cami)** | Guía | Administradora en Ecoturismo, guardaparque, educadora ambiental |

---

## 9. Cómo Comunicarse con Michi

- **Canales:** WhatsApp (principal), email, videollamada
- **Velocidad:** Responde rápido, toma decisiones con fluidez — no hay que esperar semanas
- **Estilo:** Directa, muy motivada, rápida para aprender herramientas nuevas
- **Cómo presentar ideas:** Explicar el "para qué" antes del "cómo" — ella aprende rápido una vez que entiende el beneficio
- **Decisiones:** Generalmente las toma sola; Magda es socia pero Michi es la cara operativa del proyecto con CreActive
- **Seguimiento:** No es necesario insistir mucho — es proactiva

---

## 10. Flujos GHL

> 🔲 Pendiente documentar — flujos activos pero no registrados en este archivo.
> Oscar compartirá acceso a GHL para levantar la documentación.

---

## 11. Pendientes del Cliente

| # | Pendiente | Urgencia | Para qué |
|---|---|---|---|
| 1 | **Access Token MercadoPago** | 🔴 Alta | n8n necesita el token para consultar el detalle de cada pago vía API |
| 2 | Documentar flujos GHL activos | 🟡 Media | Registro Agency OS |

---

## 12. Decisiones Técnicas Tomadas

| # | Decisión | Opción elegida | Razón |
|---|---|---|---|
| 1 | Gateway de pagos | MercadoPago | Confirmado por el cliente |
| 2 | Gestión de redes sociales | Cliente (Michi/equipo) | CreActive no gestiona RRSS |
| 3 | Modelo comisión ads | % sobre utilidad por venta (escalonado) | Alineado con resultado, no con gestión |

---

## 13. Notas Internas

- La campaña de Valle del Elqui es la primera activación de Meta Ads — importante que salga bien, es la prueba del modelo de comisión por resultados
- Michi es muy receptiva a aprender — cuando se le presenten herramientas nuevas (GHL, reportes de ads, etc.) se puede ir directo sin mucho preámbulo
- Las redes sociales las manejan ellas — no proponer gestión de RRSS como servicio adicional a menos que ellas lo pidan
- El pixel de Meta ya está instalado — lo que falta es el evento Purchase (se dispara vía n8n post-pago MP)
- GHL Form ID de la landing: `HQDlgpOK0beeaQzpiYK8`
- Transferencia bancaria también disponible como opción en la landing (datos BANK en constants.ts)
- **Última actualización:** 2026-04-07 (sesión de planificación campaña)

---

## 14. Relación con CreActive Studio

| Campo | Detalle |
|---|---|
| **Servicios activos** | Web (WordPress) + CRM (GHL) + Meta Ads |
| **Retainer mensual** | $97.000 CLP/mes |
| **Comisión ads** | Escalonada sobre utilidad por venta (ver sección 5) |
| **Gestor de cuenta** | Oscar Vergara (CreActive Studio) |

---

## 15. Assets y Links Clave

| Recurso | URL |
|---|---|
| Web principal | https://www.pumpalcerro.com |
| Nosotras | https://www.pumpalcerro.com/es/about-us/ |
| Actividades | https://www.pumpalcerro.com/es/actividades/ |
| Empresas | https://www.pumpalcerro.com/es/empresas/ |
| Tienda | https://www.pumpalcerro.com/es/tienda/ |
| Blog | https://www.pumpalcerro.com/es/blog/ |
| Guía PDF gratuita | https://drive.google.com/file/d/1EqRkSxRoVhAkZU0bZhQJvcjHcdiXxZBF/view |
| Plan de riesgos | https://drive.google.com/file/d/1u--wqtLNz0xxP_BBg6-Yp9npHKXvXVY_/view |
| Ficha inscripción | https://drive.google.com/file/d/1_xqFMRfpYsRqEsN0GzvGalMR3OL/view |
| WhatsApp contacto | https://wa.me/+56938602203 |

---

*Generado por CreActive Studio — Marzo 2026*
*Fuente: Web pública pumpalcerro.com + briefing Oscar Vergara*