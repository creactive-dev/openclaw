# /kitcha-import-pedidosya

Importa un restaurante a Kitcha desde cualquier fuente soportada. Acepta:
- Una **URL** de PedidosYa o Uber Eats → corre el scraper correcto automáticamente
- Un **archivo JSON** ya generado por cualquier scraper

El seed sigue exactamente el patrón de `supabase/migrations/20260421_seed_el_charakato.sql`.

---

## Uso

```
# Desde URL (corre el scraper automáticamente)
/kitcha-import-pedidosya https://www.ubereats.com/cl/store/restaurante/uuid
/kitcha-import-pedidosya https://www.pedidosya.cl/restaurantes/ciudad/restaurante-menu

# Desde JSON ya generado
/kitcha-import-pedidosya tools/hillfood_20260422_1427.json

# Sin argumento → usa el .json más reciente en tools/
/kitcha-import-pedidosya
```

---

## Instrucciones para Claude Code

### PASO 0 — Detectar tipo de input y obtener el JSON

Analizar el argumento recibido:

**Si el argumento empieza con `http`** (es una URL):
- Contiene `pedidosya` → ejecutar:
  ```bash
  cd /Users/oz/Documents/CAS-CEO/creactive-studio && python3 tools/pedidosya_scraper.py "{url}"
  ```
- Contiene `ubereats` → ejecutar:
  ```bash
  cd /Users/oz/Documents/CAS-CEO/creactive-studio && python3 tools/ubereats_scraper.py "{url}"
  ```
- El scraper imprime el nombre del archivo generado en stderr (`✅ JSON exportado: {archivo}.json`). Usar ese archivo como input del PASO 1.
- Si el scraper falla → mostrar el error y detenerse.

**Si el argumento es un path `.json`** → usarlo directamente en PASO 1.

**Sin argumento** → buscar el `.json` más reciente en `tools/` con:
```bash
ls -t /Users/oz/Documents/CAS-CEO/creactive-studio/tools/*.json | head -1
```

---

### PASO 1 — Leer el JSON

Leer el archivo JSON obtenido en PASO 0.

Extraer:
- `restaurante.nombre`
- `restaurante.slug`
- `restaurante.menu_source_url`
- `restaurante.telefono_whatsapp`
- `restaurante.color_primario`
- `restaurante.color_secundario`
- `categorias[]` → array con `nombre`, `orden`, `productos[]`
- `categorias[].productos[]` → `nombre`, `descripcion`, `precio` (int), `imagen_url`, `orden`
- `scraped_at`

Detectar fuente desde `menu_source_url`:
- Contiene `pedidosya` → `{fuente}` = `"PedidosYa"`
- Contiene `ubereats` → `{fuente}` = `"Uber Eats"`
- Otro → `{fuente}` = `"Scraper"`

---

### PASO 2 — Derivar el email del demo

El email se construye a partir del **nombre del restaurante** (no del slug):
- Lowercase
- Sin tildes (á→a, é→e, í→i, ó→o, ú→u, ñ→n, ü→u)
- Sin espacios ni caracteres especiales
- Append `@kitchat.cl`

Ejemplos:
- `"Hillfood"` → `hillfood@kitchat.cl`
- `"El Charakato"` → `elcharakato@kitchat.cl`
- `"Soli Sushi"` → `solisushi@kitchat.cl`

Mostrar resumen al usuario y pedir confirmación:

```
Restaurante:  {nombre}
Slug:         {slug}
Email demo:   {email}
Categorías:   {n}
Productos:    {total}

¿Continuar con este email? (o indica el email correcto)
```

---

### PASO 3 — Normalizar nombres de variables SQL

Para cada categoría, generar un nombre de variable SQL:
- Lowercase
- Sin tildes (á→a, é→e, í→i, ó→o, ú→u, ñ→n)
- Espacios y caracteres especiales → `_`
- Eliminar `(`, `)`, `/`, `-` y similares
- Truncar a 40 chars
- Prefix `v_cat_`

Ejemplos:
- `"Ensaladas"` → `v_cat_ensaladas`
- `"Aguas con sabores (sin gas)"` → `v_cat_aguas_con_sabores_sin_gas`
- `"Platos Fríos"` → `v_cat_platos_frios`

---

### PASO 4 — Generar el SQL

Generar el archivo completo siguiendo esta estructura:

```sql
-- ============================================================
-- SEED: {nombre}
-- Admin: {email}
-- WhatsApp: {telefono_whatsapp}
-- Slug: {slug}
-- Color: {color_primario}
-- Horario: 24h todos los días (demo)
-- Fuente: {fuente} — scraped {scraped_at}
--
-- PASOS ANTES DE EJECUTAR:
--   1. Crear usuario en Supabase Auth (ver comandos en PASO 6)
--   2. Ejecutar este seed.
--   3. Subir logo: UPDATE restaurantes SET logo_url = '...' WHERE slug = '{slug}';
-- ============================================================

DO $$
DECLARE
    v_user_id  uuid;
    v_rest     uuid;

    -- Categories ({n} total)
    v_cat_{var1}  uuid;
    v_cat_{var2}  uuid;
    ...

BEGIN
    -- ----------------------------------------------------------------
    -- 1. LOCATE USER + RESTAURANT
    -- ----------------------------------------------------------------
    SELECT id INTO v_user_id FROM auth.users WHERE email = '{email}';
    IF v_user_id IS NULL THEN
        RAISE EXCEPTION 'Usuario {email} no encontrado. Créalo en Supabase Auth → Admin API primero.';
    END IF;

    SELECT id INTO v_rest FROM restaurantes WHERE user_id = v_user_id;
    IF v_rest IS NULL THEN
        RAISE EXCEPTION 'Restaurante no encontrado. Verifica que el trigger on_auth_user_created se ejecutó.';
    END IF;

    RAISE NOTICE 'Restaurante encontrado: %', v_rest;

    -- ----------------------------------------------------------------
    -- 2. CONFIGURE RESTAURANT
    -- ----------------------------------------------------------------
    UPDATE restaurantes SET
        nombre            = '{nombre}',
        slug              = '{slug}',
        telefono_whatsapp = '{telefono_whatsapp}',
        menu_source_url   = '{menu_source_url}',
        config_marca      = jsonb_build_object(
                                'color_primario',   '{color_primario}',
                                'color_secundario', '{color_secundario}',
                                'tema',             'dark'
                            ),
        horarios_semana   = NULL,  -- NULL = siempre abierto en demo (useStoreStatus devuelve isOpen:true cuando es NULL)
        config_operaciones = jsonb_build_object(
            'delivery_active', false,
            'delivery_cost',   0,
            'pickup_time',     20,
            'delivery_time',   40,
            'min_order',       0,
            'metodos_pago',    jsonb_build_array('Efectivo'),
            'prep_time',       20
        ),
        onboarding_status = 'completado',
        is_active         = true
    WHERE id = v_rest;

    -- ----------------------------------------------------------------
    -- 3. CATEGORIES ({n} total)
    -- ----------------------------------------------------------------
    INSERT INTO categorias (restaurante_id, nombre, orden) VALUES
        (v_rest, 'Cat 1', 0),
        (v_rest, 'Cat 2', 1),
        ...
        (v_rest, 'Cat N', n);   -- última SIN coma

    SELECT id INTO v_cat_{var1} FROM categorias WHERE restaurante_id = v_rest AND nombre = 'Cat 1';
    SELECT id INTO v_cat_{var2} FROM categorias WHERE restaurante_id = v_rest AND nombre = 'Cat 2';
    ...

    -- ----------------------------------------------------------------
    -- 4. {NOMBRE CATEGORÍA EN MAYÚSCULAS} ({n} productos)
    -- ----------------------------------------------------------------
    INSERT INTO productos (restaurante_id, categoria_id, nombre, descripcion, imagen_url, precio, tags, disponible, orden)
    VALUES
        (v_rest, v_cat_{var1}, 'Producto 1', 'Descripción', 'https://...', 14600, ARRAY[]::text[], true, 0),
        (v_rest, v_cat_{var1}, 'Producto 2', '',             NULL,          12000, ARRAY[]::text[], true, 1);
        -- imagen vacía → NULL; descripción vacía → ''

    INSERT INTO variantes_producto (producto_id, nombre, precio, orden)
    SELECT p.id, 'Regular', p.precio, 1
    FROM productos p WHERE p.restaurante_id = v_rest AND p.categoria_id = v_cat_{var1};

    -- repetir para cada categoría...

    -- ----------------------------------------------------------------
    RAISE NOTICE 'Seed {nombre} completado. REST_ID: %', v_rest;
    RAISE NOTICE '{n} categorías | {total} productos | fuente: {fuente}';
    RAISE NOTICE 'Pendiente: logo → restaurant-assets/%/logo.png', v_rest;
END $$;
```

**Reglas de generación:**

1. `imagen_url` vacío (`""`) → `NULL` sin comillas
2. `descripcion` vacía → `''` (string vacío, no NULL)
3. Comillas simples en texto → duplicar (`O'Brien` → `O''Brien`)
4. `precio` siempre entero (ya viene así del JSON)
5. Último valor de cada `INSERT ... VALUES (...)` sin coma final
6. `variantes_producto` NO tiene columna `restaurante_id` — no incluirla jamás
7. `color_primario` y `color_secundario` vienen del JSON (no hardcodear)

---

### PASO 5 — Guardar el archivo

```
Proyectos Internos/white-cassini/supabase/migrations/YYYYMMDD_seed_{slug}.sql
```

`YYYYMMDD` = fecha de hoy.

---

### PASO 6 — Ejecutar los pasos automáticamente

Ejecutar en bash, **en este orden**, mostrando el output de cada paso:

**6A — Crear usuario en Supabase Auth:**

```bash
TOKEN=$(security find-generic-password -s "Supabase CLI" -a "supabase" -w | sed 's/go-keyring-base64://' | base64 -d)
SERVICE_KEY=$(curl -s "https://api.supabase.com/v1/projects/gjkaboosygjitxgqcawy/api-keys" \
  -H "Authorization: Bearer $TOKEN" | jq -r '.[] | select(.name=="service_role") | .api_key')
curl -s -X POST "https://gjkaboosygjitxgqcawy.supabase.co/auth/v1/admin/users" \
  -H "Authorization: Bearer $SERVICE_KEY" -H "apikey: $SERVICE_KEY" \
  -H "Content-Type: application/json" \
  -d '{"email":"{email}","email_confirm":true,"password":"TempPass2026!"}'
```

Si la respuesta contiene `"email":"{email}"` → usuario creado. Si contiene `"email address is already registered"` → el usuario ya existe, continuar igual.

**6B — Ejecutar el seed SQL:**

```bash
TOKEN=$(security find-generic-password -s "Supabase CLI" -a "supabase" -w | sed 's/go-keyring-base64://' | base64 -d)
jq -Rs '{"query": .}' < "Proyectos Internos/white-cassini/supabase/migrations/YYYYMMDD_seed_{slug}.sql" \
  | curl -s -X POST "https://api.supabase.com/v1/projects/gjkaboosygjitxgqcawy/database/query" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d @-
```

Si la respuesta contiene `"error"` → mostrar el error completo y detenerse.

**6C — Mostrar resumen final:**

```
✅ Demo Kitcha listo

Restaurante:  {nombre}
Fuente:       {fuente}
Admin:        https://admin.kitchat.cl  (login: {email} / TempPass2026!)
Customer:     https://white-cassini-sigma.vercel.app/?local={slug}

Pendiente: subir logo al bucket restaurant-assets/{rest_id}/logo.png
```

---

## Notas técnicas

- Supabase project ref white-cassini: `gjkaboosygjitxgqcawy`
- El trigger `on_auth_user_created` crea automáticamente el row en `restaurantes` al crear el usuario en Auth — por eso el seed busca por email, no inserta restaurante directamente
- `variantes_producto` no tiene columna `restaurante_id` — nunca incluirla
- El seed no crea zonas de delivery ni modificadores — demo simple intencional
- `horarios_semana = NULL` → el hook `useStoreStatus` devuelve `isOpen: true` inmediatamente, sin evaluar horarios
