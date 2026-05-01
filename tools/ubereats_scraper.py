#!/usr/bin/env python3
"""
Uber Eats Restaurant Scraper
Extrae información completa de un restaurante en Uber Eats y genera un JSON
estructurado listo para importar a Supabase (white-cassini / Kitcha).

Estrategia:
  1. Abre el navegador (modo visible) para bypassear la protección anti-bot.
  2. Extrae el JSON-LD schema.org embebido en el HTML (mismo formato que PedidosYa)
     — contiene nombre, categorías, productos y precios.
  3. Intenta enriquecer con imágenes desde __REACT_QUERY_STATE__ (SSR de Uber Eats).
  4. Genera un JSON anidado compatible con el schema de Supabase.

Uso:
    python3 ubereats_scraper.py <url> [output.json]

Ejemplos:
    python3 ubereats_scraper.py "https://www.ubereats.com/cl/store/al-dente.../uuid" menu.json
    python3 ubereats_scraper.py "https://www.ubereats.com/cl/store/..."   # nombre automático
"""

import sys
import re
import json
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright


# ──────────────────────────────────────────────────────────────────────────────

DEFAULT_TELEFONO = "+56 9 8271 7201"
DEFAULT_COLOR_PRIMARIO = "#06C167"   # verde Uber Eats
DEFAULT_COLOR_SECUNDARIO = "#05A659"
DEFAULT_TEMA = "dark"
DEFAULT_HORARIOS = {
    dia: {"apertura": "00:00", "cierre": "23:59"}
    for dia in ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
}


# ──────────────────────────────────────────────────────────────────────────────

def log(msg):
    print(f"  {msg}", file=sys.stderr)


def extract_restaurant_slug(url: str) -> str:
    # URL: https://www.ubereats.com/cl/store/{name-slug}/{uuid}
    parts = url.rstrip("/").split("/")
    for i, part in enumerate(parts):
        if part == "store" and i + 1 < len(parts):
            return parts[i + 1]
    return parts[-2] if len(parts) >= 2 else parts[-1] or "restaurante"


# ──────────────────────────────────────────────────────────────────────────────

def get_page_data(url: str, max_retries: int = 2) -> tuple[str, dict]:
    """Abre el navegador, espera el JSON-LD, hace scroll y retorna (html, image_index)."""
    for attempt in range(1, max_retries + 1):
        if attempt > 1:
            log(f"Reintento {attempt}/{max_retries} (esperando 5s)...")
            import time; time.sleep(5)

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=False,
                args=["--disable-blink-features=AutomationControlled"],
            )
            context = browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                ),
                viewport={"width": 1440, "height": 900},
                locale="es-CL",
            )
            context.add_init_script(
                "Object.defineProperty(navigator, 'webdriver', { get: () => undefined });"
            )
            page = context.new_page()

            log(f"Navegando a: {url}")
            page.goto(url, wait_until="domcontentloaded", timeout=60_000)

            # Esperar a que el JSON-LD del menú esté en el DOM
            try:
                page.wait_for_function(
                    """document.querySelector('script[type="application/ld+json"]') !== null"""
                    """ && Array.from(document.querySelectorAll('script[type="application/ld+json"]'))"""
                    """.some(s => s.textContent.includes('hasMenu'))""",
                    timeout=15_000,
                )
            except Exception:
                log("Advertencia: JSON-LD no detectado en 15s, intentando igual...")

            page.wait_for_timeout(2_000)

            # Esperar que React renderice al menos un item del menú
            try:
                page.wait_for_selector('[data-testid="item-image"]', timeout=10_000)
            except Exception:
                log("Advertencia: items del menú no visibles todavía, scrolleando igual...")

            # Scroll lento para activar lazy loading de imágenes
            log("Scrolleando para cargar imágenes lazy...")
            total_height = page.evaluate("document.body.scrollHeight")
            for pos in range(0, total_height + 400, 300):
                page.evaluate(f"window.scrollTo(0, {pos})")
                page.wait_for_timeout(250)
            page.wait_for_timeout(2_500)

            html = page.content()

            # Extraer imágenes desde el DOM renderizado.
            # Cada item del menú tiene data-testid="store-item-{uuid}" como contenedor;
            # el <img> dentro tiene alt = nombre del producto y src = URL de la imagen.
            image_index: dict = {}
            try:
                raw_images = page.evaluate("""() => {
                    const out = {};
                    // Selector principal: contenedores store-item-{uuid}
                    document.querySelectorAll('[data-testid^="store-item-"] img').forEach(img => {
                        const name = (img.alt || '').trim().toLowerCase();
                        const src  = img.src || '';
                        if (name && src && src.includes('tb-static')) out[name] = src;
                    });
                    // Fallback: contenedor item-image (sección de favoritos)
                    document.querySelectorAll('[data-testid="item-image"] img').forEach(img => {
                        const name = (img.alt || '').trim().toLowerCase();
                        const src  = img.src || '';
                        if (name && src && src.includes('tb-static') && !out[name]) out[name] = src;
                    });
                    return out;
                }""")
                image_index = raw_images or {}
                log(f"Imágenes capturadas del DOM: {len(image_index)}")
            except Exception as e:
                log(f"No se pudieron extraer imágenes del DOM: {e}")

            browser.close()

            if "hasMenu" not in html and attempt < max_retries:
                log("⚠️  Menú no cargó correctamente, reintentando...")
                continue

            return html, image_index

    raise RuntimeError(
        "Uber Eats bloqueó la carga del menú. "
        "Espera unos minutos y vuelve a intentarlo."
    )


def extract_schema_data(html: str) -> dict | None:
    """Extrae el JSON-LD schema.org Restaurant con hasMenu del HTML."""
    pattern = r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>'
    for raw in re.findall(pattern, html, re.DOTALL):
        try:
            data = json.loads(raw.strip())
            if data.get("@type") == "Restaurant" and "hasMenu" in data:
                return data
        except Exception:
            continue
    return None


# ──────────────────────────────────────────────────────────────────────────────

def scrape(url: str) -> dict:
    html, image_index = get_page_data(url)

    log("Extrayendo JSON-LD schema.org...")
    schema = extract_schema_data(html)

    if not schema:
        raise RuntimeError(
            "No se encontró el JSON-LD del menú en el HTML. "
            "El sitio puede haber cambiado su estructura."
        )

    products = []
    categories = []

    for section in schema.get("hasMenu", {}).get("hasMenuSection", []):
        cat_name = section.get("name", "").strip()
        items = section.get("hasMenuItem", [])
        if not cat_name or not items:
            continue
        categories.append(cat_name)

        for item in items:
            raw_price = item.get("offers", {}).get("price", 0)
            price = int(float(raw_price)) if raw_price else 0

            name = item.get("name", "")
            # Buscar imagen: primero en el item mismo, luego en el índice RQS
            image_url = item.get("image", "") or image_index.get(name.strip().lower(), "")

            products.append(
                {
                    "name": name,
                    "description": item.get("description", ""),
                    "precio": price,
                    "image_url": image_url,
                    "category": cat_name,
                }
            )

    restaurant_name = schema.get("name", "")

    log(f"Restaurante: {restaurant_name}")
    log(f"Productos:   {len(products)} en {len(categories)} categorías")

    return {
        "restaurant": {"name": restaurant_name, "url": url},
        "products": products,
        "categories": categories,
        "url": url,
        "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }


# ──────────────────────────────────────────────────────────────────────────────

def to_json(data: dict) -> str:
    """Genera JSON estructurado compatible con el schema de Supabase (white-cassini)."""
    by_category: dict[str, list] = {}
    for p in data["products"]:
        by_category.setdefault(p["category"], []).append(p)

    categorias = []
    for i, cat_name in enumerate(data["categories"]):
        productos = [
            {
                "nombre": p["name"],
                "descripcion": p["description"],
                "precio": p["precio"],
                "imagen_url": p["image_url"],
                "orden": j,
            }
            for j, p in enumerate(by_category.get(cat_name, []))
        ]
        categorias.append({"nombre": cat_name, "orden": i, "productos": productos})

    r = data["restaurant"]
    payload = {
        "restaurante": {
            "nombre": r["name"],
            "slug": extract_restaurant_slug(data["url"]),
            "menu_source_url": data["url"],
            "telefono_whatsapp": DEFAULT_TELEFONO,
            "color_primario": DEFAULT_COLOR_PRIMARIO,
            "color_secundario": DEFAULT_COLOR_SECUNDARIO,
            "tema": DEFAULT_TEMA,
            "horarios_semana": DEFAULT_HORARIOS,
            "ubereats_meta": {},
        },
        "categorias": categorias,
        "scraped_at": data["scraped_at"],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


# ──────────────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    urls = [a for a in args if a.startswith("http")]
    non_urls = [a for a in args if not a.startswith("http") and not a.startswith("-")]
    output_path = non_urls[0] if non_urls else None

    if not urls:
        print("Error: proporciona al menos una URL de Uber Eats.", file=sys.stderr)
        sys.exit(1)

    for url in urls:
        slug = extract_restaurant_slug(url)
        print(f"\n{'='*60}", file=sys.stderr)
        print(f"Restaurante: {slug}", file=sys.stderr)
        print(f"{'='*60}", file=sys.stderr)

        try:
            data = scrape(url)
        except Exception as e:
            print(f"\n❌ Error: {e}", file=sys.stderr)
            sys.exit(1)

        out_file = output_path or f"{slug}_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        if not out_file.endswith(".json"):
            out_file = out_file.rsplit(".", 1)[0] + ".json"

        Path(out_file).write_text(to_json(data), encoding="utf-8")

        p_count = len(data["products"])
        cats = ", ".join(data["categories"])
        print(f"\n✅ JSON exportado: {out_file}", file=sys.stderr)
        print(f"   Productos:  {p_count}", file=sys.stderr)
        print(f"   Categorías: {cats}", file=sys.stderr)


if __name__ == "__main__":
    main()
