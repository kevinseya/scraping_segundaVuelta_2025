import pandas as pd
from textblob import TextBlob
import re

# Cargar el CSV original
csv_path = r'D:\scraping\noticias_segunda_vuelta_ecuador_final_contenido.csv'
df = pd.read_csv(csv_path)

# Limpiar datos: eliminar filas sin contenido
df = df.dropna(subset=['Contenido'])

# Funciones auxiliares

def limpiar_texto(texto):
    texto = re.sub(r'[^\w\s]', '', texto)
    return texto.lower()

def analizar_sentimiento(texto):
    blob = TextBlob(texto)
    polaridad = blob.sentiment.polarity
    if polaridad > 0.05:
        return 'positivo', polaridad
    elif polaridad < -0.05:
        return 'negativo', polaridad
    else:
        return 'neutro', polaridad

def contar_menciones(texto, palabras):
    count = 0
    for palabra in palabras:
        count += texto.count(palabra.lower())
    return count

def detectar_temas(texto):
    temas = []
    if any(p in texto for p in ['seguridad', 'violencia', 'delincuencia', 'crimen']):
        temas.append('Seguridad')
    if any(p in texto for p in ['economía', 'empleo', 'trabajo', 'dinero']):
        temas.append('Economía')
    if any(p in texto for p in ['corrupción', 'corrupto', 'coimas']):
        temas.append('Corrupción')
    if any(p in texto for p in ['renovación', 'cambio', 'nuevo liderazgo']):
        temas.append('Renovación Política')
    return ', '.join(temas) if temas else 'Otros'

# Preprocesar contenido
contenidos_limpios = df['Contenido'].apply(lambda x: limpiar_texto(str(x)))

# Análisis
sentimientos = []
polaridades = []
menciones_noboa = []
menciones_gonzalez = []
temas_detectados = []

for texto in contenidos_limpios:
    sentimiento, polaridad = analizar_sentimiento(texto)
    sentimientos.append(sentimiento)
    polaridades.append(polaridad)
    
    # Contar menciones (Correa se suma a González)
    menciones_noboa.append(contar_menciones(texto, ['noboa', 'daniel noboa']))
    menciones_gonzalez.append(contar_menciones(texto, ['gonzalez', 'luisa gonzalez', 'correa', 'rafael correa']))
    
    temas_detectados.append(detectar_temas(texto))

# Agregar nuevas columnas
df['Sentimiento_recalculado'] = sentimientos
df['Polaridad_recalculada'] = polaridades
df['Menciones_Noboa'] = menciones_noboa
df['Menciones_Gonzalez'] = menciones_gonzalez
df['Temas'] = temas_detectados

# Eliminar columnas anteriores que ya no sirven
df = df.drop(columns=['Sentimiento', 'Polaridad'])

# Guardar el nuevo CSV
nuevo_csv_path = r'D:\scraping\noticias_analizadas.csv'
df.to_csv(nuevo_csv_path, index=False, encoding='utf-8-sig')

print('✅ Análisis completo y CSV actualizado como noticias_analizadas.csv')
