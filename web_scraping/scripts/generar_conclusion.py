import json
import google.generativeai as genai

# ---- 1. Configuración de Gemini ----
genai.configure(api_key="TU API DE GOOGLE")

# ---- 2. Cargar datos ----
with open(r'D:\scraping\web_scraping\static\data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# ---- 3. Adaptar sentimientos de tweets (en inglés vienen) ----
sentimientos_tweets = {
    "positivo": data['sentimientos_tweets'].get('positive', 0),
    "neutro": data['sentimientos_tweets'].get('neutral', 0),
    "negativo": data['sentimientos_tweets'].get('negative', 0)
}

# ---- 4. Prompt profesional ----
prompt = f"""
**Análisis político - Elecciones Ecuador 2025**

Como experto en comunicación política, analiza estos datos y explica en 200 palabras por qué Daniel Noboa ganó:

1. **Sentimientos del electorado en periódicos locales**:
   - Positivo: {data['sentimientos_noticias']['positivo']}%
   - Neutro: {data['sentimientos_noticias']['neutro']}%
   - Negativo: {data['sentimientos_noticias']['negativo']}%

2. **Sentimientos del electorado en X (Twitter)**:
   - Positivo: {sentimientos_tweets['positivo']}%
   - Neutro: {sentimientos_tweets['neutro']}%
   - Negativo: {sentimientos_tweets['negativo']}%

3. **Temas clave** (frecuencia):
{chr(10).join([f"   - {k}: {v} menciones" for k, v in data['temas'].items() if v >= 10])}

4. **Menciones a candidatos**:
   - Daniel Noboa: {data['menciones']['Daniel Noboa']} veces
   - Luisa González/Correa: {data['menciones']['Luisa González / Rafael Correa']} veces

5. **Medios citados**:
{chr(10).join([f"   - {k}: {v} artículos" for k, v in data['fuentes'].items()])}

**Requisitos**:
- Lenguaje periodístico
- Máximo 200 palabras
- Relaciona sentimientos, temas y cobertura mediática
- Sin opiniones personales
"""

# ---- 5. Llamada a Gemini API ----
model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content(prompt)
respuesta = response.text.strip()

# ---- 6. Actualizar JSON ----
data['conclusion'] = respuesta

with open(r'D:\scraping\web_scraping\static\data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("✅ Análisis agregado al JSON existente")
print("Extracto de la conclusión:\n", respuesta[:200] + "...")
