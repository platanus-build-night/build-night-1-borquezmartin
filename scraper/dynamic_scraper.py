# pip install playwright
# playwright install

# article_types = {'article', 'feature', 'comment', 'news', 'analysis' }

import os
import re
import json
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import asyncio

# --- Configuración por portal --- #
SCRAP_PROFILES = {
    'guardian': {
        # selector de los <a> que enlazan a los cards
        'link_selector': 'a[data-link-name]',
        # función que decide si un valor de atributo coincide con nuestro tipo
        'link_match': lambda val, t: bool(re.match(rf'^\s*{re.escape(t)}\b', val, re.IGNORECASE)),
        # cómo extraer título y descripción a partir del <a> y su contenedor
        'extract_title': lambda a, card: (a.get('aria-label') or a.get_text(strip=True)).strip(),
        'extract_description': lambda a, card: next(
            (
                d.get_text(strip=True)
                for span in card.find_all('span', class_=re.compile(r'^dcr-'))
                for d in span.find_all('div')
                if d.get_text(strip=True)
            ), None
        ),
        # para subir desde <a> a su “card” contenedor
        'card_ancestor': lambda a: a.find_parent(class_=re.compile(r'^dcr-\w+$'))
    },
    'bbc': {
        'link_selector': 'a[data-testid="internal-link"]',
        # en BBC no filtramos por tipo en el atributo, así que siempre True
        'link_match': lambda val, t: True,
        # en BBC el título está en <h2 data-testid="card-headline">
        'extract_title': lambda a, card: (
            card.select_one('h2[data-testid="card-headline"]').get_text(strip=True)
            if card.select_one('h2[data-testid="card-headline"]') else None
        ),
        # descripción en <p data-testid="card-description">
        'extract_description': lambda a, card: (
            card.select_one('p[data-testid="card-description"]').get_text(strip=True)
            if card.select_one('p[data-testid="card-description"]') else None
        ),
        'card_ancestor': lambda a: a.find_parent('a')  # el propio <a> envuelve todo el card
    }
}


def scrap_dynamic(
    url: str,
    portal: str = 'guardian',
    article_type: str = 'article',
    limit: int = 10,
    timeout: int = 10000
) -> list[dict]:
    """
    Scrapea noticias de distintos portales parametrizados.

    Args:
      url:           URL de la página a scrapear.
      portal:        Clave en SCRAP_PROFILES ('guardian' o 'bbc').
      article_type:  Sólo para portales que filtren por tipo (e.g. Guardian).
      limit:         Máximo de resultados.
      timeout:       Tiempo de espera de selectores en ms.

    Devuelve:
      Lista de dicts {'title','url','description'}.
    """
    profile = SCRAP_PROFILES[portal]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until='networkidle')
        page.wait_for_selector(profile['link_selector'], timeout=timeout)
        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, 'html.parser')
    out = []

    for a in soup.select(profile['link_selector']):
        # extraemos el valor relevante (p.ej. data-link-name o data-testid)
        val = a.get(profile.get('link_attr', 'data-link-name')) or a.get('data-testid', '')
        if not profile['link_match'](val, article_type):
            continue

        href = a.get('href')
        card = profile['card_ancestor'](a) or a

        title = profile['extract_title'](a, card)
        desc  = profile['extract_description'](a, card)

        if not (title and href):
            continue

        out.append({
            'title':       title,
            'url':         href,
            'description': desc
        })
        if len(out) >= limit:
            break

    return out


async def scrap_dynamic_async( url, portal='guardian', article_type='article', limit=10, timeout=10000 ):
    profile = SCRAP_PROFILES[portal]
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page    = await browser.new_page()
        await page.goto(url, wait_until='networkidle')
        await page.wait_for_selector(profile['link_selector'], timeout=timeout)
        html = await page.content()
        await browser.close()
    soup = BeautifulSoup(html, 'html.parser')
    out = []

    for a in soup.select(profile['link_selector']):
        # extraemos el valor relevante (p.ej. data-link-name o data-testid)
        val = a.get(profile.get('link_attr', 'data-link-name')) or a.get('data-testid', '')
        if not profile['link_match'](val, article_type):
            continue

        href = a.get('href')
        card = profile['card_ancestor'](a) or a

        title = profile['extract_title'](a, card)
        desc  = profile['extract_description'](a, card)

        if not (title and href):
            continue

        out.append({
            'title':       title,
            'url':         href,
            'description': desc
        })
        if len(out) >= limit:
            break

    return out

async def main():
    # 1. Carga las URLs de tus portales
    news_links_path = os.path.join('..', 'news_sources.json')
    with open(news_links_path, encoding='utf-8') as f:
        news_sources = json.load(f)

    # 2. Obtén la URL de la BBC
    bbc_url = news_sources['news_portal']['bbc']

    # 3. Llama a tu scraper asíncrono y espera el resultado
    bbc_results = await scrap_dynamic_async(
        url=bbc_url,
        portal='bbc',
        limit=10
    )

    # 4. Muestra los resultados por pantalla
    print("BBC results:")
    print(bbc_results)

if __name__ == "__main__":
    # Arranca el loop de asyncio y ejecuta main()
    asyncio.run(main())

# if __name__ == "__main__":
#     # Ejemplo de uso
#     news_links_path = os.path.join('..', 'news_sources.json')
#     with open(news_links_path) as f:
#         news_sources = json.load(f)

#     guardian_url = news_sources['news_portal']['the_guardian']
#     #features = scrap_dynamic(guardian_url, article_type='article', limit=10)
    
#     # Ejemplo de The Guardian
#     # results = {}
#     # results['the_guardian'] = []
#     # for kind in ['article', 'feature', 'comment', 'news', 'analysis']:
#     #     print(f"\n--- {kind.upper()} ---")
#     #     try:
#     #         features = scrap_dynamic(url=guardian_url, article_type=kind, limit=10)
#     #     except TypeError:
#     #         pass
        
#     #     for item in features:
#     #         item['article_type'] = kind
#     #         # print(f"Title:       {item['title']}")
#     #         # print(f"Article Type: {item['article_type']}\n")
#     #         # print(f"URL:         {item['url']}")
#     #         # print(f"Description: {item['description']}\n")
#     #     results['the_guardian'].append(features)
    
#     # Ejemplo de uso para BBC
#     bbc_results = scrap_dynamic_async(
#         url=news_sources['news_portal']['bbc'],
#         portal='bbc'
#     )
#     print("BBC:", bbc_results)
#     # results['bbc'] = bbc_results
    
#     # # Save results
#     # with open("articles.json", 'w') as json_file:
#     #     json.dump(results, json_file, ensure_ascii=False)

