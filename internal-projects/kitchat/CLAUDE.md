# White-Cassini — CLAUDE.md

> Sistema multi-tenant de menú digital y gestión de pedidos para restaurantes.
> Estado: En producción. Customer app con home de categorías + menú scroll anclado en feature/customer-redesign (2026-04-13).

---

## 1. Arquitectura general

```
┌──────────────────────────────┐     ┌──────────────────────────────┐
│   Customer App               │     │   Admin Panel (React)        │
│   customer-app/              │     │   admin-react/               │
│   Preact 10 + Vite + TS      │     │   React 19 + Vite + Tailwind │
│   Preact Signals + PWA       │     │   + Supabase + dnd-kit       │
│   Deploy: Vercel             │     │   Deploy: Vercel             │
└──────────────┬───────────────┘     └──────────────┬───────────────┘
               │                                    │
               │  ?local=slug [&mesa=N]             │  useAuth → restaurante_id
               │                                    │
               ▼                                    ▼
┌──────────────────────────────────────────────────────────────────┐
│                         Supabase                                  │
│  ┌─────────────┐  ┌───────────┐  ┌────────────────────────────┐ │
│  │ PostgreSQL   │  │ Realtime  │  │ Edge Functions (8)         │ │
│  │ (RLS)       │  │ pedidos   │  │ kapso-setup                │ │
│  │ Auth        │  │ productos │  │ kapso-webhook              │ │
│  │ Storage     │  │ restauran │  │ kapso-send                 │ │
│  │ RPC (4)     │  │           │  │ kapso-conversations        │ │
│  └─────────────┘  └───────────┘  │ kapso-messages             │ │
│                                   │ kapso-feedback-scheduler   │ │
│                                   │ kapso-review-flusher       │ │
│                                   │ review-classifier          │ │
│                                   └──────────────┬─────────────┘ │
└──────────────────────────────────────────────────┼───────────────┘
                                                   │
                                                   ▼
                                        ┌────────────────────┐
                                        │   Kapso Platform   │
                                        │   WhatsApp Business│
                                        │   API              │
                                        └────────────────────┘
```

**Flujo de un pedido:**
1. Cliente abre `?local=slug` (o `?local=slug&mesa=N`) → hooks cargan menú desde Supabase
2. Cliente arma carrito → CheckoutModal llama RPC `submit_order_v1`
3. Pedido se inserta en `pedidos` + `pedido_items`
4. Cliente confirma por WhatsApp (`wa.me/`) → FloatingOrderButton activa polling de estado
5. Admin recibe pedido vía Supabase Realtime → chime de audio en loop
6. Admin cambia estado en Kanban → Edge Function `kapso-send` notifica al cliente por WhatsApp

---

## 2. Estructura de archivos

```
white-cassini/
├── CLAUDE.md                          ← este archivo
│
├── customer-app/                      ← Customer app (Preact + Vite + TypeScript)
│   ├── index.html                     ← lang="es", Google Fonts Inter, Material Symbols
│   ├── vite.config.ts                 ← preact() + VitePWA + alias @/
│   ├── tsconfig.app.json              ← paths: "@/*" → "./src/*"
│   ├── .env.local                     ← VITE_SUPABASE_URL + VITE_SUPABASE_ANON_KEY (no commiteado)
│   └── src/
│       ├── app.tsx                    ← Root: hooks, slug guard, skeleton, overlays
│       ├── main.tsx                   ← render(<App />)
│       ├── components/
│       │   ├── Navbar.tsx             ← Logo, status badge, search trigger, cart badge + back-to-home (en vista menú)
│       │   ├── HeroSection.tsx        ← Hero bg, nombre, chips pickup_time + delivery_time
│       │   ├── HomeView.tsx           ← Vista home: HeroSection + QuickReorder + grid de CategoryHomeCards
│       │   ├── CategoryHomeCard.tsx   ← Card de categoría: imagen del primer producto, nombre, count
│       │   ├── MenuView.tsx           ← Vista menú: CategoryTabsSticky + secciones por categoría (scroll anclado al montar)
│       │   ├── CategoryTabsSticky.tsx ← Tab bar sticky con IntersectionObserver (highlight automático) + botón tres puntos
│       │   ├── CategoryNavSheet.tsx   ← Bottom sheet de navegación rápida entre categorías
│       │   ├── CategoryTabs.tsx       ← [DEPRECADO en MenuView] Tabs originales — sin usar en la vista principal
│       │   ├── ProductGrid.tsx        ← Grid de productos. Prop categoryId?: filtra esa cat; sin ella usa currentCategory signal
│       │   ├── ProductCard.tsx        ← Card con overlay Agotado, lazy image
│       │   ├── ProductModal.tsx       ← Bottom sheet: variantes, extras, qty, notas
│       │   ├── CartBadge.tsx          ← Badge flotante sobre cart icon
│       │   ├── CartSidebar.tsx        ← Panel lateral: items, qty, min order, checkout CTA
│       │   ├── CheckoutModal.tsx      ← Bottom sheet: CustomerForm + zonas + resumen + total + WA submit
│       │   ├── CustomerForm.tsx       ← Delivery/Retiro (con tiempo estimado), nombre, teléfono, dirección, pago
│       │   ├── OrderSuccess.tsx       ← Overlay post-pedido con link WA
│       │   ├── FloatingOrderButton.tsx← Botón flotante que activa OrderTracker
│       │   ├── OrderTracker.tsx       ← Timeline de 4 estados con polling
│       │   ├── SearchBar.tsx          ← Modal buscador client-side
│       │   ├── QuickReorder.tsx       ← Chip "Tu pedido anterior" en hero
│       │   ├── ClosedBanner.tsx       ← Banner "Abre en X horas" cuando tienda cerrada
│       │   ├── OfflineBanner.tsx      ← Banner de sin conexión (PWA)
│       │   └── Toast.tsx              ← Notificaciones flotantes
│       ├── hooks/
│       │   ├── useStore.ts            ← Carga datos + Realtime productos/restaurante + zonas_delivery
│       │   ├── useBranding.ts         ← Aplica CSS vars de config_marca via effect()
│       │   ├── useStoreStatus.ts      ← Abierto/cerrado con interval 60s
│       │   ├── useOrderTracking.ts    ← Polling RPC get_order_status cada 10s
│       │   └── useCustomerMemory.ts   ← Lee nombre/teléfono guardados en localStorage
│       ├── signals/
│       │   ├── store.ts               ← restaurant, menuData, storeStatus, isLoading, minOrderAmount, deliveryZones
│       │   ├── cart.ts                ← cart, cartTotal, cartCount + auto-persist localStorage
│       │   ├── order.ts               ← activeOrderId, orderStatus, orderNumber
│       │   ├── mesa.ts                ← mesaNumber (lee ?mesa= de URL)
│       │   └── ui.ts                  ← toastMessage, toastType, orderSuccessData + currentView ('home'|'menu') + pendingScrollCategoryId + isCategoryNavOpen
│       ├── lib/
│       │   ├── database.types.ts      ← Tipos manuales (8 tablas + 4 RPCs)
│       │   ├── supabase.ts            ← createClient<Database>
│       │   ├── utils.ts               ← formatPrice, buildWhatsAppUrl, normalizeChileanPhone, etc.
│       │   └── storage.ts             ← getItem/setItem + customer memory keys
│       └── styles/
│           ├── tokens.css             ← :root CSS vars (colores, radii, sombras, --navbar-height, --tab-bar-height, --sticky-offset)
│           ├── animations.css         ← keyframes: spin, toastIn, successPop, skeletonPulse
│           ├── components.css         ← Design system completo (~2500 líneas)
│           └── index.css              ← @import chain + Google Fonts + reset
│
├── admin-react/                       ← Admin panel
│   ├── src/
│   │   ├── App.jsx                    ← Router + auth gate + onboarding gate
│   │   ├── main.jsx                   ← Entry point React
│   │   ├── context/
│   │   │   └── DataContext.jsx        ← Estado global, Realtime, polling 30s, chime loop con acknowledge
│   │   ├── hooks/
│   │   │   └── useAuth.js             ← Login/logout Supabase Auth
│   │   ├── lib/
│   │   │   ├── supabase.js            ← Cliente Supabase singleton
│   │   │   └── utils.js               ← cn(), fmt(), playChime() (loop 4s, retorna {stop})
│   │   ├── pages/
│   │   │   ├── LoginPage.jsx
│   │   │   ├── OnboardingPage.jsx
│   │   │   ├── DashboardPage.jsx
│   │   │   ├── OrdersPage.jsx
│   │   │   ├── MenuPage.jsx
│   │   │   ├── CustomersPage.jsx
│   │   │   ├── IngredientsPage.jsx
│   │   │   ├── SettingsPage.jsx
│   │   │   └── ConversationsPage.jsx
│   │   └── components/
│   │       ├── layout/
│   │       │   ├── AppShell.jsx       ← Wrapper Sidebar + MobileNav + content
│   │       │   ├── Sidebar.jsx        ← Nav desktop
│   │       │   └── MobileNav.jsx      ← Nav mobile con popup "Más"
│   │       ├── menu/
│   │       │   ├── ProductsTab.jsx    ← CRUD productos + drag-reorder + duplicate + Toggle shared + toast
│   │       │   ├── CategoriesTab.jsx  ← CRUD categorías + drag-reorder
│   │       │   └── ModifiersTab.jsx   ← CRUD modificadores con editor key-value dinámico
│   │       ├── orders/
│   │       │   └── OrderDetailModal.jsx ← Detalle + cambio de estado + notificación WA
│   │       └── shared/
│   │           ├── Toast.jsx          ← useToast() hook
│   │           ├── ConfirmDialog.jsx  ← HeroUI Modal (reemplaza confirm())
│   │           ├── Toggle.jsx         ← Toggle accesible con ARIA
│   │           ├── StatsCard.jsx      ← Card KPI reutilizable con onClick opcional
│   │           ├── SectionHeader.jsx  ← Header de sección con icono
│   │           ├── InputField.jsx     ← Input con label
│   │           └── Skeleton.jsx       ← KpiSkeleton, TableSkeleton, KanbanSkeleton
│   └── vercel.json                    ← SPA rewrite config
│
├── supabase/
│   ├── migrations/
│   │   ├── 20260319_kapso_pedidos.sql             ← Patch: delivered_at, feedback_sent
│   │   ├── 20260329_fix_rls_security.sql          ← RLS hardening
│   │   ├── 20260404_schema_base.sql               ← Schema completo versionado
│   │   ├── 20260405_order_tracking_rpcs.sql       ← RPCs: get_order_status, get_last_order ✅ aplicada
│   │   ├── 20260405_pedidos_mesa.sql              ← ALTER TABLE pedidos ADD COLUMN mesa TEXT ✅ aplicada
│   │   ├── 20260407153202_add_custom_domain.sql   ← custom_domain en restaurantes ✅ aplicada
│   │   ├── 20260411_delivery_zones.sql            ← Tabla zonas_delivery + RLS ✅ aplicada
│   │   ├── 20260412_chat_media_bucket.sql         ← Bucket chat-media ✅ aplicada
│   │   ├── 20260413_grupos_modificadores.sql      ← grupos_modificadores + adicionales.grupo_id ✅ aplicada
│   │   ├── 20260413_producto_tags.sql             ← productos.tags text[] + GIN index ✅ aplicada
│   │   ├── 20260413_seed_soli_sushi.sql           ← Seed Soli Sushi (112 prods, 7 grupos) ✅ aplicada
│   │   ├── 20260415_feedback_scheduler_fixes.sql  ← Scheduler fixes pg_cron ✅ aplicada
│   │   ├── 20260416_review_flow.sql               ← pedido_review_turns + review_classifier_calls ✅ aplicada
│   │   ├── 20260421_seed_el_charakato.sql         ← Seed El Charakato (9 cat, 53 prods) ✅ aplicada
│   │   └── 20260422_seed_hillfood.sql             ← Seed Hillfood (demo) — pendiente commitear y verificar en prod
│   └── functions/
│       ├── kapso-setup/
│       ├── kapso-webhook/
│       ├── kapso-send/
│       ├── kapso-conversations/
│       ├── kapso-messages/
│       ├── kapso-feedback-scheduler/
│       ├── kapso-review-flusher/              ← cron 1 min, debounce flush + invoca review-classifier
│       └── review-classifier/                 ← Claude Haiku 4.5, sentimiento + reply
│
└── docs/
    ├── auditoria-rls-2026-03-29.md          ← Auditoría RLS (2026-03-29)
    ├── pendiente-pre-live.md                 ← Acciones manuales históricas
    ├── qa-track-b.md                         ← QA findings del merge de Track B
    ├── sesion-2026-04-06-deploy.md           ← Notas de sesión de deploy
    ├── white_cassini_migration_plan.md       ← Estrategia de migraciones DB
    ├── white_cassini_ui_report.md            ← Reporte UI/UX pre-launch
    ├── reporte-auditoria-2026-04-06.md       ← Auditoría completa del proyecto (estado al 2026-04-06)
    ├── pre-live-abril.md                     ← Plan de ejecución pre-live: bloqueantes + polish
    ├── plan-detallado-tareas.md              ← Task tracker TCK-01…TCK-13 (fuente de verdad de pendientes)
    ├── roadmap-interno.md                    ← Roadmap 4 fases: pre-live → post-live → estabilización → enterprise
    ├── Revision flujo.md                     ← Bugs QA reportados por El Padrino (producción real)
    ├── white_label_domain_strategy.md        ← Automatización de dominios custom via Vercel API (futuro)
    ├── White Cassini revision/               ← Screenshots + revisión UX del admin panel
    └── evaluacion de nuevo scope/
        └── primera-evaluacion.md            ← 7 solicitudes El Padrino — análisis, decisiones, sprints
```

---

## 3. Responsabilidad de cada módulo

### Customer App (`customer-app/src/`)

| Módulo | Responsabilidad |
|--------|----------------|
| `app.tsx` | Root: lee slug de URL, registra toast callback, monta hooks. Renderiza `HomeView` o `MenuView` según `currentView` signal. Overlays globales (modal, carrito, checkout, sheet) siempre montados. |
| `hooks/useStore` | Carga restaurante, productos, categorías, extras, variantes, zonas_delivery, grupos_modificadores. Suscripción Realtime a `productos` y `restaurantes` |
| `hooks/useBranding` | Aplica `config_marca` (color_primario, color_secundario, tema) como CSS vars en tiempo real |
| `hooks/useStoreStatus` | Evalúa horario actual cada 60s. Expone `isOpen`, `nextOpen` |
| `hooks/useOrderTracking` | Polling RPC `get_order_status` cada 10s cuando `activeOrderId` está activo |
| `hooks/useCustomerMemory` | Lee `wc_customer_name` y `wc_customer_phone` de localStorage |
| `signals/store` | `restaurant`, `menuData` (incluye `grupos: GrupoModificador[]`), `storeStatus`, `isLoading`, `minOrderAmount`, `currentCategory`, `deliveryZones` |
| `signals/cart` | `cart` (CartItem[]), `cartTotal`, `cartCount`. Auto-persiste en `wc_cart_{restaurante_id}` |
| `signals/order` | `activeOrderId`, `orderStatus`, `orderNumber`. Persiste en `sessionStorage` |
| `signals/mesa` | `mesaNumber` — lee `?mesa=` de URL al importar |
| `signals/ui` | `toastMessage`, `toastType`, `orderSuccessData`, `currentView` ('home'|'menu'), `pendingScrollCategoryId` (id de la categoría a la que hacer scroll al montar MenuView), `isCategoryNavOpen` |
| `components/Navbar` | Logo, badge estado tienda, trigger búsqueda, CartBadge. Cuando `currentView === 'menu'`: muestra botón back-to-home a la izquierda del logo |
| `components/HeroSection` | Hero image/logo, nombre restaurante, chips separados de `pickup_time` y `delivery_time` (con fallback a `prep_time`) |
| `components/CategoryTabs` | [DEPRECADO — solo en legacy] Tabs horizontales con scroll indicator. En MenuView usa `CategoryTabsSticky` |
| `components/ProductGrid` | Filtra por prop `categoryId` (si viene) o `currentCategory` signal (fallback). En modo búsqueda muestra grid cross-category. Acepta `categoryId?: string` — cuando se usa en `MenuView` cada sección pasa el suyo |
| `components/HomeView` | Vista inicial del cliente. Renderiza `HeroSection`, `QuickReorder` y el grid de `CategoryHomeCard`. Al hacer click en una card setea `pendingScrollCategoryId` + `currentView = 'menu'` |
| `components/CategoryHomeCard` | Card visual de categoría: imagen del primer producto disponible (fallback a `IMG_PLACEHOLDER`), nombre, count de disponibles. Activa la transición al menú |
| `components/MenuView` | Vista de menú completo. Al montar: lee `pendingScrollCategoryId` y hace `scrollTo` a la sección correspondiente con `requestAnimationFrame`. Renderiza una `<section id="cat-{id}">` por categoría. En modo búsqueda activa, muestra un único `ProductGrid` cross-category |
| `components/CategoryTabsSticky` | Tab bar con `position: sticky` debajo del navbar. IntersectionObserver sobre `.menu-section` actualiza `currentCategory` al scrollear. Click en tab → `scrollTo` suave a la sección. Botón `more_vert` abre `CategoryNavSheet` |
| `components/CategoryNavSheet` | Bottom sheet (reutiliza `.modal-content.bottom-sheet`) con lista completa de categorías y count de productos. Al seleccionar: cierra el sheet y hace scroll suave a la sección |
| `components/ProductCard` | Imagen lazy, overlay Agotado, pills de tags (hasta 3) debajo del nombre con colores/emojis de `tagLabels.ts`, abre ProductModal |
| `components/ProductModal` | Bottom sheet: variantes, grupos de modificadores (radio/checkbox con min/max, validación antes de agregar al carro), extras planos legacy, cantidad, notas, precio dinámico |
| `lib/tagLabels.ts` | Catálogo de tags: slug → `{label, color}`. Ampliar aquí para nuevos tags sin migraciones |
| `components/CartSidebar` | Panel lateral: items editables, qty, min order progress bar, botón checkout |
| `components/CheckoutModal` | Tipo entrega, CustomerForm, selector de zona de delivery (si hay zonas configuradas), resumen colapsable, costo envío dinámico (zona o fijo), total, submit a WA con zona en mensaje |
| `components/CustomerForm` | Delivery/Retiro cards con tiempo estimado, nombre, teléfono (+normalización Chile), dirección, método pago |
| `components/OrderSuccess` | Overlay post-checkout con link directo a WhatsApp |
| `components/FloatingOrderButton` | Botón flotante que persiste post-pedido; activa OrderTracker al presionar |
| `components/OrderTracker` | Timeline visual de 4 estados con mensajes contextuales |
| `components/SearchBar` | Modal buscador client-side sobre `menuData.products` |
| `components/QuickReorder` | Chip en hero: trae último pedido via RPC `get_last_order`, rellena carrito |
| `components/ClosedBanner` | Banner "Abre en X horas" cuando `storeStatus.isOpen === false` |
| `components/OfflineBanner` | Banner PWA cuando `navigator.onLine === false` |
| `lib/utils` | `formatPrice`, `buildWhatsAppUrl`, `normalizeChileanPhone`, `escapeHtml`, `IMG_PLACEHOLDER`, `WHATSAPP_SVG` |
| `lib/storage` | `getItem`/`setItem` wrappers + constantes: `CUSTOMER_NAME_KEY`, `CUSTOMER_PHONE_KEY` |

### Admin Panel (`admin-react/src/`)

| Módulo | Responsabilidad |
|--------|----------------|
| `App.jsx` | Router (9 rutas). Auth gate → onboarding gate → páginas protegidas |
| `DataContext.jsx` | Estado global: products, categories, orders, clients, ingredients, modifiers, settings, deliveryZones. Realtime `pedidos`. Chime en loop (4s) con per-order acknowledge + ref para detener. Polling fallback 30s |
| `useAuth.js` | Login/logout Supabase Auth. Expone `user`, `loading`, `signIn`, `signOut` |
| `DashboardPage` | 4 KPIs reales (revenue, pedidos, ticket, efectivo hoy vs ayer). Top 5 productos. Toggle tienda desde chip |
| `OrdersPage` | Kanban drag-drop 4 columnas. Cards no reconocidos con borde animado (pulse). Click o drag a "Preparando" acknowledge el chime. Filtro de archivadas. Toggle "Ver archivadas". Mesa chip en cards |
| `MenuPage` | Tabs: ProductsTab, CategoriesTab, ModifiersTab |
| `ProductsTab` | CRUD + drag-reorder + duplicate. Toggle shared + toast. StatsCard "Sin Stock" clickeable. Preview imagen URL. Sección "Grupos de Opciones" en ProductModal: CRUD completo de grupos (radio/checkbox, min/max, drag-reorder) + CRUD anidado de adicionales por grupo. Editor de tags con chips, autocomplete por restaurante y normalización automática (lowercase/sin tildes/underscore) |
| `CategoriesTab` | CRUD + drag-reorder |
| `ModifiersTab` | CRUD de modificadores **planos** (filtra `grupo_id IS NULL`). Aviso en header: los modificadores de grupos se editan desde el producto |
| `CustomersPage` | Lista + búsqueda nativa. KPIs con StatsCard. Categorización Nuevo/Recurrente/VIP. Modal historial con items por pedido. Export CSV |
| `IngredientsPage` | CRUD + drag-reorder |
| `SettingsPage` | 4 tabs: Negocio (nombre + WhatsApp), Operaciones (pickup_time + delivery_time + delivery_cost + CRUD zonas delivery + métodos pago), Horarios (multi-slot semanal), Integraciones (Kapso + mensajes automáticos) |
| `ConversationsPage` | 3 paneles: lista conversaciones + búsqueda, hilo de mensajes, OrderPanel con nav prev/next para múltiples pedidos. EmojiPicker. Estado de orden en lista. Badge Recurrente/VIP |
| `OnboardingPage` | 4 pasos: nombre, colores, upload menú PDF/imagen, procesamiento IA. Timeout 3 min |
| `LoginPage` | Email/password Supabase Auth. Botón nativo con estilo primario |
| `OrderDetailModal` | Detalle pedido + botones de estado que notifican via Kapso |

### Backend (`supabase/`)

| Edge Function | Método | `--no-verify-jwt` | Responsabilidad |
|---------------|--------|-------------------|----------------|
| `kapso-setup` | POST | **SÍ** | Crea customer Kapso + genera setup link OAuth |
| `kapso-webhook` | GET + POST | **SÍ** | GET: callback OAuth. POST: eventos Kapso. Router de review: si hay pedido esperando review, buferea mensaje. Si no, welcome |
| `kapso-send` | POST | **SÍ** | Envía mensajes WA: welcome, order_accepted, order_sent, order_ready, feedback, manual, **custom_text** (texto directo sin template). v18+: resuelve pickup_time/delivery_time por tipo de pedido. Auth: `x-internal-secret` header (callers internos) → skip ownership; user JWT → `auth.getUser()` verify ownership. |
| `kapso-conversations` | GET/POST | **SÍ** | Lista últimas 100 conversaciones (filtradas a activas) |
| `kapso-messages` | GET/POST | **SÍ** | Lista últimos 100 mensajes de una conversación |
| `kapso-feedback-scheduler` | Cron | **SÍ** | Cada 15 min (pg_cron jobid 1): pedidos `enviado`/`entregado` con delay configurable (`feedback_delay_minutes`, default 60 min) → invoca kapso-send type `feedback`. Registra turno inicial en `pedido_review_turns`, setea `review_prompt_sent_at` |
| `review-classifier` | POST | **SÍ** | Clasifica sentimiento + genera reply empático vía Claude Haiku 4.5. Auth: service_role key en header. Hard cap 3 turnos (code-enforced). Circuit breaker: `review_classifier_calls >= 4` → 429 |
| `kapso-review-flusher` | Cron | **SÍ** | Cada 1 min (pg_cron jobid 2): flush buffers de debounce vencidos (30s). Optimistic concurrency. Invoca review-classifier + kapso-send type custom_text |

> **⚠️ Deploy:** Todas las Edge Functions requieren `--no-verify-jwt`. Sin este flag el gateway retorna 401 silenciosamente.
>
> **⚠️ Inter-function auth:** El scheduler llama a `kapso-send` vía `supabase.functions.invoke` (NO raw `fetch`). El gateway de Supabase no propaga el header `Authorization` en llamadas inter-función vía URL pública; `invoke` usa routing interno que sí lo hace.
>
> **⚠️ kapso-send auth:** Callers internos (scheduler, flusher, webhook) envían header `x-internal-secret: $INTERNAL_WEBHOOK_SECRET` — la función lo verifica con comparación SHA-256. El admin envía user JWT validado internamente vía `auth.getUser(token)`. Ambos paths son seguros sin depender del gateway. Deploy CON `--no-verify-jwt` (igual que las demás functions).

---

## 4. Esquema de base de datos

Todas las tablas scoped por `restaurante_id`. Migraciones versionadas desde `20260319`.

| Tabla | Campos clave | Uso |
|-------|-------------|-----|
| `restaurantes` | id, user_id, nombre, slug, telefono_whatsapp, logo_url, config_marca (JSON), config_operaciones (JSON), config_pagos_integraciones (JSON), horarios_semana (JSON), onboarding_status, is_active | Config central del restaurante |
| `productos` | id, restaurante_id, nombre, precio_base, imagen_url, descripcion, categoria_id, orden, disponible, **tags text[]** | Items del menú. `tags` es array nativo con índice GIN; default `'{}'`. Slugs lowercase sin tildes (ej: `vegano`, `keto`, `picante`, `nuevo`, `panko`, `sin_gluten`, `nuez`) |
| `variantes_producto` | id, producto_id, nombre, precio, orden | Tamaños/variantes. **Sin `restaurante_id`** — no incluirlo en INSERTs |
| `categorias` | id, restaurante_id, nombre, orden | Agrupación de productos |
| `adicionales` | id, restaurante_id, nombre, precio, opciones_precio (JSON), disponible, categoria_id, producto_id, orden, **grupo_id uuid** | Extras/modificadores. `grupo_id IS NULL` = modificador plano (legado); `grupo_id NOT NULL` = sub-opción de un grupo (se edita desde el producto, no desde ModifiersTab) |
| `grupos_modificadores` | id, restaurante_id, producto_id, nombre, tipo (`radio`\|`checkbox`), min_seleccion, max_seleccion, orden | Agrupa adicionales bajo reglas de selección. Usado para builders tipo "Arma tu Promo". RLS espejo de adicionales |
| `pedidos` | id, restaurante_id, cliente_id, estado, metodo_pago, tipo_entrega, direccion, mesa, numero_pedido, delivered_at, feedback_sent, created_at | Pedidos |
| `pedido_items` | id, pedido_id, producto_id, variante, extras (JSON), cantidad, precio_unitario, notas | Líneas del pedido. `extras` jsonb libre — compatible con adicionales de grupos sin cambio |
| `clientes` | id, restaurante_id, nombre, telefono | Clientes registrados |
| `zonas_delivery` | id, restaurante_id, nombre, precio, activa, orden, created_at | Zonas de delivery con precio variable. RLS: SELECT público solo para zonas activas; admin CRUD por ownership de restaurante |

**Estados de pedido:** `pendiente` → `preparando` → `enviado` → `entregado`

**RPCs disponibles:**
| RPC | Auth | Descripción |
|-----|------|-------------|
| `submit_order_v1` | anon | Inserta pedido + items + cliente. Retorna `{success, pedido_id, numero_pedido}` |
| `get_order_status` | anon | Retorna estado actual de un pedido por ID |
| `get_last_order` | anon | Retorna último pedido de un teléfono para Quick Reorder |

**Campos JSON de `config_operaciones` usados por customer app y kapso-send:**

| Campo | Tipo | Uso |
|-------|------|-----|
| `delivery_active` | boolean | Mostrar/ocultar opción Delivery en checkout |
| `delivery_cost` | number | Costo de envío fijo (se ignora cuando hay zonas_delivery activas) |
| `pickup_time` | number (min) | Chip "Retiro ~X min" en hero + subtítulo en botón Retiro del checkout. Usado por kapso-send en aceptación de pedidos tipo Retiro |
| `delivery_time` | number (min) | Chip "Delivery ~X min" en hero + subtítulo en botón Delivery del checkout. Usado por kapso-send en aceptación de pedidos tipo Delivery |
| `prep_time` | number (min) | Campo legacy — usado como fallback cuando pickup_time/delivery_time no existen |
| `min_order` | number | Barra de progreso en carrito + bloqueo de checkout |
| `metodos_pago` | string[] | Lista de opciones en select de pago |

---

## 5. Integraciones

### Supabase (core)
- **Auth:** Email/password, session management
- **Database:** PostgreSQL con RLS
- **Realtime:** `pedidos` y `pedido_items` en admin; `productos` y `restaurantes` en customer app
- **Storage:** Upload logo y menú PDF en onboarding
- **RPC:** `submit_order_v1`, `get_order_status`, `get_last_order`
- **Edge Functions:** 8 funciones TypeScript (kapso-setup, kapso-webhook, kapso-send, kapso-conversations, kapso-messages, kapso-feedback-scheduler, kapso-review-flusher, review-classifier)

### Kapso (WhatsApp Business API)
- Setup OAuth, webhooks, mensajería (6 tipos), lectura de conversaciones/mensajes, scheduler feedback

### WhatsApp (directo)
- Customer app genera link `wa.me/{phone}?text={order_summary}` para confirmación manual. Independiente de Kapso.

### Vercel
- Admin: `white-cassini-admin.vercel.app` (Root Directory: `admin-react`) + dominio custom `admin.kitchat.cl`
- Customer: `white-cassini-sigma.vercel.app` (Root Directory: `customer-app`)

### PWA (customer app)
- Workbox via `vite-plugin-pwa`. Service Worker con precaching. `OfflineBanner` cuando sin conexión.

### Web Audio API (admin)
- Chime de 3 tonos (C5, E5, G5) en loop cada 4s. Hay dos contextos:
  - **Pedidos** (`DataContext.jsx`): se inicia al recibir un INSERT en `pedidos`. Se detiene en cuanto el operador **abre el OrderDetailModal** del pedido (acknowledge por orden — `useEffect` en el modal, no requiere aceptar). Cards sin reconocer muestran borde pulse. `chimeRef` en DataContext guarda el `{ stop }` handle.
  - **Mensajes WA** (`ConversationsPage.jsx`): se inicia al detectar mensajes entrantes nuevos. Se detiene cuando se selecciona la última conversación con mensajes no leídos. También se detiene al navegar fuera de Conversaciones (cleanup de unmount). `chimeRef` local en el componente.

---

## 6. Comandos de desarrollo

```bash
# Customer App
cd customer-app
npm install
npm run dev       # Vite HMR en localhost:5173
npm run build     # Build producción → dist/ (0 errores esperados)

# Admin React
cd admin-react
npm run dev       # Vite HMR en localhost:5174
npm run build     # Build producción → dist/

# Supabase
supabase start
supabase db push
supabase functions serve
supabase functions deploy kapso-send --project-ref gjkaboosygjitxgqcawy --no-verify-jwt
# ⚠️ TODAS las edge functions requieren --no-verify-jwt. kapso-send valida auth internamente.
```

---

## 7. Convenciones

- **No TypeScript** en admin-react — plain `.js`/`.jsx`
- **TypeScript estricto** en customer-app — `.ts`/`.tsx`
- **Tailwind v3.4** en admin-react con PostCSS clásico + `tailwindcss-animate`
- **Sin Tailwind** en customer-app — branding dinámico requiere CSS vars runtime
- **Dark mode admin** vía clase `dark` en `document.documentElement`, persistido en `localStorage('theme')` y en `config_marca.tema`
- **Supabase anon key** en `.env.local` de customer-app (no commiteado). En admin-react hardcodeado en `supabase.js` (pública por diseño, seguridad vía RLS)
- **Iconos:** Material Symbols Outlined — única librería en ambas apps
- **Locale:** `es-CL` en todos los componentes
- **Tokens de color admin:** `bg-primary`, `text-primary` (HeroUI). NO usar `#22d86b` hardcodeado. Excepción: `#25D366` (WhatsApp brand)
- **Notificaciones admin:** `useToast()`. Cero `alert()` nativos
- **Confirmaciones admin:** `<ConfirmDialog>`. Cero `confirm()` nativos
- **Settings:** Slug y colores de marca los gestiona el equipo internamente. El restaurante solo edita nombre, WhatsApp, logística y horarios
- **Deploy Edge Functions:** Respetar flag `--no-verify-jwt` por función (ver tabla sección 3). Usar siempre `--project-ref gjkaboosygjitxgqcawy` explícito

---

## 8. Tenants activos

| Tenant | Slug | URL customer | Credenciales admin | Estado |
|--------|------|-------------|-------------------|--------|
| El Padrino | `elpadrino` | `?local=elpadrino` | admin@elpadrino | ✅ Activo, pagando |
| Soli Sushi | `soli-sushi` | `?local=soli-sushi` | jescobp@gmail.com (TempPass2026! — debe cambiar) | 🟡 Onboarded, no operativo |
| El Charakato | `el-charakato` | `?local=el-charakato` | — (TempPass2026! — debe cambiar) | 🟡 Seed aplicado, pendiente QA |
| Hillfood | `hillfood` | `?local=hillfood` | — | 🔧 Demo — seed 20260422 sin commitear/verificar en prod |

> Fuente canónica completa: `docs/decisiones-canonicas.md §6`

---

## 9. Pendientes, estado de producción y ramas (Git)

**Estado de Ramas (Visión General al 2026-04-22):**
- `main` (PRODUCCIÓN ACTUAL): Incluye Sprint 5 (home categorías + menú scroll anclado) mergeado 2026-04-20, Review Flow IA (kapso-review-flusher + review-classifier) deploado 2026-04-20, Bug #3.2/#3.3 resueltos 2026-04-20/21, light theme dinámico, seed El Charakato.
- `track-b` (OBSOLETA): Rama de re-branding. Cambios mergeados a main. Worktree `.worktrees/track-b/` pendiente de limpiar.
- `feature/customer-redesign` (OBSOLETA): Mergeada a main (PR #2, commit `97704fa`). Worktree `.worktrees/customer-redesign/` pendiente de limpiar.

---

### Sprint 5 — Rediseño customer app (mergeado 2026-04-20)

**Rama:** `feature/customer-redesign` (commit `4e0bd7c`). Mergeado a `main` como PR #2 (commit `97704fa`, 2026-04-20).

**Estado:** ✅ En producción en Vercel.

**Cambios (solo UI, sin tocar DB/admin/edge functions):**
- `HomeView` + `CategoryHomeCard` — pantalla inicial con grid de categorías visuales
- `MenuView` — menú scrolleable con todas las secciones ancladas
- `CategoryTabsSticky` — tab bar sticky + IntersectionObserver + botón tres puntos
- `CategoryNavSheet` — bottom sheet de navegación rápida
- `Navbar` — botón back-to-home en vista menú
- `ProductGrid` — prop `categoryId?` opcional (backward-compatible)
- `signals/ui.ts` — signals: `currentView`, `pendingScrollCategoryId`, `isCategoryNavOpen`
- `tokens.css` — vars: `--navbar-height`, `--tab-bar-height`, `--sticky-offset`

**QA esperado (con ?local=elpadrino / ?local=soli-sushi, NO hacer checkout con tenants reales):**
1. Carga arranca en HomeView con grid de categorías
2. Click en card → MenuView scrolleado a esa sección
3. Tab bar sticky: highlight automático al scrollear
4. Botón tres puntos → bottom sheet con todas las categorías
5. Back-to-home en navbar
6. Search global funciona sin regresar al home
7. Carrito, checkout, modal de producto: sin regresiones

---

**Acciones manuales completadas (2026-04-13) — Grupos + Tags + Soli Sushi:**
- ✅ Migración `20260413_grupos_modificadores.sql` aplicada (tabla `grupos_modificadores` + `adicionales.grupo_id`)
- ✅ Migración `20260413_producto_tags.sql` aplicada (`productos.tags text[]` + índice GIN)
- ✅ Seed `20260413_seed_soli_sushi.sql` aplicado — 16 categorías, 112 productos, 132 variantes, 7 grupos, 46 adicionales agrupados
- ✅ Usuario `jescobp@gmail.com` creado via Auth Admin API en proyecto `gjkaboosygjitxgqcawy`
- ✅ Commit `afd0d22` pusheado a main — Vercel desplegando ambas apps

**Acciones manuales completadas (2026-04-12) — Sprints El Padrino:**
- ✅ Vercel root directories configurados (`admin-react` y `customer-app`)
- ✅ Migración `20260405_order_tracking_rpcs.sql` aplicada (RPCs de order tracking)
- ✅ Migración `20260405_pedidos_mesa.sql` aplicada (columna mesa en pedidos)
- ✅ Migración `20260411_delivery_zones.sql` aplicada (tabla zonas_delivery + RLS)
- ✅ `kapso-send` v18 redesplegado con soporte pickup_time/delivery_time
- ✅ Chime de pedidos para cuando se abre el modal (no solo al aceptar)
- ✅ Chime de mensajes WA con loop controlado (para al leer la conversación)

**Pendiente del lado del cliente:**
- **Soli Sushi:** cambiar password TempPass2026!, reemplazar teléfono WA (+56900000000), confirmar horarios, subir fotos, decidir delivery
- **El Padrino:** configurar `pickup_time` y `delivery_time` en Settings > Operaciones

**Bugs conocidos en producción** (fuente: `docs/Revision flujo.md`, QA con El Padrino):

| Área | Bug | Severidad |
|------|-----|-----------|
| Customer — 1.2 | Hora "abre en X horas" muestra timezone incorrecto (desfase ~5h) | Alta |
| Customer — 1.3 | Chip `~X min` de pickup/delivery no aparece en hero | Alta |
| Customer — 1.7 | SearchBar: click fuera del teclado borra la búsqueda activa | Media |
| Customer — 1.9 | Toggle delivery no se refleja en checkout; botón "pedir" queda fuera de pantalla; métodos de pago extra no aparecen | Alta |
| Customer — 1.11 | Order Tracker no actualiza en tiempo real (requiere reload de página); FloatingOrderButton no desaparece en estado "entregado" sin reload | Alta |
| Customer — 1.13 | Branding dinámico no aplica en customer app; dark mode de El Padrino es fijo (configurable solo por soporte) | Baja |
| Admin — 2.1 | Login: placeholder de campos no se borra al escribir | Media |
| Admin — 2.2 | Dashboard: Top 5 productos muestra $0; chips "Tienda abierta" y "Ver tienda" no tienen estilo de chip | Media |
| Admin — 2.3 | OrderDetailModal abre sin overlay de fondo | Media |
| Admin — 2.4 | Modal edición de producto sin fondo; reordenar producto recarga la página | Media |
| Admin — 2.5 | Categorías sin indicador de orden numérico; reordenar recarga la página | Media |
| Admin — 2.6 | Modal de modificadores sin fondo | Media |
| Admin — 2.7 | Modal historial de clientes sin fondo | Media |
| Admin — 2.8 | Textarea de respuestas no crece con el contenido; Emoji picker abre comprimido | Baja |
| ~~Integración — 3.2~~ | ~~Mensajes automáticos Kapso no llegan~~ | ~~Alta~~ — **✅ RESUELTO** commit `d7a2da9` (2026-04-20): kapso-send service_role auth |
| ~~Integración — 3.3~~ | ~~kapso-send gateway JWT 401~~ | ~~Alta~~ — **✅ RESUELTO** commit `22e67f0` (2026-04-21) |

> **Fuente de verdad de bugs abiertos:** `docs/bugs-abiertos.md`. Los docs `plan-detallado-tareas.md` y `pre-live-abril.md` están archivados en `docs/archive/` y **no deben usarse como referencia**.

**Nuevos Ajustes y Requerimientos Críticos (2026-04-15):**
- ✅ **Bug Automatización Reviews (RESUELTO 2026-04-15):** `kapso-feedback-scheduler` nunca se invocaba (faltaba pg_cron + el deploy tenía verify_jwt=true). Fix: pg_cron habilitado, cron job `*/15 * * * *` registrado, función redesplegada con `--no-verify-jwt`, query ampliada a `enviado`+`entregado`, ventana 24h, cleanup de expirados, error retryable vs no-retryable. Pendiente confirmar envío de mensajes cuando se resuelva el bug #3.2 de mensajes automáticos Kapso.
- 🟡 **Impresión de comandas:** Print agent local (Node.js + Raspberry Pi) suscrito a Supabase Realtime. Multi-tenant via `config_operaciones.print_config`. El Padrino tiene Epson TM-T88IV M129h Ethernet lista. Ver análisis completo + arquitectura + plan de fases en `docs/impresion-comandas-plan.md`. Decisiones pendientes antes de ejecutar: 5 preguntas documentadas en el plan.
- 🟡 **Agente WhatsApp (Admin):** [Deal breaker possible]. Permitir al dueño/admin ajustar menú, activar/desactivar items y cambiar precios directo por WA (mismo número) sin depender de UI técnica. Pendiente evaluar pricing/infra.

**Features fuera de scope inicial:**
- Mercado Pago (requiere credenciales por restaurante + SDK MP)
- Modo mesa completo (TCK-11) — pendiente post-launch

---

## 10. Decisiones técnicas consolidadas

| Área | Decisión | Razón |
|------|----------|-------|
| CSS customer-app | Sin Tailwind | Branding dinámico requiere CSS vars en runtime |
| Realtime productos | Sin filtro DB en suscripción | Supabase ignora filtros sin índice; filtro en JS |
| RLS productos | `USING (true)` pública | Realtime no entrega eventos de desactivados con filtro disponible=true |
| Cart key | `wc_cart_{restaurante_id}` | Evita colisiones entre restaurantes en mismo browser |
| Teléfonos | Solo Chile (+56) | Normalización hardcodeada, multi-país fuera de scope V1 |
| Order Tracker | Polling 10s via RPC | Realtime bloqueado por RLS con anon key |
| Sin paginación | Todo en memoria | Aceptable para V1 con volumen actual |
| Slug/colores | Gestionados internamente | El onboarding los configura; no se exponen en Settings |
| Zonas delivery | Sin Realtime en suscripción | Cambios de zonas son infrecuentes; se cargan al inicio de sesión |
| Tags de productos | `text[]` nativo con índice GIN, catálogo en código (`tagLabels.ts`) | Evita tabla de catálogo y migraciones para agregar tags nuevos; catálogo emerge del uso del restaurante |
| Grupos modificadores | `grupo_id IS NULL` = legado (sin cambio), `NOT NULL` = agrupado | Backward-compat total para El Padrino; nuevos builders solo en productos que los necesitan |
| Arquitectura de vistas customer app | Signal `currentView` ('home'\|'menu') + condicional en `app.tsx` (sin router) | Consistente con el patrón de signals existente. Cero deps nuevas. Home y menú comparten todos los overlays globales montados fuera del condicional |
| Scroll anclado a categoría | `requestAnimationFrame` + `getBoundingClientRect()` + offset `--sticky-offset` | `scroll-margin-top` en CSS es la alternativa, pero tiene quirks en Safari iOS con sticky headers anidados. El cálculo manual es más robusto |
| IntersectionObserver en MenuView | `rootMargin: -104px 0px -60% 0px` (arriba = sticky offset, abajo = 60% de viewport) | El threshold del 60% abajo evita que la sección siguiente se active demasiado pronto al scrollear hacia abajo; los 104px arriba compensan el sticky header |
| `variantes_producto` | Sin columna `restaurante_id` | El esquema original no la incluye; no agregar en INSERTs de variantes |

---

## 11. GOTCHAs

### macOS case-insensitive + git
`src/app.tsx` rastreado en minúsculas. Siempre usar `git add customer-app/src/app.tsx` (no `App.tsx`).

### Supabase MCP vs CLI vs Management API
Hay DOS instancias MCP: `mcp__supabase__` (Nutrisco, `kkkqpkyltekphrurjzwp`) y `mcp__supabase-white-cassini__` (este proyecto, `gjkaboosygjitxgqcawy`). El MCP suele no estar disponible. Para queries y migraciones usar **Management API directa** con token del keychain:
```bash
TOKEN=$(security find-generic-password -s "Supabase CLI" -a "supabase" -w | sed 's/go-keyring-base64://' | base64 -d)
# Query
jq -n '{"query": "SQL aquí"}' | curl -s -X POST "https://api.supabase.com/v1/projects/gjkaboosygjitxgqcawy/database/query" -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d @-
# Seed completo (evita problemas de escape)
jq -Rs '{"query": .}' < archivo.sql | curl -s -X POST "https://api.supabase.com/v1/projects/gjkaboosygjitxgqcawy/database/query" -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d @-
```

Para crear usuarios via Auth Admin API (la Management API `/v1/projects/{ref}/auth/users` no existe):
```bash
SERVICE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." # ver api-keys endpoint
curl -s -X POST "https://gjkaboosygjitxgqcawy.supabase.co/auth/v1/admin/users" \
  -H "Authorization: Bearer $SERVICE_KEY" -H "apikey: $SERVICE_KEY" \
  -H "Content-Type: application/json" \
  -d '{"email": "...", "email_confirm": true, "password": "..."}'
```

### Edge Functions sin `--no-verify-jwt`
Un redeploy sin el flag correcto rompe la función silenciosamente — el gateway retorna 401 antes de ejecutar el código. Verificar siempre la tabla de la sección 3.

### Migration history drift
Si `supabase db push` falla por conflicto de historia, usar `supabase migration list` para diagnosticar y `supabase migration repair --status reverted/applied <version>` para sincronizar. Los dos archivos con prefijo `20260405` no se pueden manejar con `db push` estándar — usar Management API directa para esos casos:
```bash
TOKEN=$(security find-generic-password -s "Supabase CLI" -a "supabase" -w | sed 's/go-keyring-base64://' | base64 -d)
curl -X POST "https://api.supabase.com/v1/projects/gjkaboosygjitxgqcawy/database/query" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"query": "SQL aquí"}'
```

### pickup_time / delivery_time vs prep_time
`prep_time` sigue en la DB pero ya no se muestra en Settings. La UI muestra `pickup_time` (Retiro) y `delivery_time` (Delivery). Ambos hacen fallback a `prep_time` si no existen. El campo `prep_time` puede quedar en la DB sin romper nada — no eliminarlo.

### Zonas de delivery vs delivery_cost fijo
Si existen zonas activas en `zonas_delivery`, el `delivery_cost` de `config_operaciones` se ignora en el checkout. Si no hay zonas (o ninguna activa), se usa el costo fijo. Ambos modos son compatibles.

### IIFE pattern en SettingsPage.jsx
El tab `integraciones` usa un IIFE `{activeSettingsTab === 'integraciones' && (() => { ... return (<div>...</div>) })()}` para declarar variables locales dentro de JSX. Cualquier overlay (como `ZoneModal`) debe colocarse **fuera** de este IIFE, después de todos los tabs.

### dominio custom admin.kitchat.cl
El admin se sirve desde `https://admin.kitchat.cl`. Este origen debe estar en `ALLOWED_ORIGINS` de todas las edge functions que el admin invoca: `kapso-setup`, `kapso-conversations`, `kapso-messages`, `kapso-send`. Si se agrega otro dominio custom en el futuro, actualizar esos 4 archivos.

### Preact signals en componentes
El package `@preact/signals` (no `@preact/signals-core`) es el que permite re-render automático en componentes TSX al cambiar una signal. No mezclar.

---

---

## 12. Deuda técnica (pre-mayo 2026)

| Item | Urgencia | Descripción |
|------|----------|-------------|
| Migración BSUID Kapso | 🔴 Alta | Meta ya rollando BSUIDs en webhooks; `phone_number` puede llegar `null`. Evitar fallas silenciosas. Plan: `memory/project_white_cassini_bsuid_migration.md` |
| Versionar trigger `handle_new_user_restaurante` | 🟡 Media | Hoy con comentario "apply via Supabase dashboard" en schema_base.sql. Necesita `CREATE OR REPLACE TRIGGER` en migración dedicada |
| `.env.example` Edge Functions | 🟡 Media | 7 secretos solo documentados en `index.ts`. Crear `supabase/functions/.env.example` |
| Tests automatizados | 🟢 Baja | 0% cobertura, 0 frameworks. Deuda que crece con cada tenant nuevo |

> Fuente canónica completa: `docs/decisiones-canonicas.md §10`

---

*Actualizado: 2026-04-22 — Sprint 5 mergeado + Review Flow IA deployado + Bug #3.2/#3.3 resueltos + 4 tenants (El Padrino, Soli Sushi, El Charakato, Hillfood demo) + 8 Edge Functions + 15 migraciones.*
