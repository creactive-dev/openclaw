# ContentOps — CLAUDE.md

> Sistema de marketing operacional end-to-end.
> Estado: PRD v2.1 aprobado — listo para ejecutar Fase 0.

---

## 1. Qué es ContentOps

SaaS de marketing operacional: ideación → generación → preview → publicación → métricas → optimización. Primero para CreActive Studio (Operación 90 + marca personal de Oscar). Después multi-tenant para clientes que se auto-administran.

**Dominio:** ops.creactivestudio.agency
**Deploy:** Vercel
**Stack:** Next.js 14+ (App Router) + Tailwind CSS + shadcn/ui + Supabase + n8n + Claude API

### Contexto de negocio — Operación 90

ContentOps existe para soportar y escalar **Operación 90**, la oferta central de CreActive Studio: consultoría de transformación operacional con IA para PyMEs latinoamericanas ($1.5K-$3K USD setup + $500-$1K USD/mes retainer).

**Tres líneas de revenue donde participa ContentOps:**
1. **Consultoría (Operación 90):** ContentOps gestiona el marketing que atrae leads. Es usuario interno.
2. **ContentOps como servicio:** Oscar lo implementa para clientes como parte de Operación 90. Cobro por setup.
3. **ContentOps SaaS:** Multi-tenant self-service con suscripción mensual (Mercado Pago). Revenue recurrente.

**Secuencia:** Primero usarlo internamente → luego ofrecerlo como servicio → finalmente abrir el SaaS.

**Framework Operational OS (5 fases de implementación con clientes):** Radiografía → Quick Win (resultado en 2-4 semanas) → Arquitectura → Deploy → Evolución. Garantía: si no hay resultado medible en 30 días, es gratis.

**ICP — El Operador Solo:** Emprendedor 28-40, LATAM, negocio de servicios, factura $3M-$15M CLP/mes. Dolor: "el negocio no funciona sin mí."

**Estrategia de contenido — dos carriles:** Carril 1 (30%) credibilidad técnica para devs/founders. Carril 2 (70%) atracción de cliente para Operación 90.

**Detalle completo:** Secciones 2.5 a 2.9 del PRD.md.

---

## 2. Documentación

- **PRD completo:** `PRD.md` en esta misma carpeta. Contiene: modelo de datos SQL, flujo operacional, vistas del frontend, sistema de preview, motor de inteligencia, motor de ideas, integración de plataformas, publicación/scheduling, multi-tenant, roadmap, estructura del proyecto, y todas las decisiones de diseño.

**Regla:** Antes de hacer cualquier cambio en ContentOps, leer el PRD.md completo. Toda decisión de implementación debe ser consistente con lo documentado ahí.

---

## 3. Roadmap (resumen)

| Fase | Nombre | Estado |
|------|--------|--------|
| 0 | Foundation (schema + scaffold + deploy) | Pendiente |
| 1 | Core Loop (estrategia + pipeline + calendario + generador + preview) | Pendiente |
| 2 | LinkedIn e2e (OAuth + publicación + scheduling + métricas) | Pendiente |
| 3 | Inteligencia v1 (scores + benchmarks + insights + recomendaciones) | Pendiente |
| 4 | Motor de ideas (RSS + influencers + competencia + AI proactivo) | Pendiente |
| 5 | Instagram e2e | Pendiente |
| 6 | Threads e2e | Pendiente |
| 7 | Series + Hashtags | Pendiente |
| 8 | Multi-tenant + billing | Pendiente |
| 9 | Paid integration | Pendiente |
| 10 | Avatar IA (HeyGen) | Pendiente |

---

## 4. Principios de desarrollo

1. **Construimos para nosotros primero.** CreActive/Oscar es el primer usuario. Todo se valida con datos reales antes de venderlo.
2. **Círculo completo por plataforma.** No abrir una integración nueva hasta que la anterior esté completa (publicar + métricas + aprendizaje).
3. **El sistema aprende.** Cada post publicado alimenta scores, benchmarks y recomendaciones. Esto es el diferenciador.
4. **Multi-tenant desde el diseño, no como parche.** org_id en todas las tablas, RLS desde el día 1.
5. **Preview antes de aprobar.** Ningún contenido se publica sin preview que simule cómo se verá en la plataforma.
6. **Self-service para clientes.** Cada cliente opera solo. CreActive implementa y se va. Gestión continua es un servicio separado.

---

## 5. Convenciones

- **Migraciones SQL:** Numeradas secuencialmente en `supabase/migrations/`
- **Edge Functions:** Una por responsabilidad en `supabase/functions/`
- **Workflows n8n:** Exportados como JSON en `n8n/`
- **Componentes React:** Un folder por vista en `app/src/components/`
- **API functions:** Un archivo por dominio en `app/src/lib/api/`
- **Types:** Auto-generated desde Supabase en `app/src/types/database.ts`

---

*Última actualización: 2026-04-15*
