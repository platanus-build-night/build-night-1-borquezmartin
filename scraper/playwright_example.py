# pip install playwright
# playwright install

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def scrap_dynamic():
    with sync_playwright() as p:
        # 1. Lanzar Chromium en segundo plano
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 2. Ir a la URL y esperar a que cargue
        page.goto('https://www.theguardian.com/international', 
                  wait_until='networkidle')
        
        # 3. Esperar a selector específico
        page.wait_for_selector('a[data-link-name="article"]')
        
        # 4. Obtener el HTML completo tras ejecución JS
        html = page.content()
        browser.close()
        
    # 5. Parsear con BeautifulSoup (opcional)
    soup = BeautifulSoup(html, 'html.parser')
    noticias = []
    for a in soup.select('a[data-link-name="article"]')[:10]:
        noticias.append({
            'titulo': a.get_text(strip=True),
            'url': a['href']
        })
    return noticias

if __name__ == "__main__":
    resultados = scrap_dynamic()
    for n in resultados:
        print(n)
