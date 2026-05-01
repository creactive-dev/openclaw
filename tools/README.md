# Tools — CreActive Studio

Scripts de utilidad para operaciones del Agency OS.

## Scrapers de menú

### `pedidosya_scraper.py`
Extrae el menú de un restaurante desde PedidosYa y genera un JSON compatible con el importador de KitChat.

**Uso:**
```bash
python pedidosya_scraper.py <url-restaurante-pedidosya>
```
**Output:** JSON en `scraper-output/` con nombre `{slug}_{YYYYMMDD_HHMM}.json`
**Requiere:** `pip install requests beautifulsoup4 selenium`

---

### `ubereats_scraper.py`
Mismo flujo para Uber Eats.

**Uso:**
```bash
python ubereats_scraper.py <url-restaurante-ubereats>
```

---

## Slash command relacionado

`/kitcha-import-pedidosya <url>` — invoca el scraper automáticamente y genera el SQL de seed para KitChat.
