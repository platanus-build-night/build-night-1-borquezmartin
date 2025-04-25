# pip install playwright
# playwright install

# article_types = {'article', 'feature', 'comment', 'news', 'analysis' }

import os
import re
import json
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def scrap_dynamic(
    url: str,
    article_type: str = 'article',
    limit: int = 10,
    timeout: int = 10000
) -> list[dict]:
    """
    Scrapea enlaces de The Guardian filtrando por regex en data-link-name:
      - Extrae cualquier <a> cuyo atributo data-link-name empiece con article_type.

    Args:
      url: URL de la página principal.
      article_type: Prefijo a buscar en data-link-name (ej. 'feature', 'analysis', 'news').
      limit: Máximo de enlaces a devolver.
      timeout: Tiempo en ms para wait_for_selector.

    Retorna:
      Lista de dicts con {'type', 'title', 'url'}.
    """
    # Compilamos un regex que busque el prefijo al inicio, ignorando espacios:
    prefix_pattern = re.compile(rf'^\s*{re.escape(article_type)}\b', re.IGNORECASE)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until='networkidle')
        # Esperamos a que aparezca al menos un enlace con data-link-name
        page.wait_for_selector('a[data-link-name]', timeout=timeout)
        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, 'html.parser')
    resultados = []

    # Recorremos todas las <a> con data-link-name
    for a in soup.select('a[data-link-name]'):
        dln = a.get('data-link-name', '')
        # Si coincide el prefijo con nuestro tipo...
        if prefix_pattern.match(dln):
            title = a.get('aria-label') or a.get_text(strip=True)
            href  = a.get('href')
            if title and href:
                resultados.append({
                    'type':  article_type,
                    'title': title.strip(),
                    'url':   href
                })
            if len(resultados) >= limit:
                break

    return resultados

if __name__ == "__main__":
    news_links_path = os.path.join('..', 'news_sources.json')
    with open(news_links_path, 'r') as f:
        news_sources = json.load(f)

    guardian_url = news_sources['news_portal']['the_guardian']

    # Ejemplo: extraer las Features
    # features = scrap_dynamic(guardian_url, article_type='international', limit=5)
    # for f in features:
    #     print(f"[{f['type']}] {f['title']}\n   → {f['url']}")

    # Ejemplo de[ uso para cada sección
    for kind in ['article', 'feature', 'comment', 'news', 'analysis']:
        print(f"\n--- {kind.upper()} ---")
        items = scrap_dynamic(url=guardian_url, article_type=kind, limit=5)
        for it in items:
            print(f"[{it['type']}] {it['title']}\n   → {it['url']}")

