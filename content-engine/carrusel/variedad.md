# Tracker de Variedad — Carruseles CreActive Studio

> Este archivo es leído por `/cnt-carrusel` antes de generar cada nuevo carrusel.
> Se actualiza automáticamente después de cada generación.
> Mantener los últimos 5 registros para garantizar rotación efectiva.

---

## Log de carruseles (más reciente primero)

| # | Slug | Fecha | Pilar | Patrón hook | Hero start | Content-light en slide | Cierre |
|---|------|-------|-------|-------------|------------|------------------------|--------|
| 5 | claude-code-routines | 2026-04-14 | 4 — Construir sin equipo | Lista Con Fricción | hero-light | 4 | cta-light |
| 4 | avatares-ia-big-tech | 2026-04-10 | 2 — IA práctica para negocios LatAm | Verdad Simple | hero-dark | 2 | cta-light |
| 3 | china-ia-educacion | 2026-04-10 | 1 — Sistemas que trabajan solos | Reencuadre Social | hero-light | 3 | cta-light |
| 2 | chile-ia-llegar-tarde | 2026-04-10 | 3 — El operador vs el soñador | Verdad Incómoda | hero-dark | 4 | cta |
| 1 | claude-managed-agents | 2026-04-10 | 2 — Metodología | Paradoja | hero-dark | 3 | cta |

---

## Reglas de rotación (para cnt-carrusel)

### Pilar
No repetir el mismo pilar en los últimos **2** carruseles.
Secuencia objetivo: rotar entre los 5 pilares sin repetir 2 seguidos.

### Patrón hook (hero)
No repetir el mismo patrón en los últimos **3** carruseles.
Patrones disponibles: Verdad Simple · Paradoja · Reencuadre Social · Lista Con Fricción · Verdad Incómoda

### Content-light (slide claro)
Rotar la posición del `content-light` entre slides 2, 3 y 4.
Última posición usada: **2**
Próxima posición sugerida: **4**

### Hero start (alternación entre posts)
Cada carrusel nuevo alterna el color de inicio respecto al anterior.
- Si el anterior empezó con `hero-dark` → el siguiente usa `hero-light`
- Si el anterior empezó con `hero-light` → el siguiente usa `hero-dark`
Último hero start: **hero-light**
**Próximo hero start: hero-dark**

### Quote
Si el carrusel tiene más de 5 slides, incluir una slide `quote`.
No usar quote en carruseles de exactamente 4 slides.

---

## Estado actual del sistema

- **Total carruseles generados:** 5
- **Último pilar usado:** 4 — Construir sin equipo
- **Último patrón hook:** Lista Con Fricción
- **Último hero start:** hero-light
- **Última posición content-light:** slide 4
- **Próximo pilar sugerido:** cualquiera excepto Pilar 4 (preferir 1, 3 o 5 para variar)
- **Próximo patrón sugerido:** Verdad Simple o Paradoja (evitar Lista Con Fricción, Verdad Simple, Reencuadre Social)
- **Próximo hero start:** hero-dark
- **Próxima posición content-light:** slide 2

---

*Actualizar este archivo después de cada `/cnt-carrusel` ejecutado exitosamente.*
