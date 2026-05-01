#!/usr/bin/env python3
"""
PedidosYa Restaurant Scraper
Extrae información completa de un restaurante en PedidosYa y genera un JSON
estructurado listo para importar a Supabase (white-cassini / Kitcha).

Estrategia:
  1. Abre el navegador (modo visible) para bypassear la protección anti-bot de PedidosYa.
  2. Extrae el JSON-LD schema.org que PedidosYa embebe en el HTML — contiene todos
     los productos, precios, imágenes y categorías de forma estructurada.
  3. Genera un JSON anidado compatible con el schema de Supabase.

Uso:
    python3 pedidosya_scraper.py <url> [output.json]

Ejemplos:
    python3 pedidosya_scraper.py "https://www.pedidosya.cl/restaurantes/..." menu.json
    python3 pedidosya_scraper.py "https://www.pedidosya.cl/restaurantes/..."   # nombre automático
"""

import sys
import re
import json
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright


# ──────────────────────────────────────────────────────────────────────────────
# Defaults para campos no disponibles en el JSON-LD schema.org de PedidosYa

DEFAULT_TELEFONO = "+56 9 8271 7201"
DEFAULT_COLOR_PRIMARIO = "#D32F2F"
DEFAULT_COLOR_SECUNDARIO = "#B71C1C"
DEFAULT_TEMA = "dark"
DEFAULT_HORARIOS = {
    dia: {"apertura": "00:00", "cierre": "23:59"}
    for dia in ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
}


# ──────────────────────────────────────────────────────────────────────────────

def log(msg):
    print(f"  {msg}", file=sys.stderr)


def extract_restaurant_slug(url: str) -> str:
    parts = url.rstrip("/").split("/")
    slug = parts[-1].replace("-menu", "")
    slug = re.sub(r"-[0-9a-f]{8}-.*", "", slug)
    return slug or "restaurante"


def normalize_image_url(url: str) -> str:
    base = url.split("?")[0]
    return f"{base}?quality=90&width=1440&webp=1&dpi=1.5"


# ──────────────────────────────────────────────────────────────────────────────

def get_page_html(url: str, max_retries: int = 2) -> tuple[str, str]:
    """Abre el navegador en modo visible (bypass anti-bot) y retorna el HTML."""
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
                    "document.querySelector('script[type=\"application/ld+json\"]') !== null"
                    " && document.querySelector('script[type=\"application/ld+json\"]').textContent.includes('hasMenu')",
                    timeout=15_000,
                )
            except Exception:
                log("Advertencia: JSON-LD no detectado en 15s, intentando igual...")

            page.wait_for_timeout(2_000)

            html = page.content()
            page_text = page.inner_text("body")
            browser.close()

            # Detectar si el menú no cargó (bloqueo o error de red)
            if "No se pudo cargar el menú" in page_text or (
                "hasMenu" not in html and attempt < max_retries
            ):
                log("⚠️  Menú no cargó correctamente, reintentando...")
                continue

            return html, page_text

    raise RuntimeError(
        "PedidosYa bloqueó la carga del menú. "
        "Espera unos minutos y vuelve a intentarlo."
    )


def extract_schema_data(html: str) -> dict | None:
    """Extrae el JSON-LD schema.org Restaurant del HTML."""
    patterns = [
        r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>',
        r'<script[^>]*>({"@context":"http://schema\.org/"[^<]*)</script>',
    ]
    for pat in patterns:
        matches = re.findall(pat, html, re.DOTALL)
        for raw in matches:
            try:
                data = json.loads(raw.strip())
                if data.get("@type") == "Restaurant" and "hasMenu" in data:
                    return data
            except Exception:
                continue
    return None


def extract_delivery_info(page_text: str) -> dict:
    """Intenta extraer costo de envío y mínimo de pedido del texto de la página."""
    delivery_cost = "No disponible"
    minimum_order = "Sin mínimo"

    cost_match = re.search(r'\$([\d.,]+)\s*(?:de\s+)?env[íi]o', page_text, re.IGNORECASE)
    if not cost_match:
        cost_match = re.search(r'env[íi]o[:\s]+\$\s*([\d.,]+)', page_text, re.IGNORECASE)
    if cost_match:
        delivery_cost = f"CLP ${cost_match.group(1)}"

    min_match = re.search(r'm[íi]nimo[:\s]+([^\n]+)', page_text, re.IGNORECASE)
    if min_match:
        minimum_order = min_match.group(1).strip()

    return {"delivery_cost": delivery_cost, "minimum_order": minimum_order}


# ──────────────────────────────────────────────────────────────────────────────

def scrape(url: str) -> dict:
    html, page_text = get_page_html(url)

    log("Extrayendo JSON-LD schema.org...")
    schema = extract_schema_data(html)

    if not schema:
        raise RuntimeError(
            "No se encontró el JSON-LD del menú en el HTML. "
            "El sitio puede haber cambiado su estructura."
        )

    delivery_info = extract_delivery_info(page_text)

    # ── Parsear productos ──────────────────────────────────────────────────
    products = []
    categories = []

    for section in schema.get("hasMenu", {}).get("hasMenuSection", []):
        cat_name = section.get("name", "Sin categoría")
        categories.append(cat_name)

        for item in section.get("hasMenuItem", []):
            price_int = int(item.get("offers", {}).get("price", 0) or 0)
            image_url = normalize_image_url(item["image"]) if item.get("image") else ""

            products.append(
                {
                    "name": item.get("name", ""),
                    "description": item.get("description", ""),
                    "precio": price_int,
                    "image_url": image_url,
                    "category": cat_name,
                }
            )

    restaurant = {
        "name": schema.get("name", ""),
        "description": page_text.split("\n")[0] if page_text else "",
        "url": url,
        **delivery_info,
    }

    # Descripción más precisa desde meta og:description en HTML
    og_desc = re.search(r'property="og:description"\s+content="([^"]+)"', html)
    if og_desc:
        desc_text = og_desc.group(1)
        tipo_match = re.search(r'Ped[íi]\s+(.+?)\s+a\s+' + re.escape(restaurant["name"]), desc_text, re.IGNORECASE)
        if tipo_match:
            restaurant["description"] = tipo_match.group(1)
        else:
            restaurant["description"] = desc_text

    log(f"Restaurante: {restaurant['name']}")
    log(f"Productos: {len(products)} en {len(categories)} categorías")

    return {
        "restaurant": restaurant,
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
            "pedidosya_meta": {
                "delivery_cost_raw": r.get("delivery_cost"),
                "minimum_order_raw": r.get("minimum_order"),
                "description": r.get("description"),
            },
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
        print("Error: proporciona al menos una URL de PedidosYa.", file=sys.stderr)
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

        # Asegurar extensión .json
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
