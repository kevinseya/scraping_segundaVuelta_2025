import pandas as pd
import requests
import time

# === Configuración ===
csv_path = r'D:\scraping\tweets_segunda_vuelta.csv'
output_path = r'D:\scraping\tweets_segunda_vuelta_sentimientos.csv'

HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-xlm-roberta-base-sentiment"
HUGGINGFACE_TOKEN = "TUTOKEN"  

headers = {
    "Authorization": f"Bearer {HUGGINGFACE_TOKEN}"
}

# === Cargar Tweets ===
df = pd.read_csv(csv_path)

# === Función para enviar texto a HuggingFace ===
def analizar_sentimiento(texto):
    payload = {
        "inputs": texto
    }
    try:
        response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        resultado = response.json()

        # Analizar respuesta
        if isinstance(resultado, list) and len(resultado) > 0:
            mejores = sorted(resultado[0], key=lambda x: x['score'], reverse=True)[0]
            sentimiento = mejores['label'].lower()
            confianza = round(mejores['score'], 3)
            return sentimiento, confianza
        else:
            return 'desconocido', 0.0
    except Exception as e:
        print(f"⚠️ Error analizando sentimiento: {e}")
        return 'desconocido', 0.0

# === Procesar todos los tweets ===
sentimientos = []
confianzas = []

print("🔵 Analizando tweets...")

for index, row in df.iterrows():
    texto = str(row['contenido'])[:300]  # Limitamos a 300 caracteres para ser seguros
    sentimiento, score = analizar_sentimiento(texto)
    sentimientos.append(sentimiento)
    confianzas.append(score)

    # Para no sobrecargar la API gratis
    time.sleep(0.6)

# === Guardar resultados ===
df['sentimiento'] = sentimientos
df['confianza'] = confianzas

df.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"✅ Tweets analizados y guardados en {output_path}")
