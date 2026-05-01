# Contexto de Cliente — Constanza Nutrición / Nutrisco
**Slug:** `constanza-nutricion`
**Última actualización:** Marzo 2026
**Responsable CreActive:** Oscar Vergara Barros

---

## 1. Datos del cliente

**Empresa / Marca:** Constanza Nutrición
**Producto SaaS:** Nutrisco
**Contacto principal:** Constanza (nutricionista)
**Ubicación:** Chile
**Idioma:** Español chileno
**Canal de comunicación:** WhatsApp + email
**Perfil técnico:** Profesional de la salud con manejo básico-medio de herramientas digitales — entiende el "para qué" pero delega el "cómo" al equipo técnico

---

## 2. Historial de servicios con CreActive

### Fase 1 — Presencia digital + activo digital (✅ Completado)

| Servicio | Detalle |
|----------|---------|
| Página web completa | 5 páginas |
| Landing Page | Venta de activo digital (PDF Reto Antiinflamatorio) |
| Activo Digital | PDF "Reto Antiinflamatorio 21 días" |
| Gestión de Meta Ads | Campaña para venta del activo digital |
| Flujos automatizados | Entrega automática del PDF vía GHL + n8n |

**Modelo comercial Fase 1:** $1.000 USD setup + 30% de las ventas
**Resultados validados:**
- Precio ebook: $17.990 CLP
- Clientes: 290
- Ingresos totales: $5.217.100 CLP
- Inversión en ads: $1.000.000 CLP
- **ROI: 421%**

### Fase 2 — SaaS de nutrición (🔨 En desarrollo)
Proyecto activo: plataforma web app **Nutrisco** bajo modelo de revenue share (30%).

---

## 3. Sobre el negocio — Constanza Nutrición

**Especialidad:** Nutrición antiinflamatoria
**Metodología actual:** Screening inicial → asignación manual de pauta → seguimiento quincenal por WhatsApp
**Problema central:** El modelo no escala — respuestas por WhatsApp, seguimiento manual y asignación de pautas consumen demasiado tiempo

**Base de clientes:** 290 compradores validados del ebook — lista caliente para conversión al SaaS
**Canal de adquisición:** Meta Ads + base de clientes del ebook

**Target de usuario final:**

| Atributo | Descripción | Implicancia de producto |
|----------|-------------|------------------------|
| Edad | 28–50 años | UX intuitivo, no técnico |
| Género | Mayoritariamente femenino | Tono empático, estética cuidada |
| Motivación | Reducir inflamación, mejorar energía y digestión, bajar de peso/grasa | Resultados visibles, dashboard de progreso |
| Pain point | No saben qué comer, no mantienen constancia | Planes claros, recordatorios, comunidad |
| Canal de entrada | Meta Ads + base del ebook | Onboarding simple post-pago |
| Dispositivo | Mayoritariamente móvil | Mobile-first obligatorio (375px+) |

**Casos especiales a contemplar en el screening:** embarazadas, alto rendimiento deportivo, vegetarianas/veganas.

---

## 4. Sobre el producto — Nutrisco

**Concepto:** Plataforma web app de nutrición personalizada y seguimiento automatizado, construida sobre la metodología antiinflamatoria de Constanza, con IA para asignación de pautas y soporte 24/7.

**Visión futura (B2B):** Licenciar la plataforma a otras nutricionistas para gestionar sus propios pacientes bajo su metodología.

### Escenarios de MRR proyectados

| Escenario | Suscriptores | Precio/mes | MRR |
|-----------|-------------|-----------|-----|
| Conservador | 100 | $19.990 CLP | $1.999.000 CLP |
| Moderado | 200 | $24.990 CLP | $4.998.000 CLP |
| Optimista | 400 | $29.990 CLP | $11.996.000 CLP |

### Stack tecnológico

| Capa | Tecnología | Justificación |
|------|-----------|--------------|
| Frontend | Next.js 14 + Tailwind CSS | SEO, performance, mobile-first, componentes reutilizables |
| Backend / DB | Supabase | Auth, PostgreSQL, storage y realtime sin infraestructura propia |
| IA (matching + ajuste) | Claude API (Anthropic) | Asignación de pautas, sugerencias de ajuste, agente de soporte |
| Pagos | Mercado Pago | Suscripciones recurrentes en CLP, alta adopción en Chile |
| CRM / Automatizaciones | GoHighLevel (GHL) | Emails, SMS, seguimiento de leads, landing pages |
| Agente de soporte | GHL IA + Claude API | Chatbot entrenado con pautas y FAQ, escalación a nutricionista |
| Comunidad MVP | WhatsApp Groups | Cero fricción, cero desarrollo, ideal para < 500 usuarios |
| Email transaccional | Resend | Bienvenida, recordatorios, notificaciones de ajuste |
| Hosting | Vercel | Deploy continuo de Next.js, CDN global, escalado automático |
| Boletas electrónicas | VSale (integración externa) | Boletas exentas de IVA — argumento de venta clave (reembolso isapre) |

### Flujo principal de datos

```
USUARIO
 |-- Pago (Mercado Pago) --> Webhook --> Supabase (crea cuenta)
 |-- Screening --> Next.js --> Claude API --> Selección de pauta
 |-- Check-in --> Supabase --> Claude API --> Sugerencia de ajuste
 |-- Chat soporte --> GHL / Claude API --> Respuesta o ticket

NUTRICIONISTA
 |-- Dashboard --> Supabase --> Vista de suscriptores y métricas
 |-- Ajustes pendientes --> Aprobación con 1 clic --> Supabase actualiza pauta
 |-- Soporte escalado --> GHL bandeja --> Respuesta manual
```

---

## 5. Módulos y funcionalidades

### Vista general por módulo

| Módulo | Funcionalidad core | Usuario | Fase |
|--------|-------------------|---------|------|
| Onboarding | Screening + asignación de pauta por IA | Paciente | MVP |
| Plan alimentario | Visualización de pauta semanal personalizada | Paciente | MVP |
| Recetario | Recetas vinculadas + lista de compras | Paciente | MVP |
| Check-in quincenal | Formulario de seguimiento + ajuste IA | Paciente + Nutricionista | MVP |
| Soporte IA | Chat de dudas sobre el plan asignado | Paciente | MVP |
| Dashboard nutricionista | Gestión de pautas, aprobaciones, métricas | Nutricionista | MVP |
| Pagos y suscripción | Suscripción mensual + gestión de acceso | Paciente | MVP |
| Comunidad | Grupo WhatsApp moderado | Paciente | MVP (simple) |
| Panel B2B | Licencia para otras nutricionistas | Nutricionista externa | Fase 2 |

---

### Módulo 1 — Onboarding / Screening

**Flujo de usuario:**
1. Usuario completa el pago en la landing page (Mercado Pago)
2. Es redirigido a la webapp y crea su cuenta
3. Completa el screening (8–12 preguntas)
4. La IA analiza respuestas y selecciona la pauta más adecuada del catálogo
5. El usuario ve su plan asignado
6. Recibe email de bienvenida con acceso al grupo de WhatsApp

**⚠️ UX crítico:** No entregar el plan de inmediato — simular revisión humana con mensaje tipo *"El equipo de Constanza está revisando tus respuestas, en 24 horas tendrás tu plan"* para mantener percepción de personalización.

**Preguntas del screening (draft — validar con Constanza):**

| N° | Pregunta | Variable que mapea |
|----|---------|-------------------|
| 1 | Objetivo principal (reducir inflamación / bajar de peso / mejorar energía / digestión) | Objetivo |
| 2 | Diagnóstico médico previo (celiaquía, SII, tiroides, ninguno, otro) | Restricción clínica |
| 3 | Alergias o intolerancias alimentarias | Restricción alimentaria |
| 4 | Nivel de actividad física (sedentario / moderado / activo) | Nivel calórico aproximado |
| 5 | Hábitos de cocina (cocino diario / poco / no cocino) | Complejidad de recetas |
| 6 | Alimentos que no consume por preferencia | Exclusiones voluntarias |
| 7 | Síntoma principal actual (fatiga / hinchazón / dolor / piel / ninguno) | Prioridad de protocolo |
| 8 | Cuántas comidas hace al día | Estructura del plan |
| 9 | Presupuesto semanal de alimentación (bajo / medio / alto) | Tipo de ingredientes |
| 10 | Cuánto tiempo lleva con estos síntomas | Nivel de cronicidad |

---

### Módulo 2 — Motor de Asignación de Pautas (IA)

El motor NO genera planes desde cero: selecciona la pauta correcta del catálogo y sugiere ajustes quincenales.

**Flujo de asignación:**
1. Respuestas del screening → vector de variables del paciente
2. Catálogo de pautas → etiquetado con variables compatibles
3. Claude API matchea el vector del paciente con el catálogo
4. Selecciona la pauta con mayor compatibilidad
5. Si hay empate → la nutricionista es notificada para decisión manual

**Etiquetado del catálogo de pautas** (sesión de trabajo con Constanza):

| Variable | Valores posibles |
|----------|----------------|
| Objetivo principal | Antiinflamatorio / Pérdida de peso / Energía / Digestión |
| Restricciones clínicas | Sin restricción / Celiaquía / SII / Hipotiroidismo / Combinaciones |
| Nivel calórico | Bajo / Medio / Alto |
| Complejidad de preparación | Simple / Media / Elaborada |
| Número de comidas | 3 / 4 / 5 comidas |
| Fase del protocolo | Inicial / Mantenimiento / Avanzado |
| Síntoma prioritario | Hinchazón / Fatiga / Piel / Dolor / General |

**Ajuste quincenal:** Cada 15 días el sistema genera un prompt con el historial de check-ins + pauta actual y solicita a Claude API una sugerencia de ajuste. Constanza aprueba o rechaza con un clic desde su dashboard.

---

### Módulo 3 — Plan Alimentario

**Vistas principales:**
- **Vista semanal:** Calendario de 7 días con desayuno, almuerzo, once y cena
- **Vista de día:** Detalle de cada comida con ingredientes y preparación simplificada
- **Lista de compras:** Generada automáticamente desde el plan de la semana, agrupada por categoría (verduras, proteínas, lácteos, etc.)
- **Historial:** Pautas anteriores para comparar progreso

**Reglas de UX:**
- Plan siempre visible sin necesidad de descargar PDF
- Usuario puede marcar comidas como "completadas" (gamificación de adherencia)
- Diseño mobile-first — funcionar perfectamente en smartphones desde 375px
- Usuario NO puede editar su plan directamente — cambios solo vía chat de soporte o check-in quincenal

---

### Módulo 4 — Recetario

- Catálogo indexado por ingredientes antiinflamatorios, vinculado a las pautas
- Cada pauta tiene un subconjunto de recetas asignadas
- Búsqueda por ingrediente disponible
- Cada receta incluye: ingredientes, porciones, tiempo de preparación, calorías aproximadas, etiquetas (sin gluten, sin lácteos, etc.)
- Recetas de la semana se agregan automáticamente a la lista de compras
- Usuarios pueden guardar recetas como favoritas

**Responsabilidad de Constanza:** Proveer mínimo 40 recetas en formato estructurado antes del lanzamiento.

---

### Módulo 5 — Seguimiento de Hábitos y Check-in

**Check-in diario (opcional / gamificado) — 3 preguntas:**
- Energía hoy: 1–5
- Digestión hoy: 1–5
- Adherencia al plan: Sí / Parcial / No

**Check-in quincenal (obligatorio — activa el motor de ajuste IA):**

| Dimensión | Preguntas |
|-----------|----------|
| Síntomas | Nivel de hinchazón, fatiga, dolor digestivo (escala 1–5) |
| Energía general | Comparación con quincena anterior |
| Adherencia real | Porcentaje de días que siguió el plan |
| Dificultades | Qué comidas le costaron más y por qué |
| Cambios de contexto | Viajes, eventos sociales, estrés |
| Objetivo actualizado | ¿Sigue siendo el mismo o cambió? |
| Peso | Registro quincenal |

**Dashboard de progreso del usuario:**
- Gráfico de tendencia: energía y digestión en el tiempo
- Gráfico de evolución de peso
- Racha de días con check-in completado (streak)
- Número de comidas marcadas como completadas en la semana
- Fase actual del protocolo y progreso hacia la siguiente

---

### Módulo 6 — Agente de Soporte con IA

**Alcance estricto:** Responde únicamente dudas relacionadas con la pauta actualmente asignada al usuario. NO hace onboarding, NO vende, NO realiza check-in.

**Flujo de conversación:**
```
Usuario envía pregunta en el chat
Sistema inyecta contexto: pauta asignada + FAQ + historial reciente del paciente
Claude API genera respuesta contextualizada
→ Si la duda está dentro del scope: responde de inmediato
→ Si la duda escapa del scope: "Esta duda la revisará [Constanza] en menos de 24 horas"
→ Se crea ticket automático en GHL para la nutricionista
```

**Base de conocimiento inicial:**
- 10–30 pautas digitalizadas y estructuradas
- FAQ con mínimo 50 preguntas frecuentes (extraídas de WhatsApp de Constanza)

**Mejora continua:** Preguntas escaladas se revisan semanalmente y las respuestas validadas se integran al FAQ.

**Límites del agente:**
- No diagnostica ni da recomendaciones clínicas
- No modifica el plan del usuario
- Ante síntoma grave → remite al profesional de salud
- Sin memoria persistente entre sesiones en MVP

---

### Módulo 7 — Dashboard de la Nutricionista

**MVP:**
- Vista de todos los suscriptores activos con pauta asignada y fecha de último check-in
- Bandeja de ajustes pendientes: sugerencias IA para aprobar/rechazar con un clic
- Bandeja de soporte: tickets escalados por el agente IA con historial de conversación
- Métricas generales: suscriptores activos, churn, adherencia promedio, NPS

**Fase 2:**
- Editor de pautas del catálogo directamente en la plataforma
- Creación de nuevas pautas desde el dashboard
- Gestión de contenido del recetario
- Reportes exportables por paciente

---

### Módulo 8 — Pagos y Suscripción

| Plan | Precio | Detalle |
|------|--------|---------|
| Precio fundador | $19.990 CLP/mes | Primeras 2 semanas post-lanzamiento — precio bloqueado de por vida |
| Mensual estándar | $24.990 CLP/mes | Suscripción recurrente mensual vía Mercado Pago |
| Plan anual | $19.990 CLP/mes equivalente (~20% off) | Pago único anual — Fase 2 |

**Lógica de acceso:**
- Acceso habilitado automáticamente al confirmarse el pago (webhook Mercado Pago → Supabase)
- Fallo en cobro recurrente → 3 intentos en 5 días → suspensión de acceso
- Usuario suspendido conserva datos por 30 días → puede exportar sus datos
- Durante suspensión: check-ins desactivados, acceso de solo lectura

**Facturación:** Integración con VSale para boletas electrónicas exentas de IVA.
**⚠️ Argumento de venta clave:** El paciente puede reembolsar el costo vía isapre — diferenciador crítico en el copy de lanzamiento.

---

## 6. Funcionalidades fuera de scope MVP

| Funcionalidad | Evaluación futura |
|---------------|------------------|
| App nativa iOS / Android | V2 — una vez validado el negocio |
| Videollamadas o consultas en vivo dentro de la plataforma | V2+ |
| Integración con wearables (Fitbit, Apple Health, Garmin) | V3+ |
| Generación de planes 100% desde cero con IA | Descartado — mantener control clínico |
| Panel B2B para nutricionistas externas | V3+ |
| Sistema de referidos / afiliados | V2 |
| Módulo de cursos / contenido educativo estructurado | V2 (usar plataforma de comunidad externa) |
| Comunidad dentro de la webapp | V2 (MVP usa WhatsApp) |
| Facturación electrónica integrada nativamente | Integración externa con VSale |
| Soporte multidioma | No en MVP |
| Módulo de suplementos con links de venta y comisión | V2 |
| Tips cotidianos (sueño, cortisol, organización de cocina) | V2 |
| Alarmas/recordatorios de agua y colaciones | V2 |
| Cálculo de calorías por foto o entrada manual | No en MVP |
| Integración directa con supermercados | Futuro lejano |

---

## 7. Objetivos y KPIs

### Objetivos de negocio

| Hito | Meta | Plazo |
|------|------|-------|
| Beta cerrada | 50–80 clientes del ebook como beta testers | ~11 abril 2026 |
| Lanzamiento público | Precio fundador activo 2 semanas | Semana 13 (~fines abril 2026) |
| Suscriptores activos | 80 | Mes 1 (mayo 2026) |
| Suscriptores activos | 200 | Mes 3 (julio 2026) |
| MRR objetivo | $4.000.000 CLP | Mes 3 |
| Conversión desde ebook | 30% de los 290 clientes | Primeros 60 días post-lanzamiento |
| Churn | < 5% mensual | Objetivo sostenido |

### KPIs del producto

| KPI | Meta Mes 1 | Meta Mes 3 | Meta Mes 6 |
|-----|-----------|-----------|-----------|
| Suscriptores activos | 80 | 200 | 400 |
| Churn mensual | < 8% | < 5% | < 3% |
| Tasa completitud check-in | 50% | 70% | 75% |
| Resolución IA soporte | 60% | 80% | 85% |
| NPS | > 30 | > 50 | > 60 |
| Conversión base ebook | 20% | 35% | 50% |

---

## 8. Roadmap de desarrollo

### Fase 0 — Preparación (Semanas 1–2)

| Tarea | Responsable |
|-------|-------------|
| Entregar 10–30 pautas en PDF o Word | Constanza |
| Sesión de etiquetado del catálogo (90 min) | Constanza + CreActive |
| Mapear preguntas del screening actual | Constanza |
| Validar lógica de asignación de pautas | Constanza + CreActive |
| Construir FAQ inicial (50+ preguntas) | Constanza |
| Definir recetas iniciales del recetario (mín. 40) | Constanza |
| Configurar GHL: pipeline, automatizaciones, dominio | CreActive |
| Configurar Mercado Pago: suscripción recurrente | CreActive |
| Configurar cuenta Claude API y estimar costos | CreActive |
| Diseñar estructura de base de datos (usuarios, pautas, check-ins, tickets) | CreActive |

### Fase 1 — MVP (Semanas 3–8)

| Semana | Módulo | Entregable |
|--------|--------|-----------|
| 3 | Infraestructura | Supabase + Auth + DB + deploy en Vercel |
| 3 | Catálogo pautas | Pautas digitalizadas y etiquetadas en DB |
| 4 | Onboarding | Screening completo + flujo de registro post-pago |
| 4 | Motor IA | Integración Claude API: asignación de pauta |
| 5 | Plan alimentario | Vista semanal y de día del plan asignado |
| 5 | Lista de compras | Generación automática desde el plan semanal |
| 6 | Check-in | Formulario quincenal + dashboard de progreso |
| 6 | Ajuste IA | Sugerencia quincenal + bandeja nutricionista |
| 7 | Soporte IA | Agente en GHL entrenado con pautas y FAQ |
| 7 | Pagos | Suscripción recurrente Mercado Pago + webhook |
| 8 | Recetario | Catálogo vinculado a pautas + favoritos |
| 8 | Testing | QA completo, ajustes UX, prep beta |

### Fase 2 — Beta cerrada (Semanas 9–12)
- 50–80 clientes del ebook como beta testers (gratis o con descuento)
- Feedback estructurado: encuesta + entrevistas con 10 usuarios
- Iteración sobre módulos con mayor fricción
- Validar que el agente resuelve ≥60% de dudas sin escalar
- Validar que el motor asigna correctamente según criterio de Constanza

### Fase 3 — Lanzamiento público (Semana 13+)
- Secuencia de 4 emails a los 290 clientes del ebook
- Meta Ads a audiencia lookalike del 1–3% basado en los 290 compradores
- Inscripción con precio fundador por 2 semanas
- Monitoreo diario de KPIs durante las primeras 4 semanas

---

## 9. Estrategia de lanzamiento

### Secuencia de emails — base de 290 clientes

| Email | Timing | Contenido |
|-------|--------|-----------|
| Email 1 — Anuncio | Semana 8 | "Fuiste parte del programa de 21 días. Ahora hay algo más grande." Pre-lanzamiento + lista de espera |
| Email 2 — Historia | Semana 10 | Mostrar el problema que resuelve el SaaS vs el ebook. Sin precio todavía |
| Email 3 — Precio fundador | Semana 12 | Oferta exclusiva: $19.990/mes bloqueado de por vida si se suscriben en los próximos 14 días |
| Email 4 — Urgencia | Día 10 del lanzamiento | "Quedan X cupos al precio fundador." Cierre real de la oferta |
| WhatsApp | Paralelo | Mensaje directo a quienes están en el grupo del programa original |

### Retención y reducción de churn
- Recordatorio automático de check-in quincenal vía email + WhatsApp (GHL)
- Email de reengagement si el usuario no hace check-in en 10 días
- Email de cancelación proactiva: si el cobro falla, ofrecer pausa de 1 mes antes de cancelar
- Celebración de hitos: "Completaste tu primer mes", "Llevas 3 meses en el programa"

### Meta Ads
- Audiencia principal: lookalike 1–3% basado en los 290 compradores del ebook
- Audiencia secundaria: intereses en nutrición antiinflamatoria, salud intestinal, gut health, celiaquía, tiroides
- **Creativos: testimonios de beta testers + antes/después de síntomas — NO de peso** (instrucción de Constanza)
- Objetivo de campaña: conversiones (pago en la landing page)
- Presupuesto inicial sugerido: $500.000 – $800.000 CLP/mes

---

## 10. Requerimientos no funcionales

| Categoría | Requerimiento |
|-----------|--------------|
| Performance | Carga en menos de 2 segundos en conexión 4G desde Chile |
| Disponibilidad | Uptime mínimo 99.5% mensual |
| Seguridad | Autenticación vía Supabase Auth (JWT). Datos de salud cifrados en reposo |
| Privacidad | Cumplimiento con Ley 19.628 de protección de datos personales de Chile |
| Mobile-first | Funcionar sin degradación en pantallas de 375px+ |
| Escalabilidad | Soportar hasta 2.000 usuarios activos sin refactoring mayor |
| Accesibilidad | Contraste mínimo WCAG AA en todos los componentes de UI |
| Respaldo | Backups diarios automáticos en Supabase |

---

## 11. Riesgos y mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|---------|-----------|
| Constanza no entrega el material a tiempo | Alta | Alto | Fecha límite con contrato. Sesiones agendadas en calendario |
| Motor asigna pautas incorrectas | Media | Alto | Supervisión manual de Constanza en beta. Ajuste de prompt y etiquetado |
| Baja conversión de los 290 clientes | Media | Medio | Secuencia de emails + precio fundador con urgencia real. Meta Ads en paralelo |
| Churn alto en primeros 60 días | Media | Alto | Onboarding de alta fricción positiva, comunidad activa, check-in gamificado |
| Agente de soporte da información incorrecta | Media | Alto | Scope estricto. Escalación automática ante dudas clínicas |
| Competencia con apps de nutrición establecidas | Baja | Medio | Diferenciación: metodología clínica real, IA contextualizada, protocolo específico |

---

## 12. Dependencias críticas (bloquean el desarrollo)

| # | Dependencia | Fecha límite | Responsable |
|---|------------|-------------|-------------|
| 1 | Pautas digitalizadas — sin esto la IA no funciona | Fin Semana 1 | Constanza |
| 2 | FAQ inicial (50+ preguntas) — sin esto el agente no puede entrenarse | Fin Semana 2 | Constanza |
| 3 | Recetario inicial (40+ recetas) — puede postergarse a Fase 2 | Fin Semana 6 | Constanza |
| 4 | Cuenta Mercado Pago verificada con suscripciones habilitadas | Fin Semana 2 | Constanza + CreActive |
| 5 | GHL configurado: CRM, automatizaciones, dominio, agente IA | Fin Semana 2 | CreActive |

---

## 13. Cómo comunicarse con Constanza

- **Tono:** Cercano, profesional, empático — habla de sus pacientes con compromiso real
- **Nivel técnico:** Básico-medio — explicar el "para qué" antes del "cómo"
- **Decisiones:** Le gustan las opciones con contexto claro — no asumir tecnicismos
- **Seguimiento:** Activo — tiene mucho pendiente de su parte, hacer seguimiento sin que se sienta presionada
- **Motivación:** Muy entusiasmada con el proyecto — aprovechar esa energía para avanzar los pendientes
- **Documentos:** Enviar todo junto en un solo correo cuando sea posible — evitar emails separados por ítem

---

## 14. Notas internas

- Los 290 clientes del ebook son la lista de conversión más valiosa — la estrategia de precio fundador está diseñada exactamente para ellos
- **Beta cerrada planificada para ~11 de abril 2026** — cumpleaños de Constanza, motivación extra para esa fecha
- **⚠️ Facturación crítica:** Constanza pagó más IVA del esperado con las ventas del ebook porque no configuró correctamente la exención en Mercado Pago — resolver antes del lanzamiento investigando VSale
- **Argumento de venta más potente del lanzamiento:** boleta exenta de IVA + reembolso vía isapre — debe estar en el copy de todos los canales
- Ella mencionó interés en contenido de suplementos, sueño y cortisol — dejarlo como "módulo próximamente" visible en la plataforma para generar expectativa y reducir churn
- La sesión mensual live ya está resuelta usando plataforma de comunidad externa — no desarrollar esa funcionalidad dentro de Nutrisco en MVP
- El modelo B2B (otras nutricionistas) está en el horizonte pero NO en el scope actual
- **Creativos de Meta Ads:** antes/después de síntomas (hinchazón, energía, digestión), NO de peso — instrucción explícita de Constanza

---

## 15. Estado actual del proyecto (Abril 2026)

> Estado técnico completo y actualizado en `Nutrisco/CLAUDE.md`.

**Resumen:** MVP funcional al 90%. Build 26 rutas, 0 errores TypeScript.
- ✅ Fases 0, 0.5, 1 completadas (Auth, Motor IA, Check-ins, Recetario, Dashboard Nutricionista, Soporte IA, PWA, QA)
- 🔨 Pendiente: Webhook Mercado Pago + acceso por suscripción
- 🎯 **Beta cerrada:** ~18 abril 2026
- 🎯 **Lanzamiento público:** fines de abril 2026

---

## 16. Glosario

| Término | Definición |
|---------|-----------|
| Pauta | Plan alimentario pre-diseñado por Constanza para un perfil específico de paciente |
| Catálogo de pautas | Conjunto de 10–30 pautas disponibles, etiquetadas con variables de matching |
| Screening | Cuestionario de onboarding que captura el perfil del usuario para asignarle la pauta correcta |
| Motor de asignación | Sistema basado en Claude API que hace match entre el perfil del usuario y el catálogo de pautas |
| Check-in quincenal | Formulario de seguimiento completado cada 15 días que alimenta el ajuste de pauta |
| Ajuste de pauta | Sugerencia generada por la IA para cambiar o mantener la pauta, aprobada por Constanza |
| Agente de soporte | Chatbot basado en Claude API entrenado con pautas y FAQ para responder dudas del plan |
| MRR | Monthly Recurring Revenue — ingresos recurrentes mensuales por suscripciones activas |
| Churn | Tasa de cancelación mensual — % de suscriptores que cancelan en un mes dado |
| GHL | GoHighLevel — plataforma de CRM y automatizaciones usada para emails, SMS y agente de soporte |
| NPS | Net Promoter Score — métrica de cuántos clientes promueven activamente el servicio |
| Precio fundador | Precio de lanzamiento bloqueado de por vida para los primeros suscriptores |

---

*Generado por CreActive Studio — Marzo 2026*
*Fuentes: PRD Nutrisco v1.0 + Transcripción de reunión de revisión con Constanza*