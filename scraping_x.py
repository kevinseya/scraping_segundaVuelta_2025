import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# ========== CONFIGURACIÓN NAVEGADOR ==========
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# ========== AUTENTICACIÓN ==========
driver.get("https://x.com/")

driver.add_cookie({
    'name': 'auth_token',
    'value': 'tu auth_token',
    'domain': '.x.com',
    'path': '/',
    'secure': True,
    'httpOnly': True,
    'sameSite': 'Lax'
})
driver.add_cookie({
    'name': 'ct0',
    'value': 'tu ct0',
    'domain': '.x.com',
    'path': '/',
    'secure': True,
    'httpOnly': True,
    'sameSite': 'Lax'
})

driver.refresh()
time.sleep(3)

# ========== BÚSQUEDA ==========
busqueda = "segunda vuelta 2025 ecuador lang:es"
url = f"https://x.com/search?q={busqueda}&src=typed_query&f=live"
driver.get(url)

print("🔎 Buscando tweets...")
time.sleep(5)

# ========== SCRAPING ==========
def extraer_metricas(tweet_element):
    likes = 0
    reposts = 0
    try:
        spans = tweet_element.find_elements(By.XPATH, './/span[contains(@class,"r-poiln3")]')
        for span in spans:
            try:
                parent = span.find_element(By.XPATH, './../..')
                svg = parent.find_element(By.TAG_NAME, 'svg')
                path = svg.get_attribute('outerHTML')

                if 'M16.697 5.5c-' in path:
                    likes = int(span.text.replace(',', '')) if span.text.replace(',', '').isdigit() else 0
                if 'M4.5 3.88l' in path:
                    reposts = int(span.text.replace(',', '')) if span.text.replace(',', '').isdigit() else 0
            except:
                continue
    except:
        pass
    return likes, reposts

tweets = []
scrolls = 100

for _ in range(scrolls):
    tweet_elements = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')
    for tweet in tweet_elements:
        try:
            usuario = tweet.find_element(By.XPATH, './/div[@dir="ltr"]/span').text
            fecha = tweet.find_element(By.XPATH, './/time').get_attribute('datetime')
            contenido = tweet.find_element(By.XPATH, './/div[@data-testid="tweetText"]').text
            likes, retweets = extraer_metricas(tweet)

            tweets.append({
                'usuario': usuario,
                'fecha': fecha,
                'contenido': contenido,
                'likes': likes,
                'retweets': retweets
            })
        except Exception as e:
            print(f"⚠️ Error extrayendo un tweet: {e}")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)

# ========== GUARDADO ==========
# Eliminar duplicados
tweets_unicos = {(t['usuario'], t['contenido']): t for t in tweets}.values()
tweets_unicos = list(tweets_unicos)

print(f"✅ {len(tweets_unicos)} tweets capturados únicos")

# Guardar CSV
output_path = r'D:\scraping\tweets_segunda_vuelta.csv'
with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ["usuario", "fecha", "contenido", "likes", "retweets"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for tweet in tweets_unicos:
        writer.writerow(tweet)

print(f"✅ Tweets guardados exitosamente en {output_path}")

# Cerrar navegador
driver.quit()
