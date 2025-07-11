# --- Importaciones de librerías necesarias ---
import os # Para acceder a variables de entorno (como claves de API)
import google.generativeai as genai # La librería oficial de Google para usar la API de Gemini
from youtube_transcript_api import YouTubeTranscriptApi # Para descargar transcripciones de YouTube

# --- Configuración de la API de Gemini ---
# Carga la clave de la API desde las variables de entorno del sistema.
# Es una buena práctica para no exponer claves secretas en el código.
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

def summarize_youtube_video(url: str) -> str:
    """
    Función que toma una URL de YouTube, extrae su transcripción y
    utiliza la IA de Gemini para generar un resumen en francés.

    Args:
        url (str): La URL completa del video de YouTube.

    Returns:
        str: Un resumen del video o un mensaje de error.
    """
    # --- Paso 1: Extraer la transcripción del video ---
    try:
        # Extrae el ID único del video de la URL. Funciona para URLs como
        # '.../watch?v=VIDEO_ID' y '.../watch?v=VIDEO_ID&list=...'
        video_id = url.split("v=")[1].split("&")[0]
        
        # Pide la transcripción a la API de YouTube. Intenta obtenerla en español,
        # inglés o francés, en ese orden de preferencia.
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['es', 'en', 'fr'])
        
        # Une todas las líneas de la transcripción en un solo bloque de texto.
        transcript_text = " ".join([item['text'] for item in transcript_list])

    except Exception as e:
        # Si algo falla (ej: el video no existe, no tiene subtítulos, etc.),
        # se captura el error y se devuelve un mensaje informativo.
        print(f"Error al obtener la transcripción: {e}")
        return "No se pudo obtener la transcripción del video. Asegúrate de que el video tenga subtítulos activados."

    # --- Paso 2: Resumir el texto con la IA de Gemini ---
    try:
        # Selecciona el modelo de Gemini a utilizar. 'gemini-1.5-flash' es
        # ideal para tareas rápidas y eficientes como esta.
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Crea el 'prompt' o la instrucción para la IA. Se le pide que resuma
        # el texto extraído en tres puntos clave y en un francés claro.
        prompt = f"Resume el siguiente texto en tres puntos clave y en un francés claro y conciso:\n\n---\n\n{transcript_text}"
        
        # Envía la petición a la API de Gemini y espera la respuesta.
        response = model.generate_content(prompt)
        
        # Devuelve el texto generado por el modelo.
        return response.text

    except Exception as e:
        # Si hay un problema con la API de Gemini (ej: clave incorrecta, error del servidor),
        # se captura y se devuelve un mensaje genérico.
        print(f"Error al llamar a la API de Gemini: {e}")
        return "Hubo un error al generar el resumen."