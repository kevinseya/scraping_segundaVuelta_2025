# scraping_contenido_noticias.py

from playwright.sync_api import sync_playwright
import pandas as pd
import os
import time

# Cargar el CSV existente
df = pd.read_csv('noticias_segunda_vuelta_ecuador_final_limpio.csv')

# Añadimos una nueva columna "Contenido" vacía
df['Contenido'] = ''

# Función para limpiar texto
def limpiar_texto(texto):
    if texto:
        return ' '.join(texto.split())
    return ''

# Función para extraer contenido dependiendo de la fuente
def extraer_contenido(page, fuente):
    try:
        if fuente == "El Comercio":
            # El Comercio: generalmente dentro de <div class="article-body">
            contenido = page.locator('div.article-body').inner_text(timeout=3000)
        elif fuente == "El Universo":
            # El Universo: generalmente dentro de <div class="ue-article-content">
            contenido = page.locator('div.ue-article-content').inner_text(timeout=3000)
        elif fuente == "Primicias":
            # Primicias: generalmente dentro de <div class="c-article__body">
            contenido = page.locator('div.c-article__body').inner_text(timeout=3000)
        elif fuente == "Expreso":
            # Expreso: contenido en <div class="article-body">
            contenido = page.locator('div.article-body').inner_text(timeout=3000)
        elif fuente == "El Extra":
            # El Extra: contenido en <div class="content-text">
            contenido = page.locator('div.content-text').inner_text(timeout=3000)
        elif fuente == "Metro Ecuador":
            # Metro Ecuador: contenido en <div class="story-body">
            contenido = page.locator('div.story-body').inner_text(timeout=3000)
        else:
            contenido = ''
    except Exception:
        contenido = ''
    return limpiar_texto(contenido)

# Función principal
def main():
    user_data_dir = os.path.abspath("playwright_cache_content")
    os.makedirs(user_data_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False
        )
        page = browser.new_page()

        for index, row in df.iterrows():
            url = row['URL']
            fuente = row['Fuente']

            try:
                print(f"Accediendo a {url}...")
                page.goto(url, timeout=60000)
                page.wait_for_timeout(3000)

                contenido = extraer_contenido(page, fuente)
                df.at[index, 'Contenido'] = contenido

                if contenido:
                    print(f"✅ Contenido extraído para noticia {index+1}/{len(df)}")
                else:
                    print(f"⚠️ No se encontró contenido para noticia {index+1}/{len(df)}")

            except Exception as e:
                print(f"❌ Error en URL {url}: {e}")
                continue

        browser.close()

    # Guardar nuevo CSV
    df.to_csv('noticias_con_contenido.csv', index=False, encoding='utf-8-sig')
    print(f"✅ Extracción completada. Noticias guardadas en 'noticias_con_contenido.csv'.")

# Ejecutar
if __name__ == "__main__":
    main()
