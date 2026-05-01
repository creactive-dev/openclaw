# Template GHL — Kit de Captura Exponor 2026

> Guía de setup interno para replicar en cada sub-cuenta de cliente.
> Tiempo estimado por cliente: 2-3 horas.

---

## 1. Crear Sub-Cuenta en GHL

1. GHL Agency → **Sub Accounts** → **+ Create Sub Account**
2. Nombre: `[Empresa] — Exponor 2026`
3. Correo de contacto: email principal del cliente
4. Timezone: `America/Santiago`

---

## 2. Pipeline "Exponor 2026"

**Settings → Pipelines → + Add Pipeline**

Nombre: `Exponor 2026`

### Etapas (en orden):

| # | Etapa | Color | Descripción |
|---|-------|-------|-------------|
| 1 | **Capturado en Stand** | Azul | Formulario enviado durante el evento |
| 2 | **Contactado** | Amarillo | Primer email de nurturing enviado |
| 3 | **Interesado** | Naranja | Abrió emails / respondió / visitó web |
| 4 | **En Conversación** | Morado | Respondió o agendó llamada |
| 5 | **Cerrado ✓** | Verde | Cliente convertido |
| 6 | **Sin Interés** | Gris | Marcado como frío, no seguir |

---

## 3. Campos Custom del Contacto

**Settings → Custom Fields → + Add Field**

Agregar los siguientes campos (tipo Contact):

| Campo | Tipo | Obligatorio |
|-------|------|-------------|
| `exponor_empresa` | Text | Sí |
| `exponor_cargo` | Text | No |
| `exponor_necesidad` | Textarea | No |
| `exponor_stand_visitado` | Text | No (pre-fill con stand del expositor) |
| `exponor_fecha_contacto` | Date | Auto |

---

## 4. Formulario de Captura (Survey / Form)

**Sites → Forms → + Add Form**

### Configuración:
- Nombre: `Captura Stand Exponor — [Empresa]`
- Tema: personalizar con logo del cliente (subir imagen)
- URL slug: `exponor-[empresa-slug]` (ej: `exponor-bekaert`)

### Campos del formulario:

```
1. Nombre completo *           → First Name + Last Name
2. Empresa *                   → Company Name
3. Cargo / Rol                 → exponor_cargo
4. Teléfono *                  → Phone
5. Email de trabajo            → Email
6. ¿Qué los trajo a Exponor?   → exponor_necesidad (Textarea)
   Placeholder: "Ej: Buscamos proveedor de X, evaluando opciones de Y..."
```

### Página de confirmación:
```
Título: "¡Gracias por registrarse!"
Mensaje: "Recibirá un correo de confirmación en los próximos minutos. 
          En los días siguientes estaremos en contacto con información 
          de nuestros productos y próximos pasos."
```

### Webhook / Automation trigger:
- Al enviar el formulario → crear/actualizar contacto → agregar al pipeline en etapa "Capturado en Stand"

---

## 5. Automation — Nurturing Post-Evento

**Automations → + Create Workflow**

Nombre: `Exponor 2026 — Nurturing Post-Evento`

### Trigger:
- **Contact Tag Added** → tag: `exponor-2026`
- O bien: **Pipeline Stage Changed** → Etapa: "Capturado en Stand"

### Secuencia:

---

**EMAIL 1 — Día 0 (inmediato o al día siguiente del evento)**

Asunto: `Fue un gusto conocerlos en Exponor, {{contact.first_name}}`

```
Hola {{contact.first_name}},

Gracias por pasar por nuestro stand en Exponor.

Fue un placer conversar sobre {{exponor_necesidad | "sus necesidades"}}. 
Queremos asegurarnos de darle el seguimiento que merece.

En los próximos días le compartiremos información específica sobre 
cómo [EMPRESA] puede ayudar a [DESCRIBIR SOLUCIÓN EN 1 LÍNEA].

Mientras tanto, si tiene alguna pregunta, estamos disponibles en:
📧 [email@empresa.cl]
📱 [+56 9 XXXX XXXX]

[NOMBRE REPRESENTANTE]
[EMPRESA]
```

---

**EMAIL 2 — Día 3**

Asunto: `{{contact.first_name}}, esto puede ser relevante para {{contact.company_name}}`

```
Hola {{contact.first_name}},

Mencionó en Exponor que {{exponor_necesidad | "estaban evaluando opciones"}}.

[INSERTAR: 1 caso de éxito o dato relevante del cliente similar]

¿Tiene 15 minutos esta semana para conversar en detalle?

[Link de calendario o teléfono directo]

[NOMBRE]
[EMPRESA]
```

---

**EMAIL 3 — Día 10**

Asunto: `Seguimiento — ¿podemos ayudarle con {{exponor_necesidad | "lo que conversamos"}}?`

```
Hola {{contact.first_name}},

Solo confirmar que recibió nuestros mensajes anteriores.

Entendemos que post-feria el día a día se acumula. Si el momento 
no es el indicado, sin problema — quedamos disponibles cuando sea conveniente.

Si sí hay interés en continuar la conversación, puede agendar 
directamente aquí: [link calendario]

[NOMBRE]
[EMPRESA]
```

---

**EMAIL 4 — Día 21**

Asunto: `Cerrando el loop — Exponor 2026`

```
Hola {{contact.first_name}},

Último mensaje de nuestra parte por este canal.

Si en algún momento necesitan [SOLUCIÓN DE LA EMPRESA], 
nos pueden encontrar en [web] o escribirnos directo a [email/WhatsApp].

Fue un placer conocerlos en Exponor. Éxito en los proyectos que vienen.

[NOMBRE]
[EMPRESA]
```

---

### Tags a aplicar automáticamente:
- Al crear: `exponor-2026`, `feria`, `[año]`
- Si abre Email 1: `exponor-activo`
- Si responde cualquier email: `exponor-caliente` → mover a etapa "En Conversación"
- Si no abre ningún email en 21 días: `exponor-frio` → mover a etapa "Sin Interés"

---

## 6. QR Code

Generar en: https://qr.io o https://www.qr-code-generator.com

- **URL:** link al formulario del cliente en GHL
- **Tamaño mínimo impresión:** 5cm × 5cm
- **Formato:** PNG transparente + SVG para impresión grande
- **Incluir en:** roll-up del stand, counter, tarjetas del equipo, presentaciones

---

## 7. Checklist de entrega al cliente

Antes de marcar como entregado, verificar:

- [ ] Sub-cuenta creada con nombre correcto
- [ ] Pipeline "Exponor 2026" con 6 etapas
- [ ] Campos custom creados y mapeados al formulario
- [ ] Formulario publicado y accesible vía URL
- [ ] QR code apunta al formulario correcto (testear con celular)
- [ ] Automation activa y testeada (enviar formulario de prueba → verificar que llegó al pipeline y disparó Email 1)
- [ ] Logo del cliente subido al formulario
- [ ] Correo de confirmación personalizado con nombre empresa
- [ ] Credenciales de acceso entregadas al cliente (si aplica)
- [ ] Documento de instrucciones enviado al cliente (cómo usar el QR en el stand)

---

## 8. Upsell post-evento (conversación para julio)

Una vez terminado Exponor, agendar una llamada de revisión con el cliente:

- ¿Cuántos contactos capturaron?
- ¿Qué emails tuvieron mejor apertura?
- ¿Cuántos leads se convirtieron en conversación?

**Propuesta de continuidad:** $150 USD/mes — gestión del pipeline, seguimiento personalizado a contactos calientes, reporte mensual.

---

*Template interno CreActive Studio — actualizar con cada iteración del producto.*
