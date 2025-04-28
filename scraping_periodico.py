# scraping_periodico_optimizado.py

from playwright.sync_api import sync_playwright
import pandas as pd
from bs4 import BeautifulSoup
import os

# Palabras clave principales
palabras_clave = [
    "segunda vuelta", "daniel noboa", "luisa gonzález", "balotaje", "elecciones 2025"
]

# Variaciones de búsquedas para Google
google_queries = [
    "segunda vuelta 2025 site:elcomercio.com",
    "daniel noboa segunda vuelta site:elcomercio.com",
    "luisa gonzalez elecciones 2025 site:elcomercio.com",
    "balotaje ecuador 2025 site:elcomercio.com",
]

primicias_queries = [
    "segunda vuelta 2025 site:primicias.ec",
    "daniel noboa segunda vuelta site:primicias.ec",
    "luisa gonzalez elecciones 2025 site:primicias.ec",
    "balotaje ecuador 2025 site:primicias.ec",
]

noticias = []

# Funciones

def limpiar_texto(texto):
    if texto:
        return ' '.join(texto.split())
    return ''

def scrape_google(page, queries, fuente, max_google_pages=10):
    print(f"Scrapeando {fuente} vía Google News...")
    total_encontradas = 0
    for query in queries:
        for page_num in range(max_google_pages):
            start = page_num * 10
            url = f"https://www.google.com/search?q={query}&tbm=nws&start={start}"
            page.goto(url)
            page.wait_for_timeout(4000)

            soup = BeautifulSoup(page.content(), 'html.parser')
            resultados = soup.find_all('div', class_='SoaBEf')

            encontrados = 0
            for r in resultados:
                try:
                    a_tag = r.find('a', href=True)
                    titulo = limpiar_texto(a_tag.get_text(strip=True))
                    href = a_tag['href']
                    if any(p in titulo.lower() for p in palabras_clave):
                        noticias.append({
                            "Fuente": fuente,
                            "Titulo": titulo,
                            "URL": href
                        })
                        encontrados += 1
                except Exception:
                    continue

            if encontrados == 0:
                break
            total_encontradas += encontrados
            print(f"  ➔ {encontrados} noticias en query '{query}' página {page_num+1}")
    print(f"✅ Total noticias encontradas en {fuente}: {total_encontradas}")

def scrape_scroll_universo(page):
    print("Scrapeando El Universo...")
    url = "https://www.eluniverso.com/resultados/?search=segunda+vuelta+2025"
    page.goto(url)
    page.wait_for_timeout(3000)

    for _ in range(8):
        page.mouse.wheel(0, 10000)
        page.wait_for_timeout(3000)

    soup = BeautifulSoup(page.content(), 'html.parser')
    links = soup.find_all('a', href=True)

    count = 0
    for link in links:
        titulo = limpiar_texto(link.get_text(strip=True))
        href = link['href']

        if href and not href.startswith('https://www.google.com') and any(p in titulo.lower() for p in palabras_clave):
            if href.startswith('/'):
                href = "https://www.eluniverso.com" + href
            noticias.append({
                "Fuente": "El Universo",
                "Titulo": titulo,
                "URL": href
            })
            count += 1
    print(f"✅ {count} noticias encontradas en El Universo.")

def scrape_click_ver_mas(nombre, url, page, clicks=3):
    print(f"Scrapeando {nombre}...")
    page.goto(url)
    page.wait_for_timeout(3000)

    for i in range(clicks):
        try:
            ver_mas_button = page.locator('text=Ver más')
            ver_mas_button.click()
            page.wait_for_timeout(4000)
        except:
            break

    soup = BeautifulSoup(page.content(), 'html.parser')
    links = soup.find_all('a', href=True)

    count = 0
    for link in links:
        titulo = limpiar_texto(link.get_text(strip=True))
        href = link['href']

        if titulo and any(p in titulo.lower() for p in palabras_clave):
            if href.startswith('/'):
                href = url.split('/')[0] + '//' + url.split('/')[2] + href
            noticias.append({
                "Fuente": nombre,
                "Titulo": titulo,
                "URL": href
            })
            count += 1
    print(f"✅ {count} noticias encontradas en {nombre}.")

def scrape_metro(page):
    print("Scrapeando Metro Ecuador...")
    page.goto("https://www.metroecuador.com.ec/buscador/")
    page.wait_for_timeout(3000)

    try:
        page.fill('input[type="text"]', 'segunda vuelta 2025')
        page.press('input[type="text"]', 'Enter')
        page.wait_for_timeout(5000)

        soup = BeautifulSoup(page.content(), 'html.parser')
        links = soup.find_all('a', href=True)

        count = 0
        for link in links:
            titulo = limpiar_texto(link.get_text(strip=True))
            href = link['href']

            if href and any(p in titulo.lower() for p in palabras_clave):
                if href.startswith('/'):
                    href = "https://www.metroecuador.com.ec" + href
                noticias.append({
                    "Fuente": "Metro Ecuador",
                    "Titulo": titulo,
                    "URL": href
                })
                count += 1
        print(f"✅ {count} noticias encontradas en Metro Ecuador.")
    except Exception as e:
        print(f"❌ Error en Metro Ecuador: {e}")

# Funcíon principal

def main():
    user_data_dir = os.path.abspath("playwright_cache")
    os.makedirs(user_data_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(user_data_dir=user_data_dir, headless=False)
        page = browser.new_page()

        scrape_google(page, google_queries, "El Comercio", max_google_pages=10)
        scrape_scroll_universo(page)
        scrape_google(page, primicias_queries, "Primicias", max_google_pages=10)
        scrape_click_ver_mas("Expreso", "https://www.expreso.ec/search?q=segunda+vuelta+2025", page, clicks=10)
        scrape_click_ver_mas("El Extra", "https://www.extra.ec/search?q=segunda+vuelta+2025", page, clicks=10)
        scrape_metro(page)

        browser.close()

    df = pd.DataFrame(noticias).drop_duplicates(subset=["URL"])
    df.to_csv('noticias_segunda_vuelta_ecuador_final.csv', index=False, encoding='utf-8-sig')
    print(f"✅ Scraping completado. Total noticias únicas: {len(df)}")

# Ejecutar
if __name__ == "__main__":
    main()
