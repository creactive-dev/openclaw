# Workspace Estado — CreActive OS
> Generado: 2026-04-09
> Auditor: /workspace-audit (sesión de auditoría completa)

## Salud general
🟢 Workspace en buen estado — deuda técnica de la semana resuelta. Un pendiente menor: `design-system/` sin documentar.

---

## Inventario

### Clientes activos

| Cliente | CLAUDE.md | estado.md | historial.md | Código | Estado |
|---------|-----------|-----------|--------------|--------|--------|
| constanza-nutricion | ✅ 543L | ✅ 2026-04-03 | ❌ | ✅ Nutrisco (90%) | 🟢 Beta 18/4 |
| fwc-ellinger | ✅ 201L | ✅ 2026-04-09 | ❌ | ✅ (git) | 🟡 Deploy bloqueado por video |
| ph-labs | ✅ 218L | ✅ 2026-04-09 | ❌ | ✅ landing | 🟡 GHL pendiente, deadline 1/5 |
| pumpalcerro | ✅ 100L | ✅ 2026-04-09 | ❌ | ✅ landing | 🟡 Campaña lista, bloqueada por Michi |
| rivas-legal | ✅ 133L | ✅ 2026-03-27 | ❌ | ✅ web+chat | 🟢 Retainer activo |

### Prospectos

| Prospecto | CLAUDE.md | estado.md | Propuesta | Estado |
|-----------|-----------|-----------|-----------|--------|
| fundacion-terapia | ❌ | ❌ | ✅ enviada | 🟡 Sin respuesta registrada |

### Ex clientes

| Cliente | Carpeta | Nota |
|---------|---------|------|
| mallku-consulting | ✅ outputs históricos | Relación terminada |

### Proyectos internos

| Proyecto | CLAUDE.md | En git | Estado |
|----------|-----------|--------|--------|
| Nutrisco (app) | ✅ x4 niveles | ✅ creactive-dev/nutrisco | 🔨 MVP 90%, beta 18/4 |
| Nutrisco Landing | ❌ | ✅ creactive-dev/nutrisco-landing | 🟡 Assets Constanza pendientes |
| White Cassini / Kitcha (app) | ✅ 377L | ✅ | 🟢 En producción |
| Kitcha Landing | ✅ 2026-04-09 | ❌ pendiente push | 🟡 Build listo, deploy pendiente |
| FWC Landing | ❌ | ✅ creactive-dev/fwc | 🟡 En git, deploy bloqueado |
| CreActive Web | ❌ local | ✅ creactive-dev/creactive | 🟢 En producción |
| Content Engine | ❌ CLAUDE.md | ❌ | 🟡 Archivos oscar/ presentes |

---

## Slash Commands

| Prefijo | Completos | Stubs | Total |
|---------|-----------|-------|-------|
| pro- | 4/4 ✅ | 0 | 4 |
| cnt- | 6/6 ✅ | 0 | 6 |
| sal- | 2/3 ✅ | 1 (sal-diagnostico) | 3 |
| cli- | 1/4 ✅ | 3 (onboarding, reporte, minuta) | 4 |
| admin | 2/2 ✅ | 0 | 2 |
| **Total** | **15/19** | **4** | **19** |

---

## Gaps detectados

1. **`fundacion-terapia` sin CLAUDE.md** — Si llega a ser cliente, no hay contexto. Bajo impacto mientras siga en prospecto.
2. **`design-system/`** en raíz del workspace — sin documentación, no está claro si es activo.
3. **Nutrisco Landing sin CLAUDE.md** — landing en git lista, pero sin contexto de proyecto en el workspace.
4. **4 stubs de commands** (`sal-diagnostico`, `cli-onboarding`, `cli-reporte`, `cli-minuta`) — no hacen nada si se ejecutan.
5. **`historial.md` ausente** en todos los clientes — no hay registro de qué se entregó y cuándo por cliente.

---

## Inconsistencias

Ninguna inconsistencia activa al 2026-04-09. Las 6 detectadas en la auditoría de esta semana fueron resueltas:
- ✅ Rivas Legal CLAUDE.md sección 3 actualizada (operativo)
- ✅ Pumpalcerro estado.md actualizado (blocker Meta Ads)
- ✅ FWC Ellinger estado.md actualizado (3 pendientes documentados)
- ✅ PH Labs estado.md actualizado (web lista + GHL pendiente)
- ✅ Kitcha/White Cassini nombre comercial sincronizado en CLAUDE.md raíz
- ✅ kitcha-landing/CLAUDE.md creado desde cero

---

## Alertas activas

| Cliente | Alerta | Urgencia |
|---------|--------|----------|
| Pumpalcerro | Michi debe verificar Meta Ads — viaje Valle del Elqui 21-23 mayo (11 cupos) | 🔴 Alta |
| PH Labs | Deadline landing 1 mayo (22 días) — GHL y dominio pendientes | 🔴 Alta |
| Nutrisco | Beta 18 abril (9 días) — webhook MP pendiente | 🟡 Media |
| Kitcha Landing | Deploy Vercel pendiente — repo no pusheado a GitHub | 🟡 Media |
| FWC Ellinger | Esperando video de Sebastián para go-live | 🟡 Media |

---

## Próximos pasos

- [ ] Hacer seguimiento a Michi (Pumpalcerro) para verificación Meta Ads
- [ ] Configurar GHL de PH Labs (calendarios + correos + flujo de contacto)
- [ ] Webhook Mercado Pago en Nutrisco → activar beta 18 abril
- [ ] Push `kitcha-landing` a `creactive-dev/kitcha-landing` + deploy Vercel
- [ ] Hacer seguimiento a Sebastián (FWC) para recibir video
- [ ] Construir `/cli-minuta` — mayor utilidad en flujo diario de los stubs pendientes

---

## Optimización de tokens activa

| Medida | Estado | Impacto |
|--------|--------|---------|
| `.claudeignore` creado | ✅ | Excluye .next/, node_modules/, .git/ |
| `sal-propuesta` path corregido | ✅ | Path relativo en lugar de absoluto hardcodeado |
| `app/CLAUDE.md` Nutrisco trimado | ✅ | 168L en lugar de 299L (-44%) |
| `constanza-nutricion/CLAUDE.md` sección 15 actualizada | ✅ | Pointer a Nutrisco/CLAUDE.md |
| `supabase/CLAUDE.md` notas operativas trimadas | ✅ | Sin duplicar project ID |

---

*Generado: 2026-04-09 | Basado en auditoría completa del workspace (sesión doble)*
