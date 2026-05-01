# Contexto de Contacto — Autoritas AI / ARENA
**Slug:** `autoritas-ai`
**Última actualización:** Abril 2026
**Responsable CreActive:** Oscar Vergara Barros
**Tipo de relación:** Peer / Posible colaboración mutua (no cliente)

---

## 1. Datos del contacto

| Campo | Detalle |
|-------|---------|
| **Nombre** | Héctor Partida Bazo |
| **Empresa / Producto** | Autoritas AI — herramienta ARENA |
| **Ubicación** | Madrid, España |
| **Canal preferido** | LinkedIn DM + videollamada |
| **Perfil técnico** | Autodidacta con formación en electrónica. Background profesional en automoción (trabaja actualmente para Volvo). Lleva meses aprendiendo programación + IA. Usa Claude Code pero sin estructura de proyecto/CLAUDE.md. |
| **Web** | autoritas.ai (inferido del transcript — confirmar URL exacta) |

---

## 2. Sobre el producto (ARENA)

En palabras de Héctor: *"ARENA es un detector de riesgos en producción de agentes."*

ARENA es una infraestructura de validación de agentes conversacionales de IA antes de que salgan a producción. Resuelve un problema real y específico: los agentes desarrollados internamente funcionan bien en pruebas "amigables" del propio desarrollador, pero se rompen ante clientes reales exigentes o complejos.

**Cómo funciona:**
- Inyecta "clientes sintéticos hostiles" al agente: cliente indeciso, cliente monosílabo, cliente experto que cuestiona todo, cliente que exige descuentos, cliente que pide devoluciones fuera de política
- Una capa de "jueces" evalúa las respuestas del agente y detecta fallos: respuestas demasiado largas (fallo leve), alucinaciones, salidas de contexto, fallos críticos (ej: vender a menores, dar descuentos que erosionan margen)
- Los resultados se presentan por turnos de conversación: "en el turno 7 se excedió en las políticas — puedes corregirlo de esta manera"
- No genera el prompt corregido, pero señala exactamente dónde falla y da recomendaciones
- Tiene modo blackbox: se conecta vía HTTP endpoint sin necesidad de compartir el system prompt

**Tracción actual:**
- 46 desarrolladores probando la beta
- +300 tests realizados
- Lanzamiento público: 15 de abril 2026
- Validación positiva del prompt filtrado de Claude de Anthropic: 95/100

**Modelo de precios:**
- 1 test: €2,99 (incluye hasta 3 clientes sintéticos en paralelo, con media de resultados)
- Pack de 10: 🔲 precio no mencionado
- Plan mensual: €39/mes (máximo 50 tests)
- Free tier: 1 test gratuito disponible

**Stack técnico:**
- API de Anthropic (Claude) y/o OpenAI (intercambiable)
- Frontend + backend en repositorio GitHub
- Base de datos de conversaciones (no guarda system prompt ni datos de cliente)
- Compliant con regulación de datos UE (GDPR)
- API en desarrollo para integrar en workflows n8n / Make como "bloqueante de producción"

**Diferenciador clave:** No hay nada igual en el mercado. El concepto de "cliente incógnito sintético" aplicado a agentes de IA es original. La competencia en este momento es la arrogancia del desarrollador que dice "yo lo testeo solo".

---

## 3. Estado del proyecto / relación

| Aspecto | Estado |
|---------|--------|
| **Tipo de relación** | Peer — posible colaborador / tester / referido futuro |
| **Origen del contacto** | Post de LinkedIn de CreActive sobre Kitcha |
| **Reunión** | Primera reunión — 17 abril 2026 |
| **Servicios CreActive para Héctor** | Ninguno formal. Oscar ofreció: (1) feedback comercial de landing/LinkedIn, (2) testear agentes de Kitcha y Nutrisco con ARENA cuando estén listos |
| **Servicios de Héctor para CreActive** | Usar ARENA para testear agentes de Kitcha y Nutrisco antes de producción |
| **Modelo comercial** | 🔲 Pendiente definir — podría evolucionar a colaboración formal, referidos, o intersticio |

---

## 4. Identidad visual / marca

| Elemento | Estado |
|----------|--------|
| **Nombre producto** | ARENA |
| **Marca web** | Autoritas AI |
| **Colores** | 🔲 Pendiente revisar landing |
| **Estilo visual** | 🔲 Pendiente revisar landing |
| **Landing** | autoritas.ai — existe, Oscar la revisó brevemente en la llamada |

---

## 5. Feature request identificado (oportunidad de producto)

Oscar propuso a Héctor una idea de feature que podría cambiar el modelo de negocio de ARENA:

> **"Modo cliente incógnito externo"**: en lugar de requerir el system prompt del agente, ARENA se conectaría directamente al chat de una empresa (WhatsApp, widget web) y simularía una conversación real desde fuera, sin necesidad de acceso interno. Esto permitiría a Héctor llegar a empresas que ni siquiera saben que tienen el problema, hacer una auditoría no invasiva y presentarles los resultados como argumento de venta.

Héctor respondió: *"Si eso se lo pudiera desarrollar, me pasaría el fuego. Es un win to win."*

Limitación actual: implica complejidad técnica y potenciales problemas de políticas de privacidad.

---

## 6. Pendientes de CreActive hacia Héctor

| # | Pendiente | Urgencia | Para qué |
|---|-----------|----------|----------|
| 1 | Revisar landing de Autoritas AI y dar feedback comercial | 🟡 Media | Oscar lo ofreció en la llamada — esta semana |
| 2 | Revisar perfil de LinkedIn de Héctor y dar feedback | 🟡 Media | Oscar lo ofreció en la llamada — esta semana |
| 3 | Enviar link de Vexa AI (transcriptor self-hosted) por interno de LinkedIn | 🟢 Baja | Oscar lo prometió al cierre de la llamada |
| 4 | Testear agentes de Kitcha y Nutrisco con ARENA cuando tengan agente activo | 🟢 Baja | Cuando los agentes estén listos para producción |

---

## 7. Cómo comunicarse con Héctor

- **Tono:** muy cercano, informal, de igual a igual. Lenguaje de "hermano", directo, sin corporativo.
- **Jerga:** mezcla español de España con tecnicismos en inglés (system prompt, run, blackbox, endpoint, token, workflow). Nada de jerga latinoamericana que pueda sonar extraño.
- **Decisiones:** toma decisiones rápido, es ejecutivo, valora el feedback directo y accionable.
- **Seguimiento:** LinkedIn DM es el canal natural. No abusar. Con un mensaje bien escrito basta.
- **Vulnerabilidad:** reconoce que la parte comercial es su punto débil — ahí hay espacio para aportar valor real.

---

## 8. Notas internas

- Héctor trabaja de día en Volvo (automoción) y de noche construye ARENA. Solopreneur como Oscar.
- Síndrome del impostor presente: tardó meses en lanzar porque quería que "estuviera perfecto". Lo superó.
- Está llegando "muy pronto a la fiesta" — igual que CreActive. Hay mucha afinidad de situación y mentalidad.
- No usa estructura de CLAUDE.md / carpetas para trabajar con Claude Code. Oportunidad de aportar valor mostrándole el sistema de CreActive (ya se hizo en la llamada — le impactó positivamente).
- La base de datos que está construyendo (300+ conversaciones de test) puede convertirse en una ventaja competitiva enorme cuando el mercado de agentes explote.
- Posible ángulo de colaboración: CreActive recomienda ARENA a sus clientes que implementen agentes. Revenue share o referido simple.
- **Idea de contenido para ARENA:** documentar los casos raros — el prompt filtrado de Claude con 95/100, el agente de una tienda de cannabis que no detectó a un menor, etc. Eso vende solo.

---

*Generado por CreActive Studio — Abril 2026*
*Fuente: Reunión inicial con Héctor Partida Bazo — 17 abril 2026 (transcrito en `clientes/autoritas-ai/Transcritos/`)*
