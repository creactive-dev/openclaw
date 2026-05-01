# ============================================================
# Enriquecedor de emails - Exponor
# Requiere: pip install requests beautifulsoup4 openpyxl pandas
#
# Uso:
#   1. Pon este script en la misma carpeta que el Excel
#   2. Cambia ARCHIVO_EXCEL al nombre de tu archivo
#   3. Corre: python enriquecer_exponor.py
# ============================================================

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time
import random
from urllib.parse import urljoin, urlparse

ARCHIVO_EXCEL = "Exponor_Emails_Limpios.xlsx"
ARCHIVO_SALIDA = "Exponor_Emails_Enriquecido.xlsx"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'es-CL,es;q=0.9,en;q=0.8',
}

EMAIL_RE = re.compile(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}')

PALABRAS_SPAM = [
    'example', 'noreply', 'no-reply', 'domain', 'sentry', 'wixpress',
    'yourdomain', 'test@', 'support@wix', '@example.com',
    '.png', '.jpg', '.gif', '.svg', '.webp'
]

RUTAS_CONTACTO = [
    '/contacto', '/contact', '/contactenos', '/contactar',
    '/nosotros/contacto', '/quienes-somos', '/about/contact'
]

# ------------------------------------------------------------------

def normalizar_url(url):
    url = url.strip().rstrip('/')
    if not url.startswith('http'):
        url = 'https://' + url
    return url

def es_email_valido(email):
    email = email.lower()
    if any(s in email for s in PALABRAS_SPAM):
        return False
    partes = email.split('@')
    if len(partes) != 2:
        return False
    dominio = partes[1]
    if '.' not in dominio or len(dominio) < 4:
        return False
    return True

def obtener_dominio(url):
    return urlparse(url).netloc.replace('www.', '')

def extraer_emails(html, dominio_empresa=None):
    soup = BeautifulSoup(html, 'html.parser')
    emails = []

    # 1. Links mailto: (más confiable)
    for a in soup.find_all('a', href=True):
        if a['href'].startswith('mailto:'):
            email = a['href'].replace('mailto:', '').split('?')[0].strip().lower()
            if email and es_email_valido(email) and email not in emails:
                emails.append(email)

    # 2. Regex en texto visible
    for e in EMAIL_RE.findall(soup.get_text()):
        e = e.lower().strip('.,;:')
        if es_email_valido(e) and e not in emails:
            emails.append(e)

    # 3. Regex en HTML crudo (captura algunos ofuscados)
    for e in EMAIL_RE.findall(html):
        e = e.lower().strip('.,;:')
        if es_email_valido(e) and e not in emails:
            emails.append(e)

    # Preferir emails del dominio de la empresa
    if dominio_empresa and emails:
        dominio_limpio = dominio_empresa.replace('www.', '')
        emails_dominio = [e for e in emails if dominio_limpio in e]
        if emails_dominio:
            return emails_dominio

    return list(dict.fromkeys(emails))

def fetch(url, timeout=10):
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        if r.status_code == 200:
            return r.text
    except Exception:
        pass
    return None

def scrape_empresa(raw_url):
    url = normalizar_url(raw_url)
    dominio = obtener_dominio(url)
    todos_emails = []

    # Página principal
    html = fetch(url)
    if html:
        emails = extraer_emails(html, dominio)
        todos_emails.extend(emails)

    # Si no encontró nada, probar páginas de contacto
    if not todos_emails:
        base = normalizar_url(raw_url)
        for ruta in RUTAS_CONTACTO:
            url_contacto = base + ruta
            html2 = fetch(url_contacto, timeout=7)
            if html2:
                emails2 = extraer_emails(html2, dominio)
                if emails2:
                    todos_emails.extend(emails2)
                    break
            time.sleep(0.4)

    return list(dict.fromkeys(todos_emails))

# ------------------------------------------------------------------

def main():
    print(f"Cargando {ARCHIVO_EXCEL}...")
    df = pd.read_excel(ARCHIVO_EXCEL)
    email_cols = [c for c in df.columns if c.startswith('Email_')]
    df['_n_emails'] = df[email_cols].notna().sum(axis=1)

    # Empresas con sitio web y sin emails
    mask = (df['Sitio Web'] != 'No encontrado') & (df['_n_emails'] == 0)
    targets = df[mask]
    print(f"Empresas a procesar: {len(targets)} (tienen sitio web pero sin email)\n")

    resultados = {}
    encontrados = 0

    for i, (idx, row) in enumerate(targets.iterrows()):
        empresa = row['Empresa']
        sitio = row['Sitio Web']

        print(f"[{i+1}/{len(targets)}] {empresa[:45]:<45}", end=' -> ', flush=True)
        emails = scrape_empresa(sitio)
        resultados[idx] = emails

        if emails:
            encontrados += 1
            print(f"✓ {', '.join(emails[:3])}")
        else:
            print("—")

        time.sleep(random.uniform(1.0, 2.0))

    print(f"\n✓ Empresas con emails nuevos: {encontrados}/{len(targets)}")

    # Agregar al dataframe
    total_nuevos = 0
    for idx, nuevos_emails in resultados.items():
        if not nuevos_emails:
            continue
        existentes = [str(df.at[idx, c]) for c in email_cols if pd.notna(df.at[idx, c])]
        nuevos_emails = [e for e in nuevos_emails if e not in existentes]
        pos = int(df.loc[idx, email_cols].notna().sum())
        for email in nuevos_emails:
            if pos < len(email_cols):
                df.at[idx, email_cols[pos]] = email
                pos += 1
                total_nuevos += 1

    df.drop(columns=['_n_emails'], inplace=True)
    df.to_excel(ARCHIVO_SALIDA, index=False)

    # Resumen final
    df2 = pd.read_excel(ARCHIVO_SALIDA)
    ec = [c for c in df2.columns if c.startswith('Email_')]
    con_email = df2[ec].notna().any(axis=1).sum()

    print(f"\n{'='*50}")
    print(f"Emails nuevos agregados: {total_nuevos}")
    print(f"Total empresas con email: {con_email}/{len(df2)}")
    print(f"Archivo guardado: {ARCHIVO_SALIDA}")

if __name__ == '__main__':
    main()
