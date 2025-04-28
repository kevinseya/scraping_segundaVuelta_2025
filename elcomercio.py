import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Ruta del CSV
csv_path = 'noticias_segunda_vuelta_ecuador_final_contenido.csv'

# Cargar CSV
df = pd.read_csv(csv_path)
print("Columnas en el CSV:", df.columns.tolist())

# Configurar Chrome (NO HEADLESS para que no detecten scraping)
chrome_options = Options()
# No agregamos chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--start-maximized")

# Iniciar navegador
driver = webdriver.Chrome(options=chrome_options)

# Procesar solo los primeros 92
for idx, row in df.iloc[:92].iterrows():
    url = row['URL']
    if pd.isna(row['Contenido']) or row['Contenido'].strip() == '':
        print(f"\nProcesando noticia {idx+1}: {url}")
        
        intentos = 0
        max_intentos = 2
        exito = False
        
        while intentos < max_intentos and not exito:
            try:
                driver.get(url)
                
                # Esperar hasta que cargue algo de contenido
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'single-layout__article'))
                )
                
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                article = soup.find('div', class_='single-layout__article')
                
                if article:
                    paragraphs = article.find_all('p')
                    contenido = ' '.join(p.get_text(strip=True) for p in paragraphs)
                    df.at[idx, 'Contenido'] = contenido
                    print(f"✅ Contenido guardado para noticia {idx+1}")
                    exito = True
                else:
                    print(f"⚠️ No se encontró contenido en el HTML para {url}")
                    break  # Si no hay div, no vale intentar de nuevo
            except Exception as e:
                intentos += 1
                print(f"⚠️ Error ({intentos}) en {url}: {e}")
                time.sleep(3)
    
# Guardar CSV actualizado
driver.quit()
df.to_csv(csv_path, index=False, encoding='utf-8-sig')
print("\n✅ Todos los datos procesados y guardados correctamente.")
