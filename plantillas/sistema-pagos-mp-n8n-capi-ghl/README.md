# Sistema de Pagos — MercadoPago + n8n + Meta CAPI + GHL

> Plantilla reutilizable CreActive Studio  
> Construida y probada en: Pumpalcerro — Valle del Elqui (abril 2026)  
> Aplica a: landing pages con pago único, reservas, suscripciones, infoproductos

---

## Arquitectura del sistema

```
Usuario en landing
→ Formulario pre-pago (nombre / email / teléfono)
→ fbq('InitiateCheckout')                          ← pixel client-side
→ POST /api/lead
   ├── GHL Webhook A (crea contacto + oportunidad)
   └── MP Preferences API (crea preferencia dinámica con external_reference)
→ Redirect a MercadoPago (init_point de la preferencia)
→ Usuario paga
→ MP: redirect success → /gracias
   └── fbq('Purchase') client-side                 ← respaldo pixel
→ MP IPN → n8n (async, independiente del redirect)
   ├── GET /v1/payments/{id}                        ← obtiene detalle del pago
   ├── IF type == "payment" AND status == "approved"
   ├── Code node: SHA256(email) + SHA256(teléfono)
   ├── Meta Conversions API → evento Purchase       ← server-side (más confiable)
   └── GHL Webhook B (actualiza oportunidad + dispara correo)
```

**Por qué `external_reference`:** El email que el usuario escribe en el formulario (capturado en GHL) puede ser diferente al email que usa para pagar en MP. El campo `external_reference` de la preferencia de MP almacena el email del formulario y lo devuelve en el IPN — así GHL puede hacer match entre el contacto creado y el pago.

---

## Componentes

### 1. Next.js — `/api/lead/route.ts`

Recibe el formulario pre-pago, envía a GHL y crea la preferencia dinámica de MP.

```typescript
import { NextRequest, NextResponse } from 'next/server'

export async function POST(req: NextRequest) {
  const webhookUrl = process.env.GHL_WEBHOOK_URL
  const mpAccessToken = process.env.MP_ACCESS_TOKEN

  if (!webhookUrl) {
    return NextResponse.json({ error: 'Webhook not configured' }, { status: 500 })
  }

  const body = await req.json()
  const { name, email, phone, plan, price } = body

  if (!name || !email || !phone) {
    return NextResponse.json({ error: 'Missing required fields' }, { status: 400 })
  }

  // 1. Enviar a GHL (crea contacto + oportunidad "Interesado")
  const ghlRes = await fetch(webhookUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      name,
      email,
      phone,
      plan,
      price,
      source: 'landing-[NOMBRE-PRODUCTO]',   // ← personalizar
      timestamp: new Date().toISOString(),
    }),
  })

  if (!ghlRes.ok) {
    return NextResponse.json({ error: 'Webhook delivery failed' }, { status: 502 })
  }

  // 2. Crear preferencia dinámica en MP (si hay access token)
  if (mpAccessToken && price) {
    const mpRes = await fetch('https://api.mercadopago.com/checkout/preferences', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${mpAccessToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        items: [{
          id: '[ID-PRODUCTO]',               // ← personalizar, ej: 'valle-elqui-2026'
          title: `[NOMBRE PRODUCTO] — ${plan || 'Pago'}`,
          quantity: 1,
          currency_id: 'CLP',               // ← cambiar según país: ARS, MXN, COP, etc.
          unit_price: Number(price),
        }],
        payer: { name, email },
        external_reference: email,           // ← clave del sistema: email del formulario
        back_urls: {
          success: 'https://[DOMINIO]/gracias',
          failure: 'https://[DOMINIO]',
          pending: 'https://[DOMINIO]/gracias',
        },
        auto_return: 'approved',
        notification_url: 'https://[URL-N8N]/webhook/[PATH-WEBHOOK]',
      }),
    })

    if (mpRes.ok) {
      const mpData = await mpRes.json()
      return NextResponse.json({ ok: true, mp_url: mpData.init_point })
    }
  }

  // Fallback: sin preferencia dinámica
  return NextResponse.json({ ok: true })
}
```

**Variables de entorno requeridas:**

| Variable | Descripción |
|---|---|
| `GHL_WEBHOOK_URL` | Webhook GHL que crea contacto + oportunidad |
| `MP_ACCESS_TOKEN` | Access Token de producción de MercadoPago |
| `NEXT_PUBLIC_META_PIXEL_ID` | ID del pixel de Meta |

---

### 2. Next.js — `PaymentModal.tsx` (fragmento clave)

```typescript
const handleSubmit = useCallback(async (e: React.FormEvent) => {
  e.preventDefault()
  setStatus('sending')

  // Pixel client-side — InitiateCheckout
  if (typeof window !== 'undefined' && (window as any).fbq) {
    (window as any).fbq('track', 'InitiateCheckout')
  }

  try {
    const res = await fetch('/api/lead', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, phone, plan: planLabel, price }),
    })
    if (!res.ok) throw new Error('Failed')

    const data = await res.json()
    // Usa preferencia dinámica si existe, fallback a link estático
    window.location.href = data.mp_url || paymentUrl
  } catch {
    setStatus('error')
  }
}, [name, email, phone, planLabel, price, paymentUrl])
```

---

### 3. n8n — Workflow completo

Importar el JSON desde `plantillas/sistema-pagos-mp-n8n-capi-ghl/n8n-workflow-template.json`

**Nodos del workflow:**

| Nodo | Tipo | Función |
|---|---|---|
| MP IPN | Webhook (POST) | Recibe notificación async de MP |
| ¿Es un pago? | IF | Filtra `body.type == "payment"` |
| GET Pago MP | HTTP Request | `GET /v1/payments/{id}` con Access Token MP |
| ¿Pago aprobado? | IF | Filtra `status == "approved"` |
| Preparar payload | Code | SHA256 de email y teléfono |
| Meta CAPI — Purchase | HTTP Request | POST a Graph API con hashes |
| GHL — Pago confirmado | HTTP Request | POST a webhook GHL con datos del pago |

**Valores a reemplazar al importar:**
1. `GET Pago MP` → header `Authorization`: Access Token MP del cliente
2. `Meta CAPI — Purchase` → `access_token` en el body: token de Meta Events Manager
3. `GHL — Pago confirmado` → URL del nodo: webhook GHL de confirmación de pago

---

### 4. n8n — Code node "Preparar payload" (SHA256 puro JS)

> ⚠️ n8n sandboxea los Code nodes: `require('crypto')` y `crypto.subtle` están bloqueados.
> La única solución es SHA256 implementado en JavaScript puro.

```javascript
const p = $input.all()[0].json;

const email = (p.payer && p.payer.email ? p.payer.email : '').toLowerCase().trim();
const phone = (p.payer && p.payer.phone && p.payer.phone.number
  ? String(p.payer.phone.number) : '').replace(/\D/g, '');

function sha256(msg) {
  if (!msg) return '';
  const K=[0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2];
  let H=[0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19];
  const rr=(v,n)=>(v>>>n)|(v<<(32-n));
  const b=[];
  for(let i=0;i<msg.length;i++){const c=msg.charCodeAt(i);if(c<128)b.push(c);else if(c<2048)b.push((c>>6)|192,(c&63)|128);else b.push((c>>12)|224,((c>>6)&63)|128,(c&63)|128);}
  const L=b.length;
  b.push(0x80);
  while(b.length%64!==56)b.push(0);
  b.push(0,0,0,0,(L*8>>>24)&255,(L*8>>>16)&255,(L*8>>>8)&255,(L*8)&255);
  for(let i=0;i<b.length;i+=64){
    const W=new Array(64);
    for(let j=0;j<16;j++)W[j]=(b[i+j*4]<<24)|(b[i+j*4+1]<<16)|(b[i+j*4+2]<<8)|b[i+j*4+3];
    for(let j=16;j<64;j++){const s0=rr(W[j-15],7)^rr(W[j-15],18)^(W[j-15]>>>3);const s1=rr(W[j-2],17)^rr(W[j-2],19)^(W[j-2]>>>10);W[j]=(W[j-16]+s0+W[j-7]+s1)|0;}
    let a=H[0],bb=H[1],c=H[2],d=H[3],e=H[4],f=H[5],g=H[6],h=H[7];
    for(let j=0;j<64;j++){const S1=rr(e,6)^rr(e,11)^rr(e,25);const ch=(e&f)^(~e&g);const t1=(h+S1+ch+K[j]+W[j])|0;const S0=rr(a,2)^rr(a,13)^rr(a,22);const maj=(a&bb)^(a&c)^(bb&c);const t2=(S0+maj)|0;h=g;g=f;f=e;e=(d+t1)|0;d=c;c=bb;bb=a;a=(t1+t2)|0;}
    H[0]=(H[0]+a)|0;H[1]=(H[1]+bb)|0;H[2]=(H[2]+c)|0;H[3]=(H[3]+d)|0;
    H[4]=(H[4]+e)|0;H[5]=(H[5]+f)|0;H[6]=(H[6]+g)|0;H[7]=(H[7]+h)|0;
  }
  return H.map(v=>(v>>>0).toString(16).padStart(8,'0')).join('');
}

return [{ json: { ...p, em_hashed: sha256(email), ph_hashed: sha256(phone) } }];
```

**Output:** el objeto original de MP más `em_hashed` y `ph_hashed` — los nodos siguientes pueden acceder a todos los campos originales.

---

### 5. n8n — Meta CAPI node (body)

```javascript
={{ JSON.stringify({
  data: [{
    event_name: 'Purchase',
    event_time: Math.floor(new Date().getTime() / 1000),
    action_source: 'website',
    event_source_url: 'https://[DOMINIO]/gracias',
    user_data: {
      em: $json.em_hashed ? [$json.em_hashed] : [],
      ph: $json.ph_hashed ? [$json.ph_hashed] : []
    },
    custom_data: {
      currency: $json.currency_id || 'CLP',
      value: $json.transaction_amount || 0,
      content_ids: ['[ID-PRODUCTO]'],
      content_type: 'product'
    }
  }],
  // test_event_code: 'TEST_XXXXX',   ← descomentar solo al probar en Meta Events Manager
  access_token: '[META-CAPI-ACCESS-TOKEN]'
}) }}
```

> **Importante:** `em` y `ph` **deben** estar hasheados con SHA256 — Meta rechaza PII en texto plano (error `error_subcode: 2804017`).

---

### 6. n8n — GHL Pago confirmado node (body)

```javascript
={{ JSON.stringify({
  event: 'payment_confirmed',
  payment_id: $('Preparar payload').item.json.id || '',
  amount: $('Preparar payload').item.json.transaction_amount || 0,
  currency: $('Preparar payload').item.json.currency_id || 'CLP',
  payer_email: ($('Preparar payload').item.json.payer && $('Preparar payload').item.json.payer.email)
    ? $('Preparar payload').item.json.payer.email : '',
  payer_phone: ($('Preparar payload').item.json.payer && $('Preparar payload').item.json.payer.phone
    && $('Preparar payload').item.json.payer.phone.number)
    ? $('Preparar payload').item.json.payer.phone.number.toString() : '',
  external_reference: $('Preparar payload').item.json.external_reference || '',
  source: 'mercadopago',
  product: '[NOMBRE-PRODUCTO]'
}) }}
```

> **Por qué `$('Preparar payload').item.json` y no `$json`:** El nodo GHL está después de Meta CAPI. En n8n, `$json` = output del nodo inmediatamente anterior (= respuesta de Meta, no el pago). Referenciar por nombre de nodo evita este problema.

---

## Gotchas y lecciones aprendidas

### n8n Set node (typeVersion 3) no transforma datos
El nodo Set en algunos entornos Railway pasa los datos de entrada sin transformar. **Solución:** usar un Code node para transformaciones, o referenciar campos originales directamente por nombre de nodo: `$('NombreNodo').item.json.campo`.

### `JSON.stringify` silencia campos `undefined`
Si un campo no tiene valor y no tiene fallback, `JSON.stringify` lo elimina silenciosamente del JSON. **Regla:** todos los campos en el body deben tener `|| ''` o `|| 0` como fallback.

### SHA256 en n8n Code node
- `require('crypto')` → bloqueado por el task runner sandboxed
- `crypto.subtle` (Web Crypto API) → no disponible en el sandbox
- **Solución:** implementación SHA256 en JavaScript puro (ver nodo "Preparar payload" arriba)

### Cadena de datos en n8n
En un workflow lineal A → B → C:
- En el nodo C, `$json` = output de B (no de A)
- Para acceder al output de A desde C: `$('NombreNodoA').item.json`

### `event_time` en Meta CAPI
- Usar `Math.floor(new Date().getTime() / 1000)` directamente en la expresión
- No depender de `$json.event_time` desde un Set node (puede ser undefined)

### Test event code
- Agregar `test_event_code: 'TEST_XXXXX'` para probar en Meta Events Manager → "Probar eventos"
- El código se obtiene en: Meta Business → Events Manager → Pixel → Configuración → Probar eventos
- **Eliminar antes de producción**

### MP Preferences API bloquea requests desde curl local
Al intentar crear preferencias con `curl` desde la máquina local usando el Access Token de producción, MP devuelve `403 PolicyAgent / PA_UNAUTHORIZED_RESULT_FROM_POLICIES`. Las preferencias se crean correctamente cuando el request viene desde un servidor (Vercel, Railway). **Nunca probar la creación de preferencias con curl directo** — usar siempre la propia landing como punto de entrada.

### Preferencias dinámicas vs links estáticos
Los links estáticos de MP (`mpago.la/xxx`) no permiten `external_reference` ni `notification_url`. Las preferencias dinámicas vía API sí. **Usar preferencias dinámicas siempre** que se necesite IPN o tracking por usuario.

---

## Flujo de configuración para un proyecto nuevo

### Paso 1 — MercadoPago
1. Obtener Access Token de producción del cliente (MP Dashboard → Tu negocio → Credenciales)
2. Configurar `notification_url` con la URL del webhook n8n en la preferencia (se hace desde el código, no desde el dashboard)

### Paso 2 — n8n
1. Importar `n8n-workflow-template.json`
2. Reemplazar los 3 valores marcados:
   - Access Token MP en "GET Pago MP"
   - Access Token Meta CAPI en "Meta CAPI — Purchase"
   - URL webhook GHL en "GHL — Pago confirmado"
3. Activar el workflow
4. Copiar la URL del webhook (Webhook node → URL de producción)

### Paso 3 — Meta
1. Meta Business → Events Manager → Pixel → Configuración → Generar token de acceso
2. Guardar el token (se usa en n8n y opcionalmente en `/api/lead` si hay CAPI desde Next.js)

### Paso 4 — GHL
**Webhook A — Captura de lead (pre-pago):**
- Trigger: webhook entrante
- Acción: crear/actualizar contacto, crear oportunidad en pipeline con etapa "Interesado"

**Webhook B — Confirmación de pago:**
- Trigger: webhook entrante con `event == "payment_confirmed"`
- Acción: buscar contacto por `external_reference` (= email del formulario), mover oportunidad a "Pagó", agregar nota con `payment_id` y `amount`, disparar correo de confirmación

### Paso 5 — Vercel (si es Next.js)
Variables de entorno a configurar:
```
GHL_WEBHOOK_URL=https://services.leadconnectorhq.com/hooks/.../webhook-trigger/...
MP_ACCESS_TOKEN=APP_USR-...
NEXT_PUBLIC_META_PIXEL_ID=...
```

### Paso 6 — Test end-to-end
1. Cambiar precios a $1 CLP temporalmente en `lib/constants.ts`
2. Hacer el flujo completo: formulario → MP → pago
3. Verificar: redirect `/gracias` ✅, n8n Executions ✅, Meta Events ✅, GHL actualizado ✅
4. Reembolsar desde MP Dashboard
5. Restaurar precios reales y hacer deploy final

---

## Estructura de archivos en un proyecto

```
clientes/[slug]/outputs/[nombre]-landing/
├── app/
│   ├── api/
│   │   └── lead/
│   │       └── route.ts          ← API route principal
│   ├── gracias/
│   │   └── page.tsx              ← página post-pago con fbq Purchase
│   └── page.tsx
├── components/
│   └── ui/
│       └── PaymentModal.tsx      ← modal pre-pago
├── lib/
│   └── constants.ts              ← precios, links de fallback, config
└── .env.local                    ← NO subir a git

clientes/[slug]/outputs/
└── n8n-workflow-[slug].json      ← workflow importable a n8n
```

---

## Campos que llegan a GHL en cada webhook

### Webhook A — Lead pre-pago
```json
{
  "name": "María López",
  "email": "maria@email.com",
  "phone": "+56912345678",
  "plan": "Reserva — Débito/Transferencia",
  "price": 200000,
  "source": "landing-[producto]",
  "timestamp": "2026-04-08T18:00:00.000Z"
}
```

### Webhook B — Pago confirmado
```json
{
  "event": "payment_confirmed",
  "payment_id": "123456789",
  "amount": 200000,
  "currency": "CLP",
  "payer_email": "maria@email.com",
  "payer_phone": "56912345678",
  "external_reference": "maria@email.com",
  "source": "mercadopago",
  "product": "[Nombre del producto]"
}
```

> `external_reference` = email del formulario pre-pago. Permite hacer match aunque `payer_email` sea diferente.

---

## Aplicabilidad a otros casos de uso

| Caso | Adaptación necesaria |
|---|---|
| **Suscripción mensual** | Usar MP Subscriptions API en lugar de Preferences; el IPN es similar |
| **Infoproducto (ebook, curso)** | Sin cambios en el flujo; ajustar `content_ids` en CAPI |
| **Evento / taller** | Agregar campo `event_date` en el payload GHL |
| **Multi-país** | Cambiar `currency_id` (ARS, MXN, COP, etc.); el Access Token cambia por cuenta MP |
| **Sin GHL** | Reemplazar webhooks GHL por cualquier otro CRM o base de datos |
| **Sin Meta Pixel** | Eliminar el nodo Meta CAPI del workflow n8n |

---

*Creado por CreActive Studio — Abril 2026*  
*Primer caso de uso: Pumpalcerro — Valle del Elqui 2026*
