# Patrones de Hormozi — Análisis Real del CSV

> Análisis de 671 posts de @hormozi en Threads.
> Fuente: `content-engine/carrusel/ideas/Threads hormozi.csv`
> Columnas: texto (hasta 3 segmentos), likes, replies, reposts, fecha.
>
> Este archivo se usa para informar el tono y estructura de posts de Threads de Oscar.
> NO es para copiar a Hormozi — es para entender qué estructuras generan distribución real.

---

## Datos del análisis

| Métrica | Valor |
|---------|-------|
| Total posts analizados | 671 |
| Post con más reposts | 827 (paradoja de tiempo) |
| Post con más likes | 10,500 ("Go to bed on time") |
| Post con más replies | 449 (challenge de 30 días) |
| Promedio reposts top 20 | ~470 |
| Promedio likes top 20 | ~4,900 |

---

## Top posts por reposts (distribución)

| Reposts | Likes | Post (resumido) |
|---------|-------|-----------------|
| 827 | 7,900 | "The sooner you accept that it's going to take longer than you want, the sooner it happens faster than you thought." |
| 689 | 10,500 | "How to avoid tons of problems in life: Go to bed on time." |
| 622 | 3,700 | "Normalize ignoring the opinions of people who have smaller dreams for your life than you do." |
| 572 | 4,900 | "The best way to identify a great friend is how they react when you win." |
| 558 | 5,500 | "Until you win, effort always goes unnoticed. Get used to it." |
| 506 | 4,100 | "You must first become consistent before you can become exceptional." |
| 487 | 4,400 | "You just have to be willing to look like an idiot while you figure it out. Because once you figure it out, no one remembers." |
| 478 | 4,300 | "The single greatest skill you can develop is the ability to stay in a great mood in the absence of things going well." |
| 473 | 4,200 | "Fastest way to change your life: Change who you're friends with." |
| 462 | 5,200 | "At your funeral, friends and family will argue over who gets your stuff. People will talk about the impact you had on their lives." |
| 424 | 5,400 | "If you have no money, you should have no shame. Knock. Call. Email. Text. DM. Ask." |
| 408 | 4,100 | "Money loves speed. Wealth loves time. Poverty loves indecision." |
| 407 | 3,600 | "Poor people stay poor because they're afraid of other poor people judging them for trying to get rich." |
| 392 | 4,700 | "Your 9-5 isn't killing your dreams. Wasting your 5-9 is." |
| 364 | 5,300 | "Elon Musk owns 20% of Tesla. Jeff Bezos owns 9% of Amazon. Jensen Huang owns 4% of NVIDIA." |

---

## Top posts por likes (resonancia)

| Likes | Reposts | Post (resumido) |
|-------|---------|-----------------|
| 10,500 | 689 | "How to avoid tons of problems in life: Go to bed on time." |
| 7,900 | 827 | "The sooner you accept that it's going to take longer..." |
| 5,500 | 558 | "Until you win, effort always goes unnoticed. Get used to it." |
| 5,400 | 424 | "If you have no money, you should have no shame. Knock. Call. Email..." |
| 5,300 | 364 | "Elon Musk owns 20% of Tesla. Jeff Bezos owns 9% of Amazon..." |
| 5,200 | 462 | "At your funeral, friends and family will argue over who gets your stuff." |
| 4,900 | 572 | "The best way to identify a great friend is how they react when you win." |
| 4,800 | 411 | "Dear younger me: The less a customer pays, the more problems they cause." |
| 4,700 | 392 | "Your 9-5 isn't killing your dreams. Wasting your 5-9 is." |
| 4,600 | 276 | "If you're poor, it makes sense to buy a suit and pretend you have money..." |

---

## Top posts por replies (conversación)

| Replies | Likes | Post (resumido) |
|---------|-------|-----------------|
| 449 | 3,600 | "If you're poor, try the 'buy nothing' challenge: For 30 days, buy nothing except food, rent, utilities..." |
| 414 | 2,400 | "If someone says 'that's not my job' they probably shouldn't do anything else at your company either." |
| 345 | 2,600 | "In the Bible, before God gave Adam a wife, he gave him a job. We're made to work." |
| 277 | 4,100 | "It's very hard to have a vision when you have bills to pay." |
| 275 | 4,700 | "Your 9-5 isn't killing your dreams. Wasting your 5-9 is." |
| 232 | 5,300 | "Elon Musk owns 20% of Tesla. Jeff Bezos owns 9% of Amazon." |
| 194 | 3,400 | "Controversial take: You will get more views, followers, and influence by not making content for years, and then posting something people actually care about." |
| 187 | 3,900 | "If your business isn't making $100,000 a month. Follow these 2 steps..." |
| 184 | 1,900 | "Next time prospects ghost you, instead of sending a generic message, try sending this." |
| 183 | 2,200 | "If you talk about 'work life balance' as a 22 year old man, you're hanging out with the wrong people." |

---

## 5 Patrones estructurales identificados

### Patrón 1 — La Verdad Simple
**Estructura:** 1-2 líneas. Observación directa. Sin explicación adicional.
**Métricas:** Máximos reposts y likes en relación al largo del post. La simpleza ES el mensaje.

**Ejemplos reales del CSV:**
- "How to avoid tons of problems in life: Go to bed on time." (10.5K likes, 689 reposts)
- "Focus is subtraction." (589 likes, 45 reposts)
- "Money loves speed. Wealth loves time. Poverty loves indecision." (4.1K likes, 408 reposts)
- "Fastest way to change your life: Change who you're friends with." (4.2K likes, 473 reposts)

**Mecánica:** El lector completa el pensamiento solo. La brevedad lo hace guardable e irresistible de repostear.

**Adaptación para Oscar (IA + sistemas + operaciones LatAm):**
- "El cliente que más te regatea es el que más problemas te da."
- "Un sistema malo que funciona vale más que un proceso perfecto que no existe."
- "La respuesta lenta le cuesta más que el precio alto."
- "Automatiza lo repetible. Humaniza lo que importa."
- "El negocio que no tiene sistema trabaja para el sistema del dueño."

---

### Patrón 2 — La Paradoja
**Estructura:** Setup que parece contradictorio → resolución que cambia el marco.
**Métricas:** Máximos reposts (827). Alto engagement porque genera "wow, no lo había pensado así."

**Ejemplos reales del CSV:**
- "The sooner you accept that it's going to take longer than you want, the sooner it happens faster than you thought." (7.9K likes, 827 reposts)
- "Your 9-5 isn't killing your dreams. Wasting your 5-9 is." (4.7K likes, 392 reposts)
- "The best way to identify a great friend is how they react when you win." (4.9K likes, 572 reposts)
- "Until you win, effort always goes unnoticed. Get used to it." (5.5K likes, 558 reposts)

**Mecánica:** "Pensabas que X era el problema. En realidad es Y." Genera la sensación de haber aprendido algo sin esfuerzo.

**Adaptación para Oscar:**
- "Cuanto antes aceptes que la automatización tarda en configurarse, más rápido deja de depender de ti."
- "Tu negocio no pierde clientes por el precio. Los pierde por la demora en responder."
- "No contrates más gente para escalar. Contrata mejores sistemas primero."
- "La IA no va a reemplazar tu negocio. Pero tu competidor que sí la usa, sí."

---

### Patrón 3 — El Reencuadre Social
**Estructura:** "Normalize X" o "El [grupo] que vale la pena es el que hace Y."
**Métricas:** Alto repost, medio-alto likes. Funciona porque la gente lo comparte para validarse.

**Ejemplos reales del CSV:**
- "Normalize ignoring the opinions of people who have smaller dreams for your life than you do." (3.7K likes, 622 reposts)
- "Better to have friends who force you to grow than ones who accept you as you are." (3.9K likes, 504 reposts)
- "Avoiding people who make it harder to achieve your goals is the highest form of self care." (3.5K likes, 419 reposts)
- "Dear younger me: The less a customer pays, the more problems they cause." (4.8K likes, 411 reposts)

**Mecánica:** El lector se reconoce (o quiere reconocerse) en el comportamiento descrito. Lo repostea para mostrar que pertenece a ese grupo.

**Adaptación para Oscar:**
- "Normaliza cobrar bien. Los clientes que no pueden pagarte tampoco van a valorar lo que entregas."
- "El cliente que te dice 'no tengo presupuesto' te está diciendo que no le duele suficiente el problema."
- "El proveedor que entrega y desaparece no es un socio. Es un freelancer."

---

### Patrón 4 — La Lista Con Fricción
**Estructura:** Condición → lista de acciones concretas numeradas o separadas por saltos de línea.
**Métricas:** Máximos replies (449). La lista invita a discutir o preguntar por items específicos.

**Ejemplos reales del CSV:**
- "If you have no money, you should have no shame. Knock. Call. Email. Text. DM. Ask." (5.4K likes, 424 reposts)
- "If you're poor, try the 'buy nothing' challenge: For 30 days, buy nothing except: 1) food 2) rent 3) utilities..." (3.6K likes, 449 replies)
- "If your business isn't making $100,000 a month. Follow these 2 steps. Grab a kitchen timer. Set it to 30 minutes..." (3.9K likes, 187 replies)
- "I built wealth without: 1) Reading a book a week 2) Making my bed 3) Journaling 4) 2 hour morning routines..." (4.2K likes)

**Mecánica:** La lista hace el contenido escaneable y accionable. El formato fuerza a la gente a leer hasta el final para ver todos los items.

**Adaptación para Oscar:**
```
Si tu negocio pierde clientes después del primer mes:
1. Revisa los primeros 3 mensajes que les mandaste.
2. Mide cuánto tardaste en responder la primera vez.
3. Mira si tienes algún sistema de seguimiento post-venta.

La mayoría no tiene ninguno de los tres.
```

```
Si quieres automatizar pero no sabes por dónde empezar:
- Anota qué haces más de 3 veces por semana.
- Marca lo que no necesita que un humano decida.
- Eso es lo que automatizas primero.
```

---

### Patrón 5 — La Verdad Incómoda
**Estructura:** Afirmación directa de algo que la audiencia sabe pero evita decir.
**Métricas:** Medio-alto reposts, muchos replies. Genera discusión porque divide.

**Ejemplos reales del CSV:**
- "If someone says 'that's not my job' they probably shouldn't do anything else at your company either." (2.4K likes, 414 replies)
- "If you talk about 'work life balance' as a 22 year old man, you're hanging out with the wrong people." (2.2K likes, 183 replies)
- "Controversial take: You will get more views, followers, and influence by not making content for years, and then posting something people actually care about." (3.4K likes, 194 replies)
- "It's very hard to have a vision when you have bills to pay." (4.1K likes, 277 replies)

**Mecánica:** El lector está de acuerdo o en desacuerdo fuerte. Ambas reacciones generan engagement. El post da permiso para decir algo que todos piensan pero nadie dice.

**Adaptación para Oscar:**
- "La mayoría de los negocios no tienen problemas de marketing. Tienen problemas de sistemas."
- "Si tienes que estar presente para que tu negocio funcione, no tienes un negocio. Tienes un trabajo."
- "Las agencias que prometen resultados en 30 días no saben lo que hacen o no te respetan lo suficiente para ser honestos."
- "La IA no va a hacer que tu negocio sea mejor. Va a hacer que tus procesos actuales sean más rápidos — buenos o malos."

---

## Observaciones adicionales del análisis

**Longitud óptima:**
- Posts de 1-3 líneas tienen el mayor ratio reposts/likes
- Posts de 5+ líneas (listas) tienen más replies
- Threads de 3-5 posts encadenados tienen engagement sostenido

**Timing:**
- Los posts duplicados en el CSV (mismo contenido, mismas métricas similares) sugieren que Hormozi repostea contenido que funcionó bien. Estrategia válida.

**Lo que NO funciona según los datos:**
- Posts muy técnicos con jerga específica (CAC, CRO, etc.) tienen métricas bajas a menos que el gancho sea muy claro
- Posts de más de 8 líneas sin estructura visible tienen bajo repost
- Posts sobre temas muy específicos de industria tienen alto reach concentrado pero bajo distribución general

---

## Instrucción de uso

Al generar posts de Threads para Oscar:
1. Elegir uno de los 5 patrones según el objetivo (distribución → Patrón 1 o 2; conversación → Patrón 4 o 5; validación social → Patrón 3)
2. Aplicar el patrón con tema de IA / automatización / operaciones / mindset de operador
3. Verificar contra voz.md: ¿suena a Oscar o a genérico?
4. Si el post tiene más de 4 líneas, revisar si la lista está bien formateada
5. Nunca agregar hashtags en Threads — Hormozi no los usa y sus métricas hablan por sí solas
