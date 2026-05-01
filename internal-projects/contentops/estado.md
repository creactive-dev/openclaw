# ContentOps — Estado del Proyecto

> Archivo de referencia rápida para retomar el proyecto en cualquier sesión.
> Actualizar al cierre de cada sesión de trabajo.

---

## Estado general

**Fase actual:** Fase 2 — LinkedIn e2e — **pendiente de arrancar**
**Última actualización:** 2026-04-17
**Deploy:** https://app-ecru-three-91.vercel.app (Vercel, pendiente dominio custom)
**Dominio target:** ops.creactivestudio.agency
**Repo:** contentops/ (monorepo — supabase/ + app/)

---

## Fases completadas

| Fase | Nombre | Fecha | Commit | Detalle |
|------|--------|-------|--------|---------|
| 0 | Foundation | 2026-04-17 | `0ea29bf` | 14 migraciones SQL (34 tablas), scaffold Next.js 16, auth Supabase, seed data CreActive, deploy Vercel |
| 1 | UI Funcional | 2026-04-17 | `a411c50` | 6 vistas completas (Strategy, Pipeline, Calendar, Generator, Assets, Dashboard). CRUD, Claude API integrado, preview LinkedIn + carrusel IG. Build 0 errores TypeScript, 14 rutas compiladas. |

### Detalle Fase 1 (commit a411c50)
- **Foundation layer:** types (content.ts, api.ts), constantes, clientes Supabase tipados
- **API layer:** brands, tracks, ideas, posts, calendar, assets
- **Shared components:** StatusBadge, TrackTag, FormatIcon, PlatformIcon, SourceBadge, MarkdownEditor
- **Hooks:** use-brand, use-pipeline, use-calendar
- **Strategy:** VoiceEditor, TrackManager con topics anidados, CompetitorList, ReviewIndicator
- **Pipeline:** KanbanBoard 6 columnas (HTML5 drag & drop), IdeaCard, IdeaForm
- **Calendar:** CalendarGrid mensual, DayCell, PostCardMini, AssignDialog, CalendarSidebar
- **Generator:** GeneratorPanel, PreviewPanel, ActionBar
- **Preview:** LinkedInPostPreview (ver más a 210 chars), CarouselIgPreview (slides + grid)
- **AI:** buildBrandContext con prompt caching (cache_control ephemeral), generateContent claude-sonnet-4-6
- **Assets:** AssetGrid drag-drop upload, filtros, detail panel, Supabase Storage
- **Dashboard:** MetricCards, TrackDistributionBar, TrendPlaceholder

---

## Próxima fase

### Fase 2 — LinkedIn e2e

**Objetivo:** Círculo completo para LinkedIn — publicar desde ContentOps, medir resultados, que los datos vuelvan al dashboard.

**Scope según PRD:**
- OAuth perfil personal LinkedIn
- Publicación directa: texto, imagen, PDF (carrusel)
- Scheduling vía n8n
- Retry automático con backoff (máx 3 intentos)
- Estado `blocked` para posts con token expirado
- Pull de métricas automático (24h, 48h, 7d)
- Pull diario de `profile_metrics`
- Cron diario de verificación de tokens (alerta 7 días antes)
- Content scores + benchmarks
- Dashboard con datos reales

---

## Bloqueantes activos

| Tarea | Responsable | Urgencia | Nota |
|-------|-------------|----------|------|
| ANTHROPIC_API_KEY en Vercel env vars | Oscar | 🔴 Inmediato | Key comentada en .env.local — el generador no funciona en prod sin esto |
| Verificar login en app-ecru-three-91.vercel.app | Oscar | 🔴 Pronto | Confirmar que auth Supabase funciona en producción |
| DNS: CNAME `ops` → `cname.vercel-dns.com` | Oscar | 🟡 | Primero agregar dominio en Vercel (Settings → Domains), luego agregar CNAME en DNS provider |
| Supabase Auth → agregar URL redirect `ops.creactivestudio.agency/auth/callback` | Oscar | 🟡 | supabase.com → proyecto ymxdnvywznayxbmjzyhy → Authentication → URL Configuration |
| LinkedIn: app adicional solo para Community Management API | Oscar | 🟢 Fase futura | LinkedIn requiere app dedicada para este producto. No es bloqueante para Fase 2 (posting personal perfil). |

## LinkedIn OAuth — Estado

**App principal (ContentOps):** Client ID `777zochdabinom`
- Productos: Sign In with LinkedIn (OpenID Connect) ✅ + Share on LinkedIn ✅
- Redirect URI configurada: `https://ops.creactivestudio.agency/oauth/linkedin/callback` ✅
- Credenciales guardadas en `.env.local` (ambos niveles)
- **Suficiente para Fase 2 completa** (publicación en perfil personal)

**Community Management API:** requiere app separada en LinkedIn (sin otros productos).
- Usar para: posting en páginas de empresa (no aplica a Fase 2)
- Crear cuando sea necesario para clientes multi-tenant con páginas corporativas

---

## Roadmap completo

| Fase | Nombre | Estado |
|------|--------|--------|
| 0 | Foundation | ✅ Completa |
| 1 | UI Funcional (Core Loop) | ✅ Completa |
| 2 | LinkedIn e2e | 🔴 Pendiente — bloqueada por LinkedIn Developer Portal |
| 3 | Inteligencia v1 (scores + benchmarks + insights + recomendaciones) | ⬜ Pendiente |
| 4 | Motor de ideas (RSS + influencers + competencia + AI proactivo) | ⬜ Pendiente |
| 5 | Instagram e2e | ⬜ Pendiente (iniciar trámites API antes de Fase 5) |
| 6 | Threads e2e | ⬜ Pendiente |
| 7 | Series + Hashtags | ⬜ Pendiente |
| 8 | Multi-tenant + billing (Mercado Pago) | ⬜ Pendiente |
| 9 | Paid integration | ⬜ Pendiente |
| 10 | Avatar IA (HeyGen) | ⬜ Pendiente |

---

## Notas técnicas

- **Next.js:** v16 (breaking changes vs versiones anteriores — leer `node_modules/next/dist/docs/` antes de cualquier cambio)
- **Tailwind:** v3 (no migrar a v4 sin sprint dedicado)
- **shadcn/ui:** componentes en `app/src/components/ui/` — cualquier cambio de tokens afecta todos
- **Preview:** LinkedInPostPreview y CarouselIgPreview tienen dimensiones específicas — no alterar sin validar render
- **Supabase:** RLS activo desde Fase 0, org_id en todas las tablas

---

## Decisión pendiente: Redesign UI

El diseño actual es funcional pero tiene look "legacy". El momento ideal para el redesign es **entre Fase 1 (completada) y Fase 2** — ventana que coincide con el tiempo de espera del LinkedIn Developer Portal.

Referencia visual aprobada: estilo Fixoria (gradiente de fondo, cards con acento de color, íconos semánticos por tipo de métrica, filtros tipo pill).

Scope del redesign: tokens de color en `tailwind.config`, componentes atómicos primero (botones, badges, inputs), luego cards y vistas. Sin tocar lógica.

---

## Historial de sesiones

| Fecha | Qué se hizo |
|-------|-------------|
| 2026-04-17 | Fase 0 completa: git init, 14 migraciones SQL, scaffold Next.js 16, auth, seed data, deploy Vercel. |
| 2026-04-17 | Fase 1 completa: 6 vistas (Strategy, Pipeline, Calendar, Generator, Assets, Dashboard), Claude API integrada, commit `a411c50`. |
| 2026-04-27 | Análisis de estado, resolución de bloqueantes, LinkedIn OAuth configurado (Client ID `777zochdabinom`, Sign In + Share on LinkedIn). Community Management API aclarada como no bloqueante para Fase 2. Credenciales en `.env.local`. |

---

*Última actualización: 2026-04-27 por Oscar + Claude*
