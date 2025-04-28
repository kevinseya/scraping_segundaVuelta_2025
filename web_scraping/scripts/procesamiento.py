import pandas as pd
import json
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from collections import Counter
import os

# Cargar CSVs
df_noticias = pd.read_csv(r'D:\scraping\noticias_analizadas.csv')
df_tweets = pd.read_csv(r'D:\scraping\tweets_segunda_vuelta_sentimientos.csv')

# Limpiar datos
df_noticias = df_noticias.dropna(subset=['Contenido'])
df_tweets = df_tweets.dropna(subset=['contenido'])

# Crear textos
text_titles = ' '.join(df_noticias['Titulo_Limpio'].dropna().astype(str))
text_content = ' '.join(df_noticias['Contenido'].dropna().astype(str))
text_tweets = ' '.join(df_tweets['contenido'].dropna().astype(str))

# Definir stopwords personalizados
stopwords = set(STOPWORDS)
stopwords.update([
    'de', 'la', 'hace', 'segunda', 'vuelta', 'abril',
    'daniel', 'luisa', 'rafael', 'ecuador', 'cne', 'elecciones',
    'que', 'en', 'y', 'el', 'los', 'las', 'del', 'un', 'una',
    'se', 'por', 'con', 'para', 'su', 'al', 'lo', 'como', 'más', 'ya',
    'este', 'esta', 'estos', 'esas', 'esas', 'ser', 'fue', 'ha', 'son',
    'también', 'entre', 'sin', 'sobre', 'tras', 'durante', 'contra',
    'año', 'años', 'meses', 'día', 'días', 'hora', 'horas', 'vez', 'veces',
    'ni', 'desde', 'sus', 'puede', 'parte', 'todo', 'e', 'o', 'suscríbete', 'según'
])

# Crear carpetas
output_images = r'D:\scraping\web_scraping\static\images'
os.makedirs(output_images, exist_ok=True)

# WordClouds
WordCloud(width=800, height=400, background_color='white', stopwords=stopwords, collocations=False).generate(text_titles).to_file(os.path.join(output_images, 'wordcloud_titles.png'))
WordCloud(width=800, height=400, background_color='white', stopwords=stopwords, collocations=False).generate(text_content).to_file(os.path.join(output_images, 'wordcloud_content.png'))
WordCloud(width=800, height=400, background_color='white', stopwords=stopwords, collocations=False).generate(text_tweets).to_file(os.path.join(output_images, 'wordcloud_tweets.png'))

# Datos para análisis
sentimientos_noticias = df_noticias['Sentimiento_recalculado'].value_counts().to_dict()
temas = df_noticias['Temas'].value_counts().to_dict()
menciones = {
    'Daniel Noboa': int(df_noticias['Menciones_Noboa'].sum()),
    'Luisa González / Rafael Correa': int(df_noticias['Menciones_Gonzalez'].sum())
}
fuentes = df_noticias['Fuente'].value_counts().to_dict()

# Procesar sentimientos de tweets
sentimientos_tweets = df_tweets['sentimiento'].value_counts().to_dict()

# Últimos 5 tweets
ultimos_tweets = df_tweets[['usuario', 'fecha', 'contenido']].sort_values(by='fecha', ascending=False).head(4).to_dict(orient='records')

# Palabras comunes
palabras_titulos = Counter([
    word.lower() for word in text_titles.split() if word.lower() not in stopwords
]).most_common(20)

palabras_contenido = Counter([
    word.lower() for word in text_content.split() if word.lower() not in stopwords
]).most_common(20)

# Crear data.json
data = {
    'sentimientos_noticias': sentimientos_noticias,
    'sentimientos_tweets': sentimientos_tweets,
    'temas': temas,
    'menciones': menciones,
    'fuentes': fuentes,
    'palabras_titulos': palabras_titulos,
    'palabras_contenido': palabras_contenido,
    'ultimos_tweets': ultimos_tweets
}

output_path = r'D:\scraping\web_scraping\static\data.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("✅ Procesamiento COMPLETO y archivos generados correctamente.")
