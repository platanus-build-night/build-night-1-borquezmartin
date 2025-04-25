# pip install playwright
# playwright install

# article_types = {'article', 'feature', 'comment', 'news', 'analysis' }

import os, re, json
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def scrap_dynamic(
    url: str,
    article_type: str = 'feature',
    limit: int = 10,
    timeout: int = 10000
) -> list[dict]:
    prefix_pattern = re.compile(rf'^\s*{re.escape(article_type)}\b', re.IGNORECASE)
    span_pattern   = re.compile(r'^dcr-[\w]+$')

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until='networkidle')
        page.wait_for_selector('a[data-link-name]', timeout=timeout)
        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, 'html.parser')
    resultados = []

    for a in soup.select('a[data-link-name]'):
        if not prefix_pattern.match(a['data-link-name']):
            continue

        title = a.get('aria-label') or a.get_text(strip=True)
        href  = a['href']
        if not (title and href):
            continue

        # Subimos al contenedor visual del card
        card = a.find_parent(class_=re.compile(r'^dcr-\w+$'))
        description = None

        if card:
            # Buscamos el primer <span class="dcr-..."> que contenga un <div> con texto
            for span in card.find_all('span', class_=span_pattern):
                div = span.find('div')
                if div and div.get_text(strip=True):
                    description = div.get_text(strip=True)
                    break

        resultados.append({
            'type':        article_type,
            'title':       title.strip(),
            'url':         href,
            'description': description
        })

        if len(resultados) >= limit:
            break

    return resultados

if __name__ == "__main__":
    # Ejemplo de uso
    news_links_path = os.path.join('..', 'news_sources.json')
    with open(news_links_path) as f:
        news_sources = json.load(f)

    guardian_url = news_sources['news_portal']['the_guardian']
    #features = scrap_dynamic(guardian_url, article_type='article', limit=10)
    
    # Ejemplo de[ uso para cada sección
    for kind in ['article', 'feature', 'comment', 'news', 'analysis']:
        print(f"\n--- {kind.upper()} ---")
        features = scrap_dynamic(url=guardian_url, article_type=kind, limit=10)
        for item in features:
            item['article_type'] = kind
            print(f"Title:       {item['title']}")
            print(f"Article Type: {item['article_type']}\n")
            print(f"URL:         {item['url']}")
            print(f"Description: {item['description']}\n")
    
    # with open("the_guardian_articles.json", 'w') as file:
    #     json.dump(features)
