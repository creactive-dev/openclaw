# ContentOps — Product Requirements Document

> Sistema de marketing operacional end-to-end: ideación → generación → publicación → métricas → optimización.
> Primero para CreActive Studio / Operación 90. Después multi-tenant SaaS para clientes.
>
> **Versión:** 2.1
> **Fecha:** 2026-04-16
> **Autor:** Oscar Vergara Barros (CreActive Studio) + Claude
> **Estado:** Spec aprobada — pendiente ejecución

---

## Tabla de contenidos

1. [Visión del producto](#1-visión-del-producto)
2. [Contexto y problema](#2-contexto-y-problema) (incluye Operación 90, ICP, posicionamiento, modelo de revenue)
3. [Stack técnico](#3-stack-técnico)
4. [Modelo de datos](#4-modelo-de-datos)
5. [Flujo operacional](#5-flujo-operacional)
6. [Vistas del frontend](#6-vistas-del-frontend)
7. [Sistema de preview por formato](#7-sistema-de-preview-por-formato)
8. [Motor de inteligencia](#8-motor-de-inteligencia)
9. [Motor de ideas](#9-motor-de-ideas)
10. [Integración de plataformas](#10-integración-de-plataformas)
11. [Publicación y scheduling](#11-publicación-y-scheduling)
12. [Multi-tenant y modelo SaaS](#12-multi-tenant-y-modelo-saas)
13. [Funcionalidades adicionales](#13-funcionalidades-adicionales)
14. [Roadmap de construcción](#14-roadmap-de-construcción)
15. [Estructura del proyecto](#15-estructura-del-proyecto)
16. [Setup previo de plataformas](#16-setup-previo-de-plataformas)
17. [Migración del content engine actual](#17-migración-del-content-engine-actual)
18. [Decisiones de diseño](#18-decisiones-de-diseño)

---

## 1. Visión del producto

ContentOps es un sistema de marketing operacional que cierra el círculo completo del contenido: planificas → generas → previsualizas → apruebas → publicas/programas → las métricas vuelven solas → el sistema aprende → informa la siguiente planificación. Todo desde una sola plataforma, sin salir a Canva, sin copiar entre pestañas, sin Excel de métricas.

**Principio fundacional:** Lo construimos primero para nosotros (CreActive Studio, Operación 90, marca personal de Oscar). Lo validamos con datos reales. Cuando funciona, lo vendemos como SaaS. Cada cliente se auto-administra — nosotros implementamos, el cliente opera.

**Frase que define el producto:**
> "El departamento de marketing que funciona solo."

**Diferenciador vs herramientas existentes (Buffer, Hootsuite, Later):**
Esas herramientas programan posts y muestran métricas. ContentOps genera el contenido con IA usando el contexto real de la marca, aprende qué funciona, alimenta el pipeline de ideas automáticamente, y cierra el loop entre métricas y estrategia. No es un scheduler — es un sistema operacional completo.

---

## 2. Contexto y problema

### 2.1 Quién es el usuario inicial

Oscar Vergara Barros, fundador de CreActive Studio. Opera como solopreneur con red de colaboradores. Su oferta principal es **Operación 90** — consultoría de transformación operacional con IA para PyMEs latinoamericanas.

**Background relevante:**
- Movistar Empresas: ventas B2B
- ADP Chile: District Manager, ventas consultivas SaaS
- PedidosYa: Operations Specialist, 70+ dark kitchens, +300% crecimiento
- Mallplaza: operaciones de delivery, 3 países, 4M+ órdenes, 60% reducción de costos

**Métricas de credibilidad (usables en contenido):**
- 4M+ órdenes gestionadas
- +300% crecimiento en ventas
- 60% reducción de costos
- 70+ operaciones dirigidas

### 2.2 El problema

El contenido de marketing se produce de forma manual, dispersa y sin feedback loop:
- Las ideas viven en la cabeza de Oscar o en JSONs sueltos
- La generación depende de skills de Claude Code ejecutados en terminal
- No hay calendario editorial centralizado
- Las métricas se revisan manualmente entrando a cada plataforma
- No hay sistema que aprenda qué contenido funciona mejor
- No hay fuentes automáticas de ideas (RSS, influencers, competencia)
- La publicación requiere copiar/pegar a cada plataforma
- Cuando se quiera ofrecer como servicio a clientes, no hay nada productizable

### 2.3 Evidencia de tracción

Post del 14 de abril 2026 sobre White Cassini (SaaS para restaurantes construido con Claude Code):
- 21.644 impresiones
- 12.725 personas alcanzadas
- 81 reacciones + 39 comentarios
- 100 visitas al perfil
- 9 nuevos seguidores

El engagement existe. Lo que falta es un sistema para sostenerlo, optimizarlo y escalarlo.

### 2.4 Estrategia de contenido: dos carriles

**Carril 1 — Credibilidad técnica (30% del contenido)**
- Audiencia: devs, founders tech, ingenieros
- Función: autoridad, amplificación, prueba de capacidad técnica
- Temas: lo que Oscar está construyendo (Kitcha, ContentOps, Agency OS), cómo lo construye (Claude Code, stack, decisiones técnicas), reflexiones técnicas honestas

**Carril 2 — Atracción de cliente (70% del contenido)**
- Audiencia: dueños de negocio, operadores, emprendedores 28-40
- Función: generar leads para Operación 90
- Temas: síntomas del negocio operacionalmente atrapado, casos y resultados reales, qué es y cómo funciona Operación 90

**Tensión estratégica:** El contenido técnico recibe más engagement (la audiencia tech es más activa en redes), pero no genera leads directos. La tentación natural es publicar más técnico porque recibe más likes — el sistema debe ayudar a resistir eso manteniendo la distribución 70/30.

### 2.5 ICP — El Operador Solo

Emprendedor de 28-40 años, Chile o LATAM hispanohablante. Tiene un negocio de servicios que él mismo construyó (agencia, consultoría, clínica, estudio jurídico). Factura $3M-$15M CLP/mes. Es su único ingreso. Lleva 2-3+ años.

**Dolor real:** "El negocio no funciona sin mí."
- Todo pasa por su cabeza o por WhatsApp
- Si se va una semana, las cosas se caen
- Gestiona clientes con Excel o memoria
- Toma decisiones sin datos reales
- Perdió leads que nunca supo que perdió

**Compra:** Tiempo de vuelta y escala sin contratar. La tecnología es el medio. La libertad operacional es el resultado.

**Sectores prioritarios:** Proveedores/contratistas mineros, estudios jurídicos, consultoras/agencias, empresas de salud privada.

### 2.6 Oferta — Operación 90

Consultoría 1:1 de alta intensidad. Diagnóstico + implementación en 30-90 días.

**Fase 1 — Diagnóstico pagado:** $300-$500 USD, sesión de 60-90 min, entregable: mapa de 3 cuellos de botella + plan de implementación.

**Fase 2 — Implementación:** $1.500-$3.000 USD setup + $500-$1.000 USD/mes retainer post-implementación.

**Garantía:** Si no hay resultado medible en 30 días → es gratis.

**Tiers:**
| Tier | Nombre | Precio |
|------|--------|--------|
| 1 | Activate | $500-$1.500 setup + $300-$500/mes |
| 2 | Accelerate (principal) | $1.500-$3.000 setup + $500-$1.000/mes |
| 3 | Transform | $3.000-$15.000 + $2.000-$5.000/mes |

### 2.7 Análisis competitivo

| Competidor | País | Diferencial | Debilidad vs Oscar |
|-----------|------|------------|-------------------|
| AI-Think | Chile | 3 fases claras, mención CORFO | Sin casos, sin pricing, sin credencial operacional |
| Cumbre IA | Argentina | Naming memorable, pricing público ($1.5k-$20k) | Sin equipo visible, sin herramientas nombradas |
| NexPO | Argentina | Stack visible (GHL, n8n, Supabase), portafolio | Sin posicionamiento de consultoría, enfoque dev |
| Pylon AI | Chile | Consultoría formal, buen diseño | Sin credencial operacional del fundador |

**Conclusión:** Nadie en LATAM combina credencial operacional real (4M órdenes) + capacidad técnica con IA + posicionamiento de consultor.

### 2.8 Operación 90 — Framework y posicionamiento

**Operación 90** es la oferta central de CreActive Studio. No es una agencia de automatización ni un servicio de marketing. Es consultoría de transformación operacional 1:1 para dueños de negocio que están operacionalmente atrapados — su empresa no funciona sin ellos.

**Framework metodológico — Operational OS (5 fases):**

| Fase | Nombre | Qué se hace |
|------|--------|-------------|
| 1 | Radiografía | Diagnóstico profundo de operaciones, ventas y sistemas actuales |
| 2 | Quick Win | Resultado visible y medible en las primeras 2-4 semanas |
| 3 | Arquitectura | Diseño del sistema operacional completo |
| 4 | Deploy | Implementación con capacitación al equipo del cliente |
| 5 | Evolución | Optimización continua y expansión de capacidades |

**Garantía de Quick Win:** Si no hay un resultado medible en 30 días, es gratis. Esto elimina la principal objeción del cliente y diferencia de todos los competidores que no ofrecen garantía.

**Posicionamiento diferenciador:**

Oscar no es developer ni diseñador — es un operador que usa tecnología. Ese perfil no existe en LATAM. Los tres ingredientes que ningún competidor tiene juntos: criterio operacional real (4M órdenes, 70 dark kitchens), capacidad de implementación técnica (Claude Code, n8n, GHL), y visión de negocio (ex-ADP ventas consultivas SaaS).

Mensaje central:
> *"No soy una agencia de automatización. Soy un operador que ya transformó negocios de 4 millones de órdenes — y ahora usa IA para hacer lo mismo en empresas de tu tamaño, en 90 días."*

### 2.9 Modelo de revenue y cómo encaja ContentOps

CreActive Studio tiene tres líneas de ingreso. ContentOps participa en las tres:

| Línea | Descripción | Rol de ContentOps |
|-------|-------------|-------------------|
| **Consultoría (Operación 90)** | Diagnóstico + implementación 30-90 días. $1.5K-$3K setup + retainer. | ContentOps gestiona el marketing que atrae leads para Operación 90. Es usuario interno. |
| **ContentOps como servicio** | Oscar implementa ContentOps para el cliente dentro de Operación 90 o como servicio separado. | ContentOps es el producto que se instala. Cobro por setup + configuración. |
| **ContentOps SaaS** | Multi-tenant self-service. El cliente paga suscripción mensual y opera solo. | ContentOps es el SaaS. Revenue recurrente escalable. Mercado Pago como gateway. |

**Secuencia estratégica:** Primero la línea 1 (usar ContentOps internamente para validar). Luego la línea 2 (ofrecerlo como parte de Operación 90). Finalmente la línea 3 (abrir el SaaS al público). Esta secuencia asegura que el producto esté validado con datos reales antes de venderlo.

---

## 3. Stack técnico

| Capa | Tecnología | Justificación |
|------|-----------|---------------|
| Frontend | Next.js 14+ (App Router) + Tailwind CSS + Framer Motion | Mismo stack que Kitcha, landings y proyectos internos. Dominio completo. |
| UI Components | shadcn/ui | Componentes accesibles y customizables. Consistencia visual. |
| Backend/DB | Supabase (PostgreSQL + Auth + Storage + Edge Functions + Realtime) | API REST automática, RLS para multi-tenant, realtime para dashboards. Ya en el stack de la agencia. |
| Automatización | n8n (self-hosted) | Workflows de métricas, scheduling, triggers de pipeline. Oscar ya lo domina. |
| Generación IA | Claude API (Anthropic) | Motor de inteligencia para generación de contenido, insights y evaluación de ideas. |
| Storage | Supabase Storage | Imágenes de carruseles, PDFs de LinkedIn, videos, assets de marca. |
| Deploy | Vercel | Mismo que todos los proyectos. Deploy automático desde repo. |
| Dominio | ops.creactivestudio.agency | Subdominio de la agencia. Apuntado a Vercel. |
| Auth | Supabase Auth | Email/password + OAuth providers. Multi-tenant ready con RLS. |
| Publicación | APIs nativas (LinkedIn, Instagram Graph, Threads) | Publicación y scheduling directo desde ContentOps. |
| Notificaciones | WhatsApp Business API | Alertas contextuales y resúmenes semanales. |
| Pagos (Fase 8) | Mercado Pago (primario) | Estándar en LATAM. Mismo mercado que el ICP. Experiencia acumulada con Nutrisco. Stripe solo si se expande fuera de LATAM. |
| Starter base | Supabase + Next.js Auth Starter (Vercel template) | Base para Fase 0. Trae auth + DB configurados. Sin Stripe — billing se agrega en Fase 8 con Mercado Pago. |

---

## 4. Modelo de datos

### 4.1 Core — Organizaciones y usuarios

```sql
-- Organizaciones (multi-tenant)
CREATE TABLE organizations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  plan TEXT NOT NULL DEFAULT 'pro', -- starter | pro | enterprise
  setup_status TEXT NOT NULL DEFAULT 'onboarding', -- onboarding | configuring | active
  setup_by UUID REFERENCES users(id),
  setup_completed_at TIMESTAMPTZ,
  subscription_status TEXT DEFAULT 'trial', -- trial | active | past_due | cancelled
  billing_email TEXT,
  -- Rate limiting Claude API
  claude_generations_used INTEGER DEFAULT 0,
  claude_generations_reset_at TIMESTAMPTZ,
  -- Fallback de aprobación (null = manual siempre; Fase 8: semi_auto | auto)
  approval_timeout_hours INTEGER,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- Usuarios
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  avatar_url TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Membresías (relación user ↔ org)
CREATE TABLE org_members (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  role TEXT NOT NULL DEFAULT 'editor', -- owner | admin | editor | viewer
  invited_by UUID REFERENCES users(id),
  joined_at TIMESTAMPTZ DEFAULT now(),
  status TEXT NOT NULL DEFAULT 'active', -- invited | active | suspended
  UNIQUE(org_id, user_id)
);

-- Acceso temporal de implementador
CREATE TABLE implementation_access (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
  implementor_user_id UUID REFERENCES users(id),
  granted_at TIMESTAMPTZ DEFAULT now(),
  expires_at TIMESTAMPTZ NOT NULL,
  role TEXT NOT NULL DEFAULT 'implementor',
  status TEXT NOT NULL DEFAULT 'active', -- active | expired | revoked
  notes TEXT
);

-- Auto-expiración: n8n cron diario revisa implementation_access
-- WHERE status='active' AND expires_at <= now()
-- → UPDATE status='expired'
-- El implementador puede ser re-invitado por el owner de la org si necesita soporte.
```

### 4.2 Brand y estrategia

```sql
-- Marca (una por org, extensible a múltiples en enterprise)
CREATE TABLE brands (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  voice_doc TEXT, -- markdown: voz de la marca
  design_system_json JSONB, -- colores, fonts, templates
  icp_doc TEXT, -- markdown: perfil de cliente ideal
  offer_doc TEXT, -- markdown: oferta activa (ej: Operación 90)
  competitors_doc TEXT, -- markdown: análisis competitivo
  -- Motor de inteligencia
  relevance_threshold INTEGER DEFAULT 70, -- umbral de relevancia para motor de ideas (0-100)
  score_weights JSONB DEFAULT '{"engagement":0.4,"reach":0.3,"virality":0.2,"conversation":0.1}',
    -- pesos del composite score — revisar y ajustar a los 60 días de datos reales
  review_cycle_days INTEGER DEFAULT 30,
  last_review_at TIMESTAMPTZ,
  next_review_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- Carriles (tracks)
CREATE TABLE tracks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  brand_id UUID REFERENCES brands(id) ON DELETE CASCADE,
  name TEXT NOT NULL, -- "Credibilidad técnica", "Atracción de cliente"
  description TEXT,
  weight_pct INTEGER NOT NULL, -- 30, 70
  color TEXT, -- hex color para UI del calendario
  sort_order INTEGER DEFAULT 0,
  active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Subtemas (dentro de cada carril)
CREATE TABLE topics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  track_id UUID REFERENCES tracks(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  description TEXT,
  hooks TEXT[], -- array de hooks sugeridos
  recommended_formats TEXT[], -- carrusel_ig, reel, thread, etc.
  active BOOLEAN DEFAULT true,
  sort_order INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT now()
);
```

### 4.3 Conexiones de plataformas

```sql
-- Conexiones OAuth a plataformas sociales
CREATE TABLE platform_connections (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
  platform TEXT NOT NULL, -- linkedin | instagram | threads
  access_token TEXT NOT NULL, -- encriptado via Supabase Vault
  refresh_token TEXT,
  token_expires_at TIMESTAMPTZ,
  account_id TEXT, -- ID externo en la plataforma
  account_name TEXT,
  account_url TEXT,
  account_type TEXT, -- personal | business | page
  status TEXT NOT NULL DEFAULT 'active', -- active | expired | disconnected
  connected_at TIMESTAMPTZ DEFAULT now(),
  last_used_at TIMESTAMPTZ,
  UNIQUE(org_id, platform)
);
```

### 4.4 Pipeline de ideas

```sql
-- Ideas de contenido
CREATE TABLE content_ideas (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  brand_id UUID REFERENCES brands(id) ON DELETE CASCADE,
  track_id UUID REFERENCES tracks(id),
  topic_id UUID REFERENCES topics(id),
  title TEXT NOT NULL,
  description TEXT,
  primary_format TEXT, -- carrusel_ig | carrusel_pdf | reel | thread | texto_largo | caption
    -- "primario" porque cada post generado puede adaptar el formato por plataforma
  platforms TEXT[], -- ['linkedin', 'instagram', 'threads']
  status TEXT NOT NULL DEFAULT 'idea',
    -- idea → planned → generating → draft → ready → scheduled → published → archived
    -- Transición: cuando el último post vinculado alcanza 'published', la idea pasa a 'published'
  priority INTEGER DEFAULT 3, -- 1 (highest) to 5 (lowest)
  source TEXT NOT NULL DEFAULT 'manual',
    -- manual | rss | influencer | competitor | ai_suggested | ai_repurpose
  inspiration_url TEXT,
  inspiration_source_name TEXT, -- nombre del feed/influencer/competidor
  source_item_id UUID REFERENCES source_items(id),
  -- Repurposing: trazabilidad
  parent_post_id UUID REFERENCES posts(id),
    -- si la idea viene de repurpose_suggestions, apunta al post original
  -- Motor de ideas: score de relevancia
  relevance_score INTEGER,
    -- 0-100, generado por Claude al evaluar la fuente. Ideas bajo brands.relevance_threshold
    -- van al inbox de descarte (no al pipeline principal). El usuario puede rescatarlas.
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);
```

### 4.5 Posts y contenido generado

```sql
-- Posts (una pieza de contenido publicable)
CREATE TABLE posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  idea_id UUID REFERENCES content_ideas(id),
  brand_id UUID REFERENCES brands(id) ON DELETE CASCADE,
  track_id UUID REFERENCES tracks(id),
  topic_id UUID REFERENCES topics(id),
  platform TEXT NOT NULL, -- linkedin | instagram | threads
  format TEXT NOT NULL,
    -- carrusel_ig | carrusel_pdf | reel | thread | texto_largo | caption | imagen
  content_json JSONB NOT NULL,
    -- Estructura varía por formato:
    -- carrusel_ig: { slides: [{type, html, image_url, alt_text}...] }
    -- carrusel_pdf: { pdf_url, slides_text[], thumbnail_url }
    -- reel: { guion, scenes: [{text, duration, visual, audio}...], video_url }
    -- thread: { posts: [{text, order, image_url?}...] }
    -- texto_largo: { title, body, hashtags[] }
    -- caption: { text, hashtags[], image_url }
    -- imagen: { image_url, alt_text }
  caption TEXT, -- texto que acompaña al post
  cta TEXT, -- call to action específico
  hook_type TEXT, -- verdad_simple | paradoja | reencuadre | lista_friccion | verdad_incomoda
  assets TEXT[], -- URLs a archivos en Storage
  generation_params JSONB,
    -- { skill_used, prompt_hash, brand_context_version, track, topic }
  current_version INTEGER DEFAULT 1,

  -- Scheduling y publicación
  scheduled_at TIMESTAMPTZ,
  published_at TIMESTAMPTZ,
  external_id TEXT, -- ID del post en la plataforma
  external_url TEXT, -- link directo al post publicado
  publish_status TEXT NOT NULL DEFAULT 'draft',
    -- draft → approved → scheduled → publishing → published → failed | blocked
    -- blocked: post programado cuyo token expiró — vuelve a 'scheduled' al reconectar
  publish_error TEXT,
  -- Retry automático (max 3 intentos, backoff exponencial: 15min / 30min / 60min)
  publish_retry_count INTEGER DEFAULT 0,
  next_retry_at TIMESTAMPTZ,

  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- Versionado de posts
CREATE TABLE post_versions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  post_id UUID REFERENCES posts(id) ON DELETE CASCADE,
  version_number INTEGER NOT NULL,
  content_json JSONB NOT NULL,
  caption TEXT,
  cta TEXT,
  change_summary TEXT,
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE(post_id, version_number)
);

-- Comentarios en posts (para aprobación colaborativa)
CREATE TABLE post_comments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  post_id UUID REFERENCES posts(id) ON DELETE CASCADE,
  version_id UUID REFERENCES post_versions(id),
  user_id UUID REFERENCES users(id),
  comment_text TEXT NOT NULL,
  resolved BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT now()
);
```

### 4.6 Métricas y performance

```sql
-- Métricas por post (múltiples snapshots)
CREATE TABLE metrics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  post_id UUID REFERENCES posts(id) ON DELETE CASCADE,
  platform TEXT NOT NULL,
  impressions INTEGER DEFAULT 0,
  reach INTEGER DEFAULT 0,
  reactions INTEGER DEFAULT 0, -- likes, loves, etc.
  comments INTEGER DEFAULT 0,
  reposts INTEGER DEFAULT 0, -- shares, reposts, retweets
  saves INTEGER DEFAULT 0,
  profile_visits INTEGER DEFAULT 0,
  new_follows INTEGER DEFAULT 0,
  link_clicks INTEGER DEFAULT 0,
  engagement_rate NUMERIC(5,4), -- calculado: (reactions+comments+reposts)/reach
  fetched_at TIMESTAMPTZ DEFAULT now(),
  fetch_window TEXT NOT NULL -- 24h | 48h | 7d | 14d | 30d
);

-- Scores calculados por post
CREATE TABLE content_scores (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  post_id UUID REFERENCES posts(id) ON DELETE CASCADE,
  engagement_score INTEGER, -- 0-100, normalizado contra histórico del brand
  reach_score INTEGER, -- 0-100
  virality_score INTEGER, -- reposts+shares relativo al reach
  conversation_score INTEGER, -- comments+replies relativo al reach
  composite_score INTEGER, -- ponderado de los anteriores
  percentile INTEGER, -- percentil vs todos los posts del brand
  calculated_at TIMESTAMPTZ DEFAULT now()
);

-- Benchmarks por dimensión (agregados)
CREATE TABLE performance_benchmarks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  brand_id UUID REFERENCES brands(id) ON DELETE CASCADE,
  dimension TEXT NOT NULL,
    -- track | topic | format | platform | day_of_week | hour | hook_type
  dimension_value TEXT NOT NULL,
    -- ej: "credibilidad_tecnica" | "carrusel_ig" | "miercoles" | "paradoja"
  avg_engagement_rate NUMERIC(5,4),
  avg_reach INTEGER,
  avg_impressions INTEGER,
  avg_reactions INTEGER,
  avg_comments INTEGER,
  sample_size INTEGER NOT NULL,
  trend TEXT, -- improving | stable | declining
  period_start DATE,
  period_end DATE,
  calculated_at TIMESTAMPTZ DEFAULT now()
);

-- Insights generados por IA
CREATE TABLE ai_insights (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  brand_id UUID REFERENCES brands(id) ON DELETE CASCADE,
  type TEXT NOT NULL, -- weekly | monthly | ad_hoc
  period_start DATE,
  period_end DATE,
  insights_json JSONB NOT NULL,
    -- [{ insight, confidence, action, dimension, evidence }]
  generated_at TIMESTAMPTZ DEFAULT now()
);

-- Recomendaciones del sistema
CREATE TABLE recommendations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  brand_id UUID REFERENCES brands(id) ON DELETE CASCADE,
  insight_id UUID REFERENCES ai_insights(id),
  type TEXT NOT NULL,
    -- adjust_distribution | repeat_topic | try_format | shift_schedule
    -- | new_series | repurpose | explore_angle
  description TEXT NOT NULL,
  priority INTEGER DEFAULT 3, -- 1-5
  status TEXT NOT NULL DEFAULT 'pending', -- pending | accepted | dismissed
  accepted_at TIMESTAMPTZ,
  dismissed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now()
);
```

### 4.7 Campañas y calendario

```sql
-- Campañas
CREATE TABLE campaigns (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  brand_id UUID REFERENCES brands(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  description TEXT,
  offer_name TEXT, -- ej: "Operación 90"
  goal_type TEXT, -- awareness | leads | authority
  goal_metric TEXT, -- reach | profile_visits | link_clicks | engagement_rate
  goal_value INTEGER,
  start_date DATE,
  end_date DATE,
  track_distribution_json JSONB, -- {"credibilidad": 30, "cliente": 70}
  status TEXT NOT NULL DEFAULT 'planning',
    -- planning | active | completed | paused
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Relación campaña ↔ posts (many-to-many)
CREATE TABLE campaign_posts (
  campaign_id UUID REFERENCES campaigns(id) ON DELETE CASCADE,
  post_id UUID REFERENCES posts(id) ON DELETE CASCADE,
  PRIMARY KEY (campaign_id, post_id)
);

-- Calendario editorial
-- La hora se define directamente en el calendario (no en un paso separado de "programar").
-- Cuando el post se aprueba y está listo, posts.scheduled_at se sincroniza con este scheduled_at.
CREATE TABLE calendar (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  brand_id UUID REFERENCES brands(id) ON DELETE CASCADE,
  scheduled_at TIMESTAMPTZ NOT NULL, -- fecha + hora exacta, definida al planificar (hora libre)
  track_id UUID REFERENCES tracks(id),
  format TEXT,
  platforms TEXT[],
  idea_id UUID REFERENCES content_ideas(id),
  post_id UUID REFERENCES posts(id),
  campaign_id UUID REFERENCES campaigns(id),
  status TEXT NOT NULL DEFAULT 'empty',
    -- empty | planned | content_ready | scheduled | published
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE(brand_id, scheduled_at)
);

-- Reportes semanales (generados automáticamente)
CREATE TABLE weekly_reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  brand_id UUID REFERENCES brands(id) ON DELETE CASCADE,
  week_start DATE NOT NULL,
  week_end DATE NOT NULL,
  posts_planned INTEGER,
  posts_published INTEGER,
  track_distribution_actual JSONB, -- % real por carril
  total_reach INTEGER,
  total_impressions INTEGER,
  total_engagement INTEGER,
  avg_engagement_rate NUMERIC(5,4),
  top_post_id UUID REFERENCES posts(id),
  comparison_vs_previous JSONB, -- deltas vs semana anterior
  insights JSONB, -- observaciones generadas por AI
  generated_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE(brand_id, week_start)
);
```

### 4.8 Series de contenido

```sql
-- Series (agrupación de posts relacionados)
CREATE TABLE content_series (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  brand_id UUID REFERENCES brands(id) ON DELETE CASCADE,
  campaign_id UUID REFERENCES campaigns(id),
  name TEXT NOT NULL,
  description TEXT,
  total_parts INTEGER,
  track_id UUID REFERENCES tracks(id),
  topic_id UUID REFERENCES topics(id),
  frequency TEXT, -- daily | weekly | biweekly | custom
  status TEXT NOT NULL DEFAULT 'planning',
    -- planning | in_progress | completed | paused
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Posts dentro de una serie
CREATE TABLE series_posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  series_id UUID REFERENCES content_series(id) ON DELETE CASCADE,
  post_id UUID REFERENCES posts(id),
  idea_id UUID REFERENCES content_ideas(id),
  part_number INTEGER NOT NULL,
  subtitle TEXT,
  status TEXT DEFAULT 'pending', -- pending | draft | published
  UNIQUE(series_id, part_number)
);
```

### 4.9 Motor de ideas — Fuentes externas

```sql
-- Fuentes de ideas (RSS, influencers, competidores)
CREATE TABLE idea_sources (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
  type TEXT NOT NULL, -- rss | influencer | competitor
  name TEXT NOT NULL, -- ej: "TechCrunch AI", "@hormozi", "AI-Think"
  url TEXT, -- feed URL o perfil URL
  platform TEXT, -- web | linkedin | threads | instagram | youtube
  check_frequency TEXT DEFAULT 'daily', -- hourly | daily | weekly
  last_checked_at TIMESTAMPTZ,
  active BOOLEAN DEFAULT true,
  filter_prompt TEXT, -- prompt customizado para evaluar relevancia
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Items capturados de fuentes externas
CREATE TABLE source_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  source_id UUID REFERENCES idea_sources(id) ON DELETE CASCADE,
  title TEXT,
  url TEXT,
  content_preview TEXT, -- primeros 500 chars
  author TEXT,
  published_at TIMESTAMPTZ, -- fecha original
  evaluated BOOLEAN DEFAULT false,
  relevant BOOLEAN,
  idea_id UUID REFERENCES content_ideas(id), -- si generó idea
  evaluation_reasoning TEXT, -- por qué Claude dijo sí o no
  fetched_at TIMESTAMPTZ DEFAULT now()
);

-- Perfiles de influencers trackeados
CREATE TABLE influencer_profiles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  handle TEXT,
  platform TEXT NOT NULL,
  profile_url TEXT,
  why_follow TEXT, -- "IA práctica en español", "contenido de negocios directo"
  source_id UUID REFERENCES idea_sources(id), -- FK al tracking automático
  active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Competidores
CREATE TABLE competitors (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  brand_id UUID REFERENCES brands(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  website TEXT,
  linkedin_url TEXT,
  instagram_handle TEXT,
  threads_handle TEXT,
  notes TEXT, -- por qué es competidor, debilidad vs nosotros
  active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Posts de competidores capturados
CREATE TABLE competitor_posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  competitor_id UUID REFERENCES competitors(id) ON DELETE CASCADE,
  platform TEXT NOT NULL,
  external_url TEXT,
  content_preview TEXT,
  visible_reactions INTEGER,
  visible_comments INTEGER,
  topic_tags TEXT[], -- clasificados por Claude
  published_at TIMESTAMPTZ,
  fetched_at TIMESTAMPTZ DEFAULT now()
);
```

### 4.10 Repurposing

```sql
-- Sugerencias de repurposing
CREATE TABLE repurpose_suggestions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  source_post_id UUID REFERENCES posts(id) ON DELETE CASCADE,
  target_format TEXT NOT NULL,
  target_platform TEXT NOT NULL,
  rationale TEXT, -- por qué esta adaptación tiene sentido
  generated_idea_id UUID REFERENCES content_ideas(id),
  status TEXT NOT NULL DEFAULT 'suggested', -- suggested | accepted | dismissed
  created_at TIMESTAMPTZ DEFAULT now()
);
```

### 4.11 Métricas de perfil

```sql
-- Métricas de cuenta/perfil (followers, visitas) — no por post, sino por plataforma por día
-- Pull diario vía n8n. Necesarias para Dashboard (crecimiento de seguidores) y weekly report.
CREATE TABLE profile_metrics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  brand_id UUID REFERENCES brands(id) ON DELETE CASCADE,
  platform TEXT NOT NULL, -- linkedin | instagram | threads
  date DATE NOT NULL,
  followers INTEGER,
  profile_views INTEGER,
  search_appearances INTEGER, -- LinkedIn: búsquedas donde apareciste
  created_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE(brand_id, platform, date)
);
```

### 4.12 Assets y biblioteca

```sql
-- Biblioteca de assets reutilizables
CREATE TABLE assets (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
  brand_id UUID REFERENCES brands(id),
  type TEXT NOT NULL, -- image | video | pdf | template | logo | font
  name TEXT NOT NULL,
  description TEXT,
  tags TEXT[],
  file_url TEXT NOT NULL, -- Supabase Storage URL
  thumbnail_url TEXT,
  mime_type TEXT,
  file_size_bytes INTEGER,
  dimensions_json JSONB, -- { width, height } for images/videos
  usage_count INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT now()
);
```

### 4.13 Hashtags

```sql
-- Performance de hashtags
CREATE TABLE hashtag_performance (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  brand_id UUID REFERENCES brands(id) ON DELETE CASCADE,
  hashtag TEXT NOT NULL,
  platform TEXT NOT NULL,
  times_used INTEGER DEFAULT 0,
  avg_reach_when_used NUMERIC,
  avg_engagement_when_used NUMERIC,
  last_used_at TIMESTAMPTZ,
  trending BOOLEAN DEFAULT false,
  UNIQUE(brand_id, hashtag, platform)
);
```

### 4.14 Paid amplification (futuro)

```sql
-- Amplificación pagada
CREATE TABLE paid_amplifications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  post_id UUID REFERENCES posts(id) ON DELETE CASCADE,
  platform TEXT NOT NULL,
  ad_account_id TEXT,
  campaign_id_external TEXT,
  budget_usd NUMERIC(10,2),
  spend_usd NUMERIC(10,2),
  paid_impressions INTEGER,
  paid_reach INTEGER,
  paid_clicks INTEGER,
  cost_per_click NUMERIC(6,4),
  cost_per_engagement NUMERIC(6,4),
  start_date DATE,
  end_date DATE,
  status TEXT DEFAULT 'active', -- active | paused | completed
  created_at TIMESTAMPTZ DEFAULT now()
);
```

---

## 5. Flujo operacional

### 5.1 Ciclo mensual (cada 30 días)

```
Revisar estrategia en Vista Estrategia:
  → ¿La oferta cambió? Actualizar offer_doc
  → ¿El ICP cambió? Actualizar icp_doc
  → ¿Los carriles siguen con el peso correcto? Revisar benchmarks
  → ¿Hay subtemas agotados o nuevos? Activar/desactivar topics
  → ¿Hay competidores nuevos? Actualizar competitors
  → Marcar last_review_at, calcular next_review_at
```

### 5.2 Ciclo semanal

```
1. Revisar Dashboard
   → Métricas de la semana anterior
   → Recomendaciones pendientes del sistema
   → Distribución real vs target por carril

2. Revisar Pipeline → Vista Fuentes
   → ¿Qué ideas nuevas llegaron de RSS/influencers/AI?
   → Aprobar, descartar, o ajustar ideas

3. Planificar en Calendario
   → Asignar ideas a los días de la semana
   → El sistema valida distribución 70/30
   → Si hay serie activa, respetar su frecuencia

4. Generar contenido
   → Para cada día planificado: click "Generar"
   → El sistema carga brand context + carril + topic
   → Claude API genera la pieza
   → Preview por formato
   → Editar si hace falta
   → Aprobar → Programar fecha/hora
```

### 5.3 Ciclo diario

```
1. Abrir Calendario → ver el post del día
2. Si no está generado: Generar → Preview → Aprobar
3. Si está aprobado: Programar o Publicar ahora
4. El sistema publica vía API de la plataforma
5. Status cambia a "published" + se registra external_id
```

### 5.4 Ciclo automático (n8n)

```
Post publicado:
  → 24h: pull métricas → insert en metrics
  → 48h: pull métricas → insert en metrics
  → 7d: pull métricas final → insert en metrics
       → calcular content_score
       → actualizar performance_benchmarks
       → Si top 20%: generar repurpose_suggestions
       → Si top 10%: generar ideas derivadas (ai_suggested)
       → Si bottom 20%: generar recomendación de ajuste

Cada 6-12h (fuentes de ideas):
  → Fetch RSS feeds activos → evaluar con Claude → crear ideas si relevantes
  → Fetch posts de influencers → evaluar → crear ideas
  → Fetch posts de competidores → clasificar → almacenar

Domingo (semanal):
  → Agregar benchmarks de la semana
  → Claude API: generar ai_insights con datos de la semana
  → Compilar weekly_report
  → Enviar resumen por WhatsApp

Fin de mes:
  → Análisis mensual profundo
  → Comparar distribución real vs target
  → Identificar tendencias de 4+ semanas
  → Generar recomendaciones de ajuste estratégico
  → Alertar si next_review_at se acerca
```

---

## 6. Vistas del frontend

### 6.1 Dashboard

**Propósito:** Vista general del estado del marketing. Lo primero que ves al entrar.

**Contenido:**
- Cards con métricas de la semana: posts publicados, reach total, engagement rate promedio, nuevos seguidores
- Barra visual de distribución por carril (real vs target, ej: 68%/32% vs 70%/30%)
- Gráfico de tendencia de reach y engagement de las últimas 8 semanas (Recharts)
- Top 3 posts de la semana con thumbnail y métricas
- Recomendaciones activas del sistema (aceptar/descartar)
- Alerta si hay posts planificados sin contenido generado
- Comparación vs semana anterior (deltas con flechas ↑↓)

### 6.2 Calendario

**Propósito:** Planificación editorial visual.

**Contenido:**
- Vista mensual tipo grid. Cada celda = un día
- Dentro de cada celda: cards con formato (ícono), carril (color), plataforma(s), status (dot de color)
- Click en celda vacía → modal para asignar idea o crear nueva
- Click en celda con post → ver detalle, editar, programar, publicar
- Drag & drop para mover posts entre días
- Toggle vista semanal para más detalle
- Barra lateral con: distribución de la semana por carril, ideas sin asignar (para arrastrar al calendario), alertas de scheduling
- Validación visual: si la distribución se desvía del target, indicador de advertencia

### 6.3 Pipeline

**Propósito:** Gestión de ideas de contenido.

**Contenido:**
- Kanban con columnas: idea → planned → draft → ready → scheduled → published
- Cards con: título, formato (ícono), carril (color tag), plataforma(s), source (ícono), prioridad (dots)
- Filtros: por carril, formato, plataforma, source, prioridad
- Botón "Nueva idea" → formulario: título, descripción, carril, formato, plataformas, prioridad, link de inspiración
- Desde cada card: "Generar contenido" → abre Generador pre-cargado
- Badge de fuente: manual (user icon), RSS (feed icon), influencer (star), AI (sparkle), competencia (eye)
- Drag & drop entre columnas para cambiar status
- Vista alternativa: tabla/lista para bulk management

### 6.4 Generador

**Propósito:** Creación de contenido con IA y preview en tiempo real.

**Contenido:**
- Panel izquierdo: configuración
  - Seleccionar formato (carrusel IG, carrusel PDF, reel, thread, texto largo, caption)
  - Seleccionar carril y subtema
  - Indicador de performance histórico del subtema/formato seleccionado
  - Sugerencia de hook type basada en benchmarks
  - Campo de briefing adicional (instrucciones específicas para esta pieza)
  - Seleccionar assets de la biblioteca (imágenes, logo, etc.)
  - Botón "Generar"
- Panel derecho: preview (ver sección 7 para detalle por formato)
  - Edición inline del contenido generado
  - Reordenar slides (carrusel), editar texto, cambiar caption
  - Historial de versiones (dropdown con todas las versiones)
  - Botones de acción: "Guardar draft", "Aprobar", "Programar", "Publicar ahora"
- Barra inferior: generación en progreso (loading state), tokens usados

### 6.5 Reportes

**Propósito:** Análisis de performance y generación de insights.

**Contenido:**
- Selector de período: semana | mes | custom
- Weekly reports listados como cards expandibles
- Dentro de cada reporte:
  - Posts publicados con métricas individuales
  - Distribución por carril (real vs target)
  - Top post con detalle
  - Insights AI (observaciones y recomendaciones)
  - Comparación vs período anterior
- Vista mensual: tendencias de 4 semanas, evolución de benchmarks
- Botón "Exportar PDF" (para compartir con clientes en modelo gestionado)
- Gráficos: engagement rate por semana, reach por plataforma, performance por formato

### 6.6 Estrategia

**Propósito:** Definición y revisión de la marca, oferta, carriles y ICP.

**Contenido:**
- Tabs: Voz | Carriles & Subtemas | Oferta | ICP | Competencia
- **Voz:** Editor markdown del voice doc. Muestra última edición y quién la hizo.
- **Carriles & Subtemas:** Tabla editable. Cada carril con peso %, color, y subtemas anidados. Cada subtema con hooks y formatos recomendados. Activar/desactivar sin borrar.
- **Oferta:** Editor markdown de la oferta activa (Operación 90). Incluye pricing, tiers, garantía.
- **ICP:** Editor markdown del perfil de cliente ideal.
- **Competencia:** Lista de competidores con nombre, links, notas, últimos posts capturados.
- Indicador de "última revisión" y "próxima revisión" con countdown.
- Botón "Iniciar revisión mensual" que abre un wizard guiado.

### 6.7 Fuentes

**Propósito:** Configurar y monitorear fuentes de ideas.

**Contenido:**
- Tres tabs: RSS Feeds | Influencers | Competidores
- **RSS:** Lista de feeds con nombre, URL, frecuencia de check, status, last checked. CRUD completo. Botón "Agregar feed".
- **Influencers:** Perfiles trackeados con nombre, handle, plataforma, por qué lo sigues. Link a sus últimos posts capturados.
- **Competidores:** Tabla con perfil, links, últimos posts capturados y topic tags.
- **Inbox:** Lista de source_items pendientes de evaluación manual. Cada item con: título, preview, fuente, fecha, botones "Crear idea" / "Descartar". Filtrable por tipo de fuente.

### 6.8 Assets

**Propósito:** Biblioteca centralizada de recursos reutilizables.

**Contenido:**
- Grid de assets con thumbnail, nombre, tags, uso count
- Filtros: por tipo (imagen, video, PDF, template, logo), por tags, por brand
- Upload directo (drag & drop)
- Detalle de asset: preview a tamaño completo, metadata, posts donde se usó
- Tagging y búsqueda

### 6.9 Settings

**Propósito:** Configuración de la organización.

**Contenido:**
- **General:** Nombre de la org, slug, plan activo
- **Plataformas:** Estado de conexión de LinkedIn, Instagram, Threads. Botones de Connect/Disconnect. Muestra: cuenta conectada, token expiry, last used.
- **Equipo:** Miembros de la org con roles. Invitar nuevo miembro.
- **Notificaciones:** Configurar alertas WhatsApp (resumen semanal, alertas de performance, reminders de calendario).
- **Billing:** Plan actual, historial de pagos, upgrade/downgrade.

---

## 7. Sistema de preview por formato

Cada formato tiene un preview que simula cómo se verá en la plataforma real. El preview se muestra en el panel derecho del Generador y en el detalle de cada post.

### 7.1 Carrusel Instagram

- Frame que simula el ratio 1:1 o 4:5 de IG
- Navegación slide-by-slide con flechas izquierda/derecha
- Dots de posición debajo (como Instagram)
- Renderiza los HTML de cada slide dentro del frame
- Caption debajo con contador de caracteres (2.200 máx IG)
- Vista "grid" alternativa: todas las slides en miniatura para evaluar ritmo visual
- Edición inline: click en texto de una slide para editar directamente

### 7.2 Carrusel LinkedIn (PDF)

- Viewer de PDF embebido con navegación por página
- Caption de LinkedIn debajo con límite visible (3.000 chars)
- Marca visual del corte "ver más" (primeras ~3 líneas / ~210 chars del caption)
- Preview de cómo se ve el documento cerrado (primera página como thumbnail en el feed)

### 7.3 Post de texto LinkedIn

- Frame que simula un post de LinkedIn
- Foto de perfil + nombre + headline + timestamp
- Texto del post con marca del corte "ver más" (~210 chars)
- Texto completo debajo del corte
- Contador de caracteres
- Preview de la imagen adjunta si la hay

### 7.4 Thread (Threads)

- Simulación del formato Threads: secuencia vertical de posts
- Avatar + handle por post
- Separador entre posts del thread
- Contador de caracteres por post (500 máx Threads)
- Indicador de número de post (1/5, 2/5, etc.)
- Edición inline por post individual

### 7.5 Reel (guión / storyboard)

- Vista de storyboard: cada escena como card
- Campos por escena: texto del guión, duración estimada, notas de visual/B-roll, audio sugerido
- Timeline visual horizontal que muestra duración total del reel
- Cuando se integre HeyGen (fase 10): player de video real embebido
- Hasta entonces: preview es solo el guión visual

### 7.6 Caption con imagen

- Preview de la imagen a tamaño real (1:1 o 4:5)
- Caption debajo con contador
- Hashtags separados visualmente
- Preview de cómo se verá en el feed

---

## 8. Motor de inteligencia

### 8.1 Qué aprende

El sistema cruza las métricas de cada post con sus atributos (carril, subtema, formato, plataforma, día, hora, hook type, largo del contenido, CTA presente/ausente) para identificar patrones de performance.

**Performance por dimensión:**
- ¿Qué carril genera más reach? ¿Y más engagement?
- ¿Qué subtemas tienen mejor engagement rate dentro de cada carril?
- ¿Qué formato rinde mejor en cada plataforma?
- ¿Qué día/hora tiene mejor performance?
- ¿Qué tipo de hook genera más distribución?

**Tendencias temporales:**
- Engagement subiendo o bajando semana a semana
- Subtemas perdiendo o ganando tracción
- Formatos que consistentemente superan al resto

**Correlaciones:**
- Posts con CTA vs sin CTA — efecto en reach
- Largo del contenido vs engagement — sweet spot
- Frecuencia de publicación vs reach promedio por post

### 8.2 Dónde se materializa

**En el Calendario (al planificar):**
"Esta semana llevas 3 posts carril 1 y 1 carril 2. Tu target es 70/30. Los posts de carril 2 en formato carrusel tuvieron 2.3x más engagement que threads en las últimas 4 semanas."

**En el Generador (al crear):**
"Los últimos 5 posts de este subtema tuvieron engagement rate 4.2%. El hook tipo 'paradoja' rindió 6.1% vs 'verdad simple' 3.8% en este subtema." Pre-selecciona el hook con mejor performance.

**En el Reporte semanal (automático):**
Sección de insights: "El post sobre [tema] tuvo 3x el engagement promedio. Considerar serie de 3 posts." O: "Posts de miércoles a las 9am superan consistentemente a viernes. Considerar mover slot."

**En Recomendaciones (Dashboard):**
Cards accionables: "Ajustar distribución a 25/75 (actualmente 35/65)", "Repetir formato carrusel para subtema X", "El subtema Y lleva 3 semanas sin posts, considerar reactivar."

### 8.3 Cálculo de scores

Cuando llega la métrica de 7d de un post:
1. Calcular engagement_rate = (reactions + comments + reposts) / reach
2. Comparar contra todos los posts del brand → calcular percentile
3. Normalizar a score 0-100 para cada dimensión
4. Composite score = 0.4 * engagement + 0.3 * reach + 0.2 * virality + 0.1 * conversation
5. Actualizar performance_benchmarks para cada dimensión del post
6. Si trend cambió (4 semanas de datos), marcar improving/stable/declining

### 8.4 Triggers de recomendaciones

| Trigger | Recomendación generada |
|---------|----------------------|
| Post en percentil 90+ | "Explorar ángulos similares", generar 2-3 ideas derivadas |
| Post en percentil 20- | "Revisar subtema/formato, considerar pausar" |
| Distribución real desvía >10% del target | "Ajustar planificación para próxima semana" |
| Subtema sin posts en 3+ semanas | "Reactivar subtema X, última vez generó Y engagement" |
| Formato consistentemente top 3 semanas | "Aumentar frecuencia de este formato" |
| Benchmark en decline 4+ semanas | "El subtema X está perdiendo tracción, considerar rotación" |
| Post top performer | "Repurpose: adaptar a [formato] para [plataforma]" |

---

## 9. Motor de ideas

### 9.1 Fuentes

**Manual:** El usuario crea ideas directamente en el Pipeline. Formulario: título, descripción, carril, formato, plataformas, prioridad, link de inspiración.

**RSS / Noticias:** Feeds configurados en Vista Fuentes. n8n los consume periódicamente. Cada artículo nuevo se evalúa con Claude API:

```
Prompt de evaluación RSS:
"Dado este artículo y el brand context (voz, carriles, ICP):
- ¿Hay un ángulo de contenido relevante para la marca?
- Si sí: genera una idea con título, descripción, carril sugerido, formato, y hook.
- Si no: responde 'no relevante' con una razón breve."
```

**Influencers / Mentores:** Perfiles configurados en Vista Fuentes. n8n monitorea sus publicaciones vía APIs. Mismo flujo de evaluación con Claude, pero el prompt incluye: "¿Hay un ángulo que [brand] puede adaptar a su contexto? No copiar — adaptar con la voz propia."

**Competencia:** Similar a influencers pero con ángulo distinto. El prompt pregunta: "¿Este competidor está cubriendo un tema que [brand] no ha tocado? ¿Hay un gap de contenido que podemos llenar?"

**AI proactivo:** Cuando un post supera percentil 80, Claude genera 2-3 ideas derivadas automáticamente:

```
Prompt de ideas proactivas:
"Este post tuvo performance excepcional: [métricas].
Contenido: [resumen].
Carril: [track]. Subtema: [topic].
Genera 2-3 ideas de contenido derivadas que:
1. Exploren ángulos relacionados pero no cubiertos
2. Adapten el mismo tema a un formato diferente
3. No repitan ideas ya existentes en el pipeline: [lista de títulos]"
```

### 9.2 Flujo por fuente

**RSS:**
```
Cron (cada 6h)
→ fetch RSS feeds activos (idea_sources where type='rss' and active=true)
→ para cada item nuevo (no existe en source_items):
  → insert en source_items
  → enviar content_preview + brand context a Claude API
  → Si relevant=true:
    → DEDUPLICACIÓN: verificar content_ideas de los últimos 30 días del mismo brand
      → Si hay idea existente con título con >80% de overlap (similaridad semántica):
        → No crear idea nueva — agregar item.url como inspiration_url a la idea existente
      → Si no hay overlap: crear content_idea con status='idea', source='rss',
        relevance_score=<score de Claude>
      → Si relevance_score < brands.relevance_threshold: idea va a inbox de descarte
        (visible en Vista Fuentes, no en Pipeline principal). Usuario puede rescatarla.
  → Si relevant=false: marcar evaluated=true, relevant=false
```

**Influencers (LinkedIn):**
```
Cron (cada 12h)
→ para cada influencer con platform='linkedin':
  → LinkedIn API: fetch últimos posts del perfil
  → Para cada post nuevo no en source_items:
    → insert en source_items
    → evaluar con Claude
    → Si relevante: crear idea con inspiration_url
```

**Influencers (Threads):**
```
Cron (cada 12h)
→ Threads API: fetch posts de perfiles trackeados
→ Mismo flujo de evaluación
```

**Competencia:**
```
Cron (cada 24h)
→ Para cada competidor activo:
  → Fetch posts públicos recientes
  → Guardar en competitor_posts con topic_tags (clasificados por Claude)
  → Evaluar gaps: "¿Hay temas que cubren y nosotros no?"
  → Si hay gap: crear idea con source='competitor'
```

**AI proactivo:**
```
Trigger: content_score calculado con percentile > 80
→ Cargar post + brand context + últimas 10 ideas del mismo carril
→ Claude API: generar 2-3 ideas derivadas
→ Crear ideas con source='ai_suggested'
```

---

## 10. Integración de plataformas

Se conectan secuencialmente. El círculo completo (publicar → medir → aprender) se cierra para una plataforma antes de pasar a la siguiente.

### 10.1 LinkedIn (primera)

**API:** Community Management API (para perfiles personales). Marketing API si se agrega company page después.

**Autenticación:** OAuth 2.0. Scopes necesarios: `w_member_social` (publicar), `r_member_social` (leer posts propios), `r_organization_social` (si se agrega page).

**Publicación soportada:**
- Posts de texto (hasta 3.000 chars)
- Posts con imagen (upload → share)
- Posts con documento PDF (upload → share) — carruseles de LinkedIn
- Artículos (más largo, formato blog)

**Métricas disponibles vía API:**
- Impressions, clicks, likes, comments, shares a nivel de post
- Engagement rate calculable
- No provee: profile visits ni new followers por post (solo agregados)

**Limitaciones:**
- Rate limits: 100 API calls/día para UGC Posts (publicación)
- Refresh tokens: duran 365 días, se refrescan automáticamente
- La programación nativa de LinkedIn es limitada → scheduling vía n8n

**Cuenta principal:** Perfil personal de Oscar (primera línea). Company page de CreActive puede repostear (segunda línea, futuro).

### 10.2 Instagram (segunda)

**API:** Instagram Graph API vía Meta Business Suite.

**Prerequisitos:**
- Facebook Page de CreActive (crear si no existe)
- Cuenta de Instagram convertida a Business o Creator
- Ambas conectadas en Meta Business Suite
- App registrada en Meta Developers

**Autenticación:** OAuth 2.0 via Facebook Login. Token de larga duración (60 días, renovable).

**Publicación soportada:**
- Feed posts (imagen única)
- Carruseles (múltiples imágenes, hasta 10)
- Reels (video, hasta 90 segundos)
- Stories (imagen o video, 24h — prioridad baja)

**Métricas disponibles vía API:**
- Impressions, reach, likes, comments, saves, shares
- Profile visits (agregado, no por post)
- Video views (para reels)

**Limitaciones:**
- Las imágenes deben estar en una URL pública para publicar vía API (Supabase Storage resuelve esto)
- Rate limit: 200 calls/hour
- Reels requieren upload a container + publish (proceso de 2 pasos)

### 10.3 Threads (tercera)

**API:** Threads API (Meta, lanzada 2024).

**Autenticación:** Misma app de Meta Developers. Scope adicional: `threads_basic`, `threads_content_publish`, `threads_manage_insights`.

**Publicación soportada:**
- Posts de texto (hasta 500 chars)
- Posts con imagen
- Reply threads (múltiples posts encadenados) — creas el primero, luego replies al anterior

**Métricas disponibles vía API:**
- Views, likes, replies, reposts, quotes

**Limitaciones:**
- API relativamente nueva, funcionalidad más limitada
- No soporta scheduling nativo (igual que las otras → n8n)
- Rate limits más conservadores

### 10.4 Avatar IA (fase futura)

**API:** HeyGen (o alternativa como Higfield).

**Integración:** Se agrega como un "formato de generación" en el Generador. Flujo:
1. Generar guión con Claude API (skill cnt-reel-guion adaptado)
2. Enviar guión a HeyGen API con avatar de Oscar + voz clonada
3. Recibir video generado → almacenar en Storage
4. Preview de video en el Generador
5. Publicar como reel en IG o video en LinkedIn vía APIs existentes

La infraestructura de posts, scheduling y métricas ya está construida — solo se agrega el paso de generación de video.

---

## 11. Publicación y scheduling

### 11.1 Flujo de publicación

```
Post aprobado (publish_status = 'approved')
  → Usuario elige: "Publicar ahora" o "Programar"

Si "Publicar ahora":
  → Edge Function publish-post:
    → Lee platform_connections para obtener token
    → Sube assets a la plataforma si necesario (imágenes, PDF, video)
    → Crea el post via API nativa
    → Actualiza post: publish_status='published', external_id, external_url, published_at
    → Si falla: publish_status='failed', publish_error=razón
    → Trigger: programar pulls de métricas a 24h, 48h, 7d

Si "Programar":
  → Usuario selecciona fecha y hora en un datetime picker
  → Post: publish_status='scheduled', scheduled_at=fecha elegida
  → n8n scheduler-publish (cron cada 15 min):
    → Query: posts WHERE publish_status='scheduled' AND scheduled_at <= now()
    → Para cada uno: ejecutar el mismo flujo de "Publicar ahora"
```

### 11.2 Manejo de errores

**Retry automático:**
Si la publicación falla por error transitorio (rate limit, timeout de red):
```
publish_retry_count += 1
next_retry_at = now() + backoff[publish_retry_count]
  → intento 1: +15 min
  → intento 2: +30 min
  → intento 3: +60 min
Si publish_retry_count >= 3:
  → publish_status = 'failed'
  → notificar por WhatsApp: "⚠️ [Título] no se pudo publicar después de 3 intentos."
  → El usuario reintenta manualmente desde el detalle del post
```

**Errores específicos y cómo se manejan:**

- **Token expirado:**
  → `platform_connections.status = 'expired'`
  → Todos los posts `scheduled` de esa plataforma pasan a `publish_status = 'blocked'`
  → Notificación WhatsApp única: "⚠️ Tu conexión con [platform] expiró. Tienes X posts bloqueados."
  → Mostrar banner en todas las vistas: _"Tu conexión con [platform] expiró. [Reconectar]"_
  → El botón "Reconectar" inicia nuevo flujo OAuth sin perder historial ni configuración
  → Cuando la reconexión es exitosa: posts `blocked` vuelven a `scheduled` automáticamente
  → Cron de verificación preventiva (diario): alerta 7 días antes de expiración

- **Rate limit excedido:**
  → Retry automático con backoff (ver arriba). No notificar al usuario hasta fallo definitivo

- **Asset inválido (formato no soportado, tamaño excedido):**
  → No hay retry — es un error permanente
  → `publish_status = 'failed'`, `publish_error` con detalle
  → Notificación inmediata: el usuario debe corregir el asset y reintentar manualmente

- **Error parcial multi-plataforma:**
  → Cada post tiene su propio `publish_status` (ya están en filas separadas en la tabla `posts`)
  → Si LinkedIn publica e Instagram falla, el post de LinkedIn queda `published` y el de IG entra al flujo de retry
  → La idea permanece en `scheduled` hasta que todos sus posts terminen (published o failed)
  → Dashboard muestra íconos de estado por plataforma en cada celda del calendario: ✅ LinkedIn, ❌ Instagram

### 11.3 Publicación multi-plataforma

Una idea puede generar múltiples posts (uno por plataforma). Ejemplo: una idea de carrusel genera un post carrusel_ig para Instagram y un post carrusel_pdf para LinkedIn. Cada uno tiene su propio proceso de publicación, scheduling y métricas. Están vinculados por el mismo idea_id.

---

## 12. Multi-tenant y modelo SaaS

### 12.1 Principio fundamental

Cada cliente es una organización autónoma. Se auto-administra. Nosotros (CreActive) implementamos el sistema durante un período definido y luego el cliente opera solo con sus propias API keys, su propio contenido, su propia inteligencia acumulada.

Si un cliente quiere que lo gestionemos, es un retainer separado — no una feature del producto.

### 12.2 Aislamiento de datos

Row Level Security (RLS) de Supabase en todas las tablas. Cada query filtra por org_id del usuario autenticado. Un usuario solo ve datos de las organizaciones donde es miembro.

```sql
-- Ejemplo de policy RLS
CREATE POLICY "Users can only see their org's data" ON posts
  FOR ALL USING (
    brand_id IN (
      SELECT b.id FROM brands b
      JOIN organizations o ON b.org_id = o.id
      JOIN org_members om ON om.org_id = o.id
      WHERE om.user_id = auth.uid() AND om.status = 'active'
    )
  );
```

### 12.3 Proceso de implementación (onboarding de nuevo cliente)

```
1. Crear organización
   → Nombre, slug, plan seleccionado
   → Se crea el brand vacío asociado

2. Implementador (Oscar) configura:
   → Brand: voice doc, design system, ICP, oferta
   → Carriles y subtemas adaptados al cliente
   → Assets: logo, fotos, templates
   → Fuentes: RSS relevantes, influencers del nicho, competidores
   → Todo desde Vista Estrategia + Vista Fuentes

3. Conectar plataformas (con el cliente presente):
   → OAuth de LinkedIn/IG/Threads con las credenciales del cliente
   → Verificar que los tokens funcionan
   → Las API keys quedan en la org del cliente, no en la de Oscar

4. Seed del calendario:
   → Planificar primeras 2-4 semanas de contenido
   → Generar primeras piezas con el Generador
   → El cliente ve el flujo completo

5. Capacitación:
   → El cliente opera: crea ideas, genera, programa, revisa métricas
   → Oscar supervisa la primera semana

6. Handoff:
   → implementation_access del implementador expira automáticamente
   → El cliente opera solo
   → Si quiere soporte → retainer separado
```

### 12.4 Modelo de pricing SaaS

**ContentOps (la plataforma):**

| Plan | Incluye | Precio |
|------|---------|--------|
| Starter | 1 brand, 2 plataformas, calendario + pipeline + generador, métricas básicas, 50 generaciones Claude/mes | ~$30 USD/mes ($29.990 CLP) |
| Pro | 1 brand, 3 plataformas, inteligencia completa, fuentes de ideas, series, assets, reportes, generaciones ilimitadas | ~$60 USD/mes ($59.990 CLP) |
| Enterprise | Multi-brand, usuarios ilimitados, API access, white-label (futuro) | Custom |

**Servicios de CreActive (separados del SaaS):**

| Servicio | Incluye | Precio |
|----------|---------|--------|
| Setup ContentOps | Implementación completa: brand, carriles, plataformas, fuentes, calendario inicial, capacitación | $500-$1.500 USD (one-time) |
| Gestión mensual (opcional) | CreActive opera el ContentOps del cliente: genera, publica, reporta | $500-$1.000 USD/mes |

### 12.5 Tres líneas de revenue

1. **Operación 90 (consultoría)** — transformación operacional, $1.5K-$3K setup + retainer
2. **ContentOps setup (servicio)** — implementación del sistema, $500-$1.5K one-time
3. **ContentOps SaaS (producto)** — suscripción mensual recurrente, $30-$60/mes

La línea 3 es ingreso pasivo. 50 clientes activos × $60 = $3.000 USD/mes recurrentes sin esfuerzo operacional. Dentro de la meta de $5K-$10K/mes sumando las tres líneas.

---

## 13. Funcionalidades adicionales

### 13.1 Repurposing automático

Cuando un post supera percentil 70, el sistema sugiere adaptaciones para otros formatos/plataformas.

**Flujo con aprobación explícita:**
```
1. content_score calculado → percentile >= 70
   → Generar repurpose_suggestions (target_format, target_platform, rationale)
   → status = 'suggested'

2. Usuario ve las sugerencias en la card del post (vista Pipeline / Calendario)
   → Puede aceptar o descartar cada sugerencia individualmente

3. Si acepta:
   → Crear content_idea con:
       source = 'ai_repurpose'
       parent_post_id = <post original>
       primary_format = suggestion.target_format
       platforms = [suggestion.target_platform]
       title = "Repurposing: [título original] → [formato target]"
   → repurpose_suggestions.generated_idea_id = <nueva idea>
   → repurpose_suggestions.status = 'accepted'
   → La idea entra al Pipeline como cualquier otra (flujo normal)

4. Cuando el usuario genera contenido desde esa idea:
   → Claude API recibe: contenido original + brand context + formato target
   → Adapta sin copiar — contexto y ángulo son la fuente, no el texto literal
```

**Las sugerencias no crean posts directamente.** Siempre pasan por el flujo de aprobación del pipeline.

### 13.2 Series de contenido

Agrupación de posts con orden y narrativa. Ejemplo: "5 señales de que tu negocio depende de ti" — 5 carruseles que se publican con frecuencia definida.

Cuando creas una serie, el sistema planifica las partes en el calendario respetando la frecuencia. Si la parte 1 tiene buen engagement, indica señal positiva. Si la parte 2 cae, sugiere ajustar el ángulo de la parte 3.

### 13.3 Biblioteca de assets

Centraliza fotos, logos, screenshots, templates. Upload una vez, reutiliza en cualquier post. El Generador permite seleccionar assets de la biblioteca al crear contenido.

### 13.4 Monitoreo de competencia

Tracking automático de publicaciones de competidores. Clasificación por temas. Detección de gaps: "Tu competidor cubrió [tema] 3 veces esta semana. Tú no lo has tocado."

No para copiar — para detectar oportunidades.

### 13.5 Notificaciones WhatsApp

Mensajes vía WhatsApp Business API. Diseño: útiles, cortos, accionables.

**Alertas inmediatas (event-driven desde n8n):**

| Evento | Mensaje |
|--------|---------|
| Post publicado | `✅ "[Título]" publicado en LinkedIn` |
| Post fallido (3 intentos) | `⚠️ "[Título]" no se pudo publicar. Revisa ContentOps.` |
| Token próximo a expirar (7 días) | `⚠️ Tu conexión con LinkedIn expira en 7 días. Reconecta en Settings.` |
| Token expirado + posts bloqueados | `⚠️ Tu conexión con LinkedIn expiró. Tienes X posts bloqueados.` |
| Distribución desviada >20% del target | `📊 Esta semana: 85% carril técnico. Target: 30%. Planifica contenido de atracción.` |
| Posts planificados sin contenido | `📝 Tienes 3 posts planificados sin contenido generado para esta semana.` |
| Post top performer (percentil 90+) | `🚀 "[Título]" tiene 2.3x más reach que tu promedio. Considera repurposing.` |

**Resumen semanal (domingos 9:00 AM, generado por n8n):**
```
📅 Semana del DD/MM al DD/MM
Posts publicados: X
Top post: "[Título]" — X impresiones
Score promedio: X/100
Distribución: X% técnico / X% cliente
Recomendación: [insight de Claude en 1 oración]
```

**Modo bootstrap (< 20 posts con métricas):** Solo alertas inmediatas. Sin resumen semanal hasta tener datos suficientes.

### 13.6 Hashtag intelligence

Tracking de hashtags usados, correlación con performance, sugerencias automáticas por post. Detección de hashtags trending relevantes al brand.

### 13.7 Paid amplification (futuro)

Integración con Meta Ads API para boost de posts orgánicos top performers. Tracking de spend y ROI. Comparación orgánico vs paid.

---

## 14. Roadmap de construcción

| Fase | Nombre | Qué incluye | Resultado |
|------|--------|-------------|-----------|
| **0** | Foundation | Schema Supabase completo (todas las tablas incluyendo `profile_metrics`) + migrations + seed data (CreActive brand, carriles, topics migrados de .md). Next.js scaffold con auth y layout. Deploy ops.creactivestudio.agency en Vercel. **Prerequisito:** crear app en LinkedIn Developer Portal (no esperar a Fase 2). | Infraestructura lista, app accesible |
| **1** | Core Loop | Vistas: Estrategia + Pipeline (kanban) + Calendario + Generador con preview. **Preview Fase 1: solo `texto_largo` y `carrusel_ig`** — los demás formatos se agregan en fases posteriores. CRUD completo. Generación vía Claude API (con prompt caching para brand context). Asset library. Versioning de posts. Ideas manuales. | Planificas, generas, previsualizas y organizas contenido |
| **2** | LinkedIn e2e | OAuth perfil personal. Publicación directa (texto, imagen, PDF). Scheduling vía n8n. Retry automático con backoff (max 3 intentos). Estado `blocked` para posts con token expirado. Pull de métricas automático (24h, 48h, 7d) + pull diario de `profile_metrics`. Cron diario de verificación de tokens (alerta 7 días antes). Content scores + benchmarks. Dashboard con datos reales. | Círculo completo para LinkedIn |
| **3** | Inteligencia v1 | Cálculo automático de scores y benchmarks. **Lógica de bootstrap:** si < 20 posts con métricas de 7d, modo reducido sin comparativas. Pesos del composite score configurables por brand (`score_weights`). Insights semanales con Claude API. Recomendaciones en calendario/generador. Weekly report automático + resumen WhatsApp. Repurposing suggestions con flujo de aprobación. | El sistema aprende y sugiere |
| **4** | Motor de ideas | RSS feeds configurables. Tracking de influencers (LinkedIn primero). Evaluación automática con Claude + `relevance_score` + deduplicación. **Condición:** evaluación automática activa solo cuando hay 20+ posts publicados; antes, items van al inbox para revisión manual. Ideas AI proactivas por performance. Vista Fuentes con inbox de descarte. Monitoreo de competencia. | Pipeline siempre alimentado |
| **5** | Instagram e2e | Preview `carrusel_ig` ya implementado en Fase 1. Agregar preview `reel`. Setup Meta Business (Facebook Page + IG Business). Publicación carruseles + reels. Métricas. Benchmarks cross-platform. | Dos plataformas operativas |
| **6** | Threads e2e | Preview `thread`. Conexión Threads API. Publicación de threads y posts. Métricas. Tracking de influencers en Threads. | Tres plataformas, sistema completo |
| **7** | Series + Hashtags | Content series con planificación automática en calendario. Hashtag intelligence y sugerencias. Preview `caption`. | Contenido más estratégico |
| **8** | Multi-tenant | RLS por org. Signup flow. Onboarding wizard. Implementation access temporal con permisos definidos por role. Plans + billing con Mercado Pago (cobro manual hasta esta fase). Rate limiting de Claude API por plan. Configuración de `approval_fallback_mode`. Offboarding (cancelled_at, data deletion). Landing pública de ContentOps. | SaaS vendible |
| **9** | Paid integration | Meta Ads API. Boost desde dashboard. Tracking spend/ROI. Comparación orgánico vs paid. | Marketing completo |
| **10** | Avatar IA | HeyGen API. Generación de video desde guión. Preview de video en Generador. Publicación como reel/video. | Video automatizado |

**Nota sobre preview por formato:** Los 6 formatos se distribuyen así: Fase 1 (texto_largo + carrusel_ig), Fase 5 (+reel), Fase 6 (+thread), Fase 7 (+caption). `carrusel_pdf` y `imagen` son simplificados — se implementan junto al formato de plataforma correspondiente.

**Nota sobre billing manual (Fases 0-7):** Los primeros clientes que usen ContentOps como servicio se cobran con link de Mercado Pago + seguimiento en spreadsheet. El billing automático de Fase 8 solo automatiza lo que ya se cobra manualmente.

---

## 15. Estructura del proyecto

```
Proyectos Internos/contentops/
├── CLAUDE.md                        ← Contexto del proyecto para Claude Code
├── PRD.md                           ← Este documento
│
├── app/                             ← Next.js frontend
│   ├── src/
│   │   ├── app/                     ← App Router (Next.js 14+)
│   │   │   ├── (auth)/              ← Layout de autenticación
│   │   │   │   ├── login/
│   │   │   │   └── signup/
│   │   │   ├── (dashboard)/         ← Layout principal (sidebar + topbar)
│   │   │   │   ├── dashboard/       ← Vista Dashboard
│   │   │   │   ├── calendar/        ← Vista Calendario
│   │   │   │   ├── pipeline/        ← Vista Pipeline (kanban)
│   │   │   │   ├── generator/       ← Vista Generador + Preview
│   │   │   │   ├── reports/         ← Vista Reportes
│   │   │   │   ├── strategy/        ← Vista Estrategia
│   │   │   │   ├── sources/         ← Vista Fuentes (RSS, influencers, competencia)
│   │   │   │   ├── assets/          ← Vista Assets / Biblioteca
│   │   │   │   └── settings/        ← Vista Settings
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx             ← Redirect a /dashboard
│   │   │
│   │   ├── components/
│   │   │   ├── ui/                  ← shadcn/ui base components
│   │   │   ├── layout/              ← Sidebar, Topbar, Breadcrumbs
│   │   │   ├── calendar/            ← CalendarGrid, DayCell, PostCard
│   │   │   ├── pipeline/            ← KanbanBoard, IdeaCard, IdeaForm
│   │   │   ├── generator/           ← GeneratorPanel, FormatSelector
│   │   │   ├── preview/             ← PreviewFrame, CarouselPreview,
│   │   │   │                           LinkedInPreview, ThreadsPreview,
│   │   │   │                           ReelStoryboard, CaptionPreview
│   │   │   ├── metrics/             ← ScoreCard, TrendChart, BenchmarkBar
│   │   │   ├── strategy/            ← VoiceEditor, TrackManager, TopicList
│   │   │   ├── sources/             ← SourceList, InboxItem, FeedConfig
│   │   │   └── shared/              ← StatusBadge, TrackTag, FormatIcon
│   │   │
│   │   ├── lib/
│   │   │   ├── supabase/
│   │   │   │   ├── client.ts        ← Browser client
│   │   │   │   ├── server.ts        ← Server client
│   │   │   │   └── middleware.ts     ← Auth middleware
│   │   │   ├── api/                 ← Funciones por dominio
│   │   │   │   ├── brands.ts
│   │   │   │   ├── tracks.ts
│   │   │   │   ├── ideas.ts
│   │   │   │   ├── posts.ts
│   │   │   │   ├── calendar.ts
│   │   │   │   ├── metrics.ts
│   │   │   │   ├── sources.ts
│   │   │   │   ├── assets.ts
│   │   │   │   └── campaigns.ts
│   │   │   ├── ai/
│   │   │   │   ├── generate.ts      ← Llamadas a Claude API para generar contenido
│   │   │   │   ├── evaluate.ts      ← Evaluación de ideas de fuentes externas
│   │   │   │   └── insights.ts      ← Generación de insights y recomendaciones
│   │   │   └── utils/
│   │   │       ├── formats.ts       ← Helpers por formato de contenido
│   │   │       ├── scoring.ts       ← Cálculos de scores y benchmarks
│   │   │       └── constants.ts
│   │   │
│   │   ├── hooks/                   ← Custom React hooks
│   │   │   ├── use-brand.ts
│   │   │   ├── use-calendar.ts
│   │   │   ├── use-pipeline.ts
│   │   │   ├── use-metrics.ts
│   │   │   └── use-realtime.ts      ← Supabase Realtime subscriptions
│   │   │
│   │   └── types/                   ← TypeScript types
│   │       ├── database.ts          ← Auto-generated from Supabase
│   │       ├── content.ts           ← Content-specific types
│   │       └── api.ts               ← API response types
│   │
│   ├── public/
│   │   └── preview-frames/          ← Assets para simular feeds (mockup frames)
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.ts
│   └── tsconfig.json
│
├── supabase/                        ← Database + Edge Functions
│   ├── migrations/
│   │   ├── 001_organizations.sql
│   │   ├── 002_brands_strategy.sql
│   │   ├── 003_platform_connections.sql
│   │   ├── 004_content_ideas.sql
│   │   ├── 005_posts.sql
│   │   ├── 006_metrics.sql
│   │   ├── 007_campaigns_calendar.sql
│   │   ├── 008_series.sql
│   │   ├── 009_idea_sources.sql
│   │   ├── 010_repurpose.sql
│   │   ├── 011_assets.sql
│   │   ├── 012_hashtags.sql
│   │   ├── 013_paid.sql
│   │   └── 014_rls_policies.sql
│   ├── functions/
│   │   ├── generate-content/        ← Claude API: genera contenido con brand context
│   │   ├── evaluate-idea/           ← Claude API: evalúa si un source_item es relevante
│   │   ├── publish-post/            ← Proxy a LinkedIn/IG/Threads APIs
│   │   ├── calculate-scores/        ← Calcula content_scores y benchmarks
│   │   ├── generate-insights/       ← Claude API: genera weekly insights
│   │   └── generate-report/         ← Compila weekly_report
│   ├── seed.sql                     ← Data inicial: CreActive org, brand, tracks, topics
│   └── config.toml
│
├── n8n/                             ← Workflows exportados (JSON)
│   ├── scheduler-publish.json       ← Cron cada 15min: publica posts programados
│   ├── fetch-metrics-linkedin.json  ← Pull métricas LinkedIn a 24h/48h/7d
│   ├── fetch-metrics-instagram.json
│   ├── fetch-metrics-threads.json
│   ├── fetch-rss-feeds.json         ← Cron cada 6h: consume RSS + evalúa con Claude
│   ├── fetch-influencers.json       ← Cron cada 12h: monitorea influencers
│   ├── fetch-competitors.json       ← Cron cada 24h: monitorea competencia
│   ├── calculate-scores.json        ← Trigger: después de métricas 7d → calcular scores
│   ├── weekly-report.json           ← Cron domingos: compilar reporte + insights
│   ├── monthly-review-alert.json    ← Cron: alertar cuando toca revisión mensual
│   ├── whatsapp-notifications.json  ← Envío de alertas por WhatsApp
│   └── token-refresh.json           ← Cron diario: refrescar tokens que expiran pronto
│
├── content-engine/                  ← Migración del sistema actual
│   ├── migration-script.ts          ← Lee .md/.json actuales y los sube a Supabase
│   └── brand-seed/                  ← Archivos actuales como referencia
│       ├── voz.md
│       ├── pilares.md
│       ├── hormozi-patterns.md
│       └── design-system.md
│
└── docs/
    ├── api-setup-linkedin.md        ← Guía paso a paso para obtener API access
    ├── api-setup-instagram.md
    ├── api-setup-threads.md
    ├── onboarding-checklist.md      ← Checklist de implementación para nuevos clientes
    └── deployment.md                ← Instrucciones de deploy (Vercel + Supabase + n8n)
```

---

## 16. Setup previo de plataformas

Pasos que deben completarse antes o en paralelo a la construcción de cada fase.

### 16.1 LinkedIn (iniciar en Fase 0, no esperar Fase 2)

> **⚠️ Hacer en el primer día de Fase 0.** La aprobación de Community Management API puede tomar semanas y es prerequisito duro para Fase 2. Si se inicia tarde, bloquea todo el roadmap.

1. Crear app en LinkedIn Developer Portal (developer.linkedin.com)
2. Solicitar acceso a Community Management API (para perfil personal)
3. Configurar OAuth redirect URL (ops.creactivestudio.agency/api/auth/callback/linkedin)
4. Obtener Client ID y Client Secret
5. Verificar scopes: `w_member_social`, `r_member_social`
6. Documentar el proceso y estado de aprobación en `docs/api-setup-linkedin.md`

**Segunda línea (futuro):** Company page de CreActive Studio en LinkedIn. Puede repostear el contenido del perfil personal. Requiere scope r_organization_social.

### 16.2 Instagram + Facebook (antes de Fase 5)

1. Crear Facebook Page de CreActive (si no existe)
2. Convertir cuenta de Instagram a Business o Creator
3. Conectar IG a la Facebook Page en Meta Business Suite
4. Registrar app en Meta Developers (developers.facebook.com)
5. Agregar producto: Instagram Graph API
6. Configurar OAuth redirect URL
7. Solicitar permisos: instagram_basic, instagram_content_publish, instagram_manage_insights, pages_show_list

**Nota:** Proceso más largo que LinkedIn. Hacer en paralelo con Fases 2-4.

### 16.3 Threads (antes de Fase 6)

1. En la misma app de Meta Developers, habilitar Threads API
2. Solicitar scopes: threads_basic, threads_content_publish, threads_manage_insights
3. La cuenta de Threads ya está vinculada a Instagram

### 16.4 Dominio

1. Crear registro DNS para ops.creactivestudio.agency
2. Tipo: CNAME apuntando a cname.vercel-dns.com
3. Configurar dominio custom en Vercel project

### 16.5 Supabase

1. Crear proyecto en Supabase (región: South America si disponible, o US East)
2. Habilitar Auth con email/password
3. Configurar Supabase Vault para encriptar tokens de APIs
4. Configurar Storage buckets: assets, generated-content

### 16.6 n8n

1. Verificar que n8n self-hosted está accesible
2. Configurar credenciales de Supabase en n8n
3. Configurar credencial de Claude API (Anthropic) en n8n
4. Importar workflows base conforme se construyen

---

## 17. Migración del content engine actual

El content engine existente (`content-engine/`) tiene datos valiosos que deben migrarse a Supabase.

### 17.1 Mapeo de archivos a tablas

| Archivo actual | Tabla destino | Notas |
|---|---|---|
| `brand/voz.md` | `brands.voice_doc` | Copiar como markdown |
| `brand/pilares.md` | `tracks` + `topics` | Parsear: cada pilar → un track. Subtemas → topics. Hooks → topics.hooks[] |
| `brand/hormozi-patterns.md` | `brands.design_system_json` o documento adjunto | Referencia estática, no cambia seguido |
| `brand/design-system.md` | `brands.design_system_json` | Parsear a JSON |
| `carrusel/ideas/*.json` | `content_ideas` | Cada JSON → una idea con format='carrusel_ig' |
| `carrusel/variedad.md` | Eliminada — lógica de rotación calculada dinámicamente | Query últimos 5 posts del brand |
| `carrusel/output/` | Supabase Storage | Assets generados |
| `threads/semana-*.md` | `content_ideas` o `posts` según status | |
| Handoff Operación 90 | `brands` (offer_doc, icp_doc, competitors_doc) + `campaigns` | Descomponer en campos |

### 17.2 Mapeo de pilares a carriles y subtemas

**Carril 1 — Credibilidad técnica (30%):**
- Subtema: "Lo que estoy construyendo" (ex Pilar 4 parcial + nuevo)
- Subtema: "Stack y herramientas" (ex Pilar 4)
- Subtema: "IA práctica — cómo funciona" (ex Pilar 2 parcial)
- Subtema: "Reflexiones técnicas honestas" (nuevo)

**Carril 2 — Atracción de cliente (70%):**
- Subtema: "Sistemas que trabajan solos" (ex Pilar 1)
- Subtema: "IA para tu negocio" (ex Pilar 2 parcial, ángulo cliente)
- Subtema: "Ejecutar > planear" (ex Pilar 3)
- Subtema: "Casos y resultados reales" (ex Pilar 5)
- Subtema: "Síntomas del negocio atrapado" (nuevo, derivado del ICP)
- Subtema: "Operación 90 — qué es y cómo funciona" (nuevo)

### 17.3 Script de migración

`content-engine/migration-script.ts` — Script que:
1. Lee cada archivo .md y .json del content engine actual
2. Parsea la estructura
3. Inserta en las tablas correspondientes de Supabase
4. Sube assets al Storage
5. Genera seed.sql como backup

---

## 18. Decisiones de diseño

Registro de todas las decisiones tomadas durante la planificación.

| # | Decisión | Justificación |
|---|----------|---------------|
| 1 | Proyecto nuevo en `Proyectos Internos/`, no extensión del content engine | Tiene DB, frontend, y vida propia. El content engine es legacy que se migra. |
| 2 | Nombre: ContentOps | Descriptivo, profesional, domain-available friendly. |
| 3 | Deploy: Vercel + ops.creactivestudio.agency | Mismo patrón que todos los proyectos. Subdominio de la agencia. |
| 4 | Plataformas en orden: LinkedIn → Instagram → Threads | LinkedIn es la principal para Operación 90. IG para alcance. Threads para conversación. |
| 5 | Círculo completo por plataforma antes de pasar a la siguiente | Evita tener 3 integraciones a medias. Mejor una funcionando al 100%. |
| 6 | Pilares se convierten en subtemas dentro de carriles | Simplifica: carril define audiencia, subtema define tema. Alineado con estrategia de dos carriles. |
| 7 | Multi-tenant: cada cliente se auto-administra | CreActive implementa, cliente opera. Elimina cuello de botella. Escala sin headcount. |
| 8 | API keys del cliente, no de CreActive | Seguridad y autonomía. Cada org es dueña de sus datos y conexiones. |
| 9 | Inteligencia por org, no compartida | Lo que funciona para un nicho no funciona para otro. Cada brand aprende por separado. |
| 10 | Preview por formato simulando plataforma real | No se puede aprobar contenido sin verlo como quedará. Reduce ciclos de revisión. |
| 11 | Versioning de posts | Permite iterar sin perder historial. Necesario para aprobación colaborativa. |
| 12 | Métricas con múltiples snapshots (24h, 48h, 7d) | La curva de performance es más valiosa que un solo número. |
| 13 | RSS + influencers + competencia + AI proactivo como fuentes de ideas | El pipeline no puede depender solo de ideas manuales. Necesita alimentación constante. |
| 14 | Publicación/scheduling desde ContentOps | Cierra el círculo. Sin esto, hay que copiar/pegar a cada plataforma — mata la eficiencia. |
| 15 | Carruseles LinkedIn en PDF, Instagram en imágenes | Cada plataforma tiene su formato nativo. No adaptar es perder engagement. |
| 16 | n8n para automatizaciones, no cron jobs custom | Oscar ya lo domina. Visual. Debuggeable. Portable a clientes. |
| 17 | Gestión de clientes como retainer separado, no feature del SaaS | Evita complejidad de permisos/roles innecesarios en el producto. El SaaS es self-service. |
| 18 | Avatar IA como última fase del roadmap | Requiere todas las fases anteriores funcionando. Es una adición al generador, no un sistema aparte. |
| 19 | Mercado Pago como gateway primario, no Stripe | ICP es LATAM. Mercado Pago es el estándar. Experiencia acumulada con Nutrisco. Stripe solo si se valida demanda internacional. |
| 20 | Billing no se implementa hasta Fase 8 | Las fases 0-7 son para uso interno (CreActive). No necesitan cobro. El billing se agrega cuando el producto está validado y listo para vender. |
| 21 | Starter base: Supabase + Next.js Auth (Vercel template) | Arranca con auth + DB configurados. Sin Stripe incluido — evita remover código innecesario. Billing se integra limpio en Fase 8. |
| 22 | Prompt caching de Anthropic para brand context en `generate-content` | El brand context (voz + ICP + oferta + competidores) no cambia entre generaciones del mismo brand. Sin caching, cada call paga el context completo. Con caching se reduce el costo ~60%. El cache se invalida automáticamente cuando `brands.updated_at` cambia. |

---

## Apéndice A — Influencers y referentes iniciales

Cuentas a configurar como fuentes de ideas para el brand de Oscar:

| Nombre | Handle | Plataforma | Ángulo |
|--------|--------|-----------|--------|
| Alex Hormozi | @hormozi | Threads, LinkedIn | Negocios, scaling, pricing |
| Agustín Badt | @agustinbadt | Instagram | Negocios, directo, sin exceso |
| Zayn Pike | @zaynpike | Instagram | Lifestyle + negocios |
| Francisco Doglio | @franciscodoglio | Instagram | Agencia/marketing LatAm |
| Bastian Xu | @bastian.xu | Instagram | Tech/AI en español |
| Santi Ferretti | @santiiferretti | Instagram | Negocios/mindset |
| Jordi GPT | @jordigpt | Instagram | IA práctica en español |

---

## Apéndice B — Clientes actuales (casos para contenido)

| Cliente | Contrato | Implementación | Resultado |
|---------|----------|---------------|-----------|
| Pumpalcerro | $97k CLP/mes | Web + CRM GHL + Meta Ads | En curso |
| Rivas Legal | $70k CLP/mes | Landing + chat automatizado | Primer lead en 48h |
| Constanza Nutrición | 30% revenue share | Landing + webapp + Meta Ads + IA | En curso |
| PH Labs | $500 USD + $97k CLP/mes | Sub-cuenta GHL, pipeline, calendarios | En construcción |

---

## Apéndice C — Cadencia sugerida inicial

| Día | Formato | Carril | Plataforma |
|-----|---------|--------|-----------|
| Lunes | Carrusel | 1 (técnico) | LinkedIn + Instagram |
| Martes | Thread / reflexión | 2 (cliente) | Threads + LinkedIn |
| Miércoles | Reel o texto | 2 (cliente) | Instagram + LinkedIn |
| Jueves | Carrusel | 2 (cliente) | LinkedIn + Instagram |
| Viernes | Caso / resultado | 2 (cliente) | LinkedIn + Instagram |
| Sábado | Thread | Cualquiera | Threads |
| Domingo | Descanso o reflexión ligera | — | — |

**Distribución resultante:** ~29% carril 1, ~71% carril 2. Dentro del target 30/70.

---

*Documento generado como spec de producto. Toda la información proviene de sesiones de planificación con Oscar Vergara Barros, abril 2026.*
*Próximo paso: construir Fase 0 (Foundation).*
