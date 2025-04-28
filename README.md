# 🗳️ Análisis de Noticias y Redes Sociales - Segunda Vuelta Ecuador 2025

---

## 📜 Descripción General

Este proyecto realiza scraping, procesamiento y análisis automatizado de noticias de los principales periódicos de Ecuador y publicaciones en la red social **X** (anteriormente Twitter) con el objetivo de entender **por qué Daniel Noboa ganó** las elecciones presidenciales 2025.

Incluye:
- Recolección masiva de datos de medios y redes.
- Limpieza y análisis de sentimientos.
- Detección de temas principales.
- Visualización en un dashboard web moderno.
- Generación automática de conclusión analítica con IA.

---

## ⚙️ Instalación

### 1. Requisitos Previos
- Tener instalado **Python 3.9 o superior**.
- Tener instalado **Git** (opcional).

### 2. Clonar el repositorio
```bash
git clone https://github.com/kevinseya/scraping_segundaVuelta_2025.git
cd scraping_segundaVuelta_2025
```

### 3. Crear un entorno virtual
```bash
python -m venv env
```

### 4. Activar el entorno virtual
```bash
.\env\Scripts\activate
```

### 5. Instalar dependencias
```bash
pip install -r requirements.txt
```

## 🔐 Variables de Entorno
Debes configurar las siguientes claves para que funcione correctamente en el caso de que se vuelva a scrapear la información de cada medio y se analice:

    HUGGINGFACE_TOKEN: Token para análisis de sentimientos con HuggingFace API.

    API_GOOGLE: API Key de Google para usar Gemini y generar la conclusión automatizada.

    AUTH_TOKEN y CT0: Cookies de autenticación necesarias para scrapear resultados de X.

Puedes configurarlas en un archivo .env en la raíz:
```bash
HUGGINGFACE_TOKEN=your_huggingface_token
API_GOOGLE=your_google_api_key
AUTH_TOKEN=your_x_auth_token
CT0=your_x_ct0_token
```

## 🚀 Ejecución del Proyecto

### 1. Procesar los datos (noticias y tweets):
```bash
python .\web_scraping\scripts\procesamiento.py
```
### 2.  Generar la conclusión automatizada:
```bash
python .\web_scraping\scripts\generar_conclusion.py
```
### 3.Correr el servidor Flask:
```bash
python .\web_scraping\app.py
```
### 4. Acceder al dashboard:
  Navegar a http://127.0.0.1:5000 en tu navegador web.

## 📊 ¿Qué Incluye el Dashboard?
- Nube de Palabras de títulos, contenidos de noticias y tweets.
- Distribución de Sentimientos en periódicos y en X.
- Análisis de Temas Relevantes.
- Menciones por Candidato.
- Principales Fuentes de Noticias.
- Últimos Tweets Capturados.
- Conclusión automatizada generada con IA

## 🔍 Estructura del Proyecto
```bash
scraping/
│
├── env/                # Entorno virtual
├── web_scraping/
│   ├── static/
│   │   ├── images/     # Wordclouds y gráficos
│   │   └── css/        # Estilos CSS
│   ├── templates/
│   │   └── index.html  # Frontend del dashboard
│   ├── scripts/
│   │   ├── procesamiento.py
│   │   └── generar_conclusion.py
│   └── app.py          # Servidor Flask
│
├── .env                # Variables de entorno
├── requirements.txt    # Dependencias del proyecto
├── scraping_periodico.py      # Scraping de noticias
├── scraping_contenido.py      # Scraping del contenido de noticias
├── scraping_x.py               # Scraping de X
├── analisis_noticias.py        # Análisis de sentimiento en noticias
├── analisis_sentimiento_x.py   # Análisis de sentimiento en tweets
└── .gitignore
```

##🧠 Tecnologías Utilizadas

    Python (3.9+)
    Playwright y Selenium para scraping
    BeautifulSoup para parsing HTML
    TextBlob para análisis de sentimientos en noticias
    HuggingFace API para análisis de sentimientos en tweets
    Google Generative AI (Gemini) para generación de conclusiones
    Flask para servidor web
    TailwindCSS + Chart.js para visualización de datos
    Matplotlib y WordCloud para nubes de palabras

##📚 Anexos
![imagen](https://github.com/user-attachments/assets/fa32d0ee-3a25-4bbc-a605-287056ea22dc)
![imagen](https://github.com/user-attachments/assets/54574d95-b7fb-4dde-aa87-c82bed2e50fb)
![imagen](https://github.com/user-attachments/assets/28868f62-e2df-4b4a-9393-181043aa5b09)
![imagen](https://github.com/user-attachments/assets/7e0a046e-3976-483f-a037-abc7ca46eee2)
![imagen](https://github.com/user-attachments/assets/bcc8bc7b-f290-4754-ba03-163b509216b6)





