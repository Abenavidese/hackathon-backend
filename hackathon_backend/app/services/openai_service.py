# --- Importaciones de Módulos ---
import os           # Para acceder a variables de entorno (claves de API).
import json         # Para trabajar con datos en formato JSON.
import requests     # Para realizar peticiones HTTP a la API.
from dotenv import load_dotenv # Para cargar variables desde un archivo .env

# Carga las variables de entorno definidas en el archivo .env.
# Esto permite mantener las claves secretas fuera del código fuente.
load_dotenv()

# --- Configuración Inicial ---
# Obtiene la clave de la API de OpenAI desde las variables de entorno.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# Define la URL del endpoint para los modelos de chat de OpenAI.
API_URL = "https://api.openai.com/v1/chat/completions"


def get_ai_feedback(student_text: str, reference_text: str) -> dict:
    """
    Envía el texto de un estudiante y un texto de referencia a la API de OpenAI
    para obtener una evaluación estructurada en formato JSON.

    Args:
        student_text (str): La descripción escrita por el estudiante.
        reference_text (str): La descripción correcta o de referencia.

    Returns:
        dict: Un diccionario con la evaluación, feedback y texto corregido.
    """
    # Se crea un 'prompt' detallado que instruye a la IA sobre su rol, la tarea,
    # los criterios de evaluación y, muy importante, el formato de salida.
    prompt_template = f"""
    Actúa como un profesor de francés experto. Se le ha dado una imagen a un estudiante para que la describa.

    - La descripción de referencia (la descripción real de la imagen) es: "{reference_text}"
    - La descripción del estudiante es: "{student_text}"

    Tu tarea es evaluar la descripción del estudiante y devolver **únicamente un objeto JSON** con la siguiente estructura:
    - "evaluation": una cadena de texto, "Correcto" si la respuesta del estudiante tiene buena estructura gramatical y coherencia con el tema, o "Incorrecto" en caso contrario.
    - "feedback": una cadena de texto con una retroalimentación breve y amigable en francés para el estudiante.
    - "corrected_text": una cadena de texto con la corrección de la frase del estudiante. Si la frase es perfecta, devuelve el texto original.
    
    Tienes que tener en cuenta la coherencia, si la imagen describe un gato y un perro, y el estudiante menciona un perro pero no un gato, la respuesta debe ser "Incorrecto" y ademas decirle que se olvido mencionar el gato.
    Analiza la gramática, el vocabulario y la coherencia. No seas demasiado severo.
    """

    # Cabeceras necesarias para la autenticación y el tipo de contenido.
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    # El cuerpo (payload) de la petición a la API.
    data = {
        "model": "gpt-4.1-nano", # Modelo pequeño y rápido, ideal para tareas de evaluación simples.
        "messages": [{"role": "user", "content": prompt_template}],
        "response_format": {"type": "json_object"}, # Forza a la API a devolver un JSON válido.
        "temperature": 0.3 # Baja temperatura para respuestas más predecibles y menos creativas.
    }

    try:
        # Se envía la petición POST a la API de OpenAI.
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status() # Lanza un error si la respuesta HTTP no es exitosa (ej. 401, 500).
        
        # El resultado de la IA es un string con formato JSON.
        # `json.loads` lo convierte a un diccionario de Python.
        ai_response_dict = json.loads(response.json()['choices'][0]['message']['content'])
        return ai_response_dict
    except requests.exceptions.RequestException as e:
        # Captura errores de red y devuelve un diccionario de error estándar.
        print(f"Error llamando a la API de OpenAI: {e}")
        return {
            "evaluation": "Error",
            "feedback": "No se pudo conectar con el servicio de evaluación.",
            "corrected_text": ""
        }


def generate_gift_questions(image_description: str) -> str:
    """
    Usa la descripción de una imagen para generar un conjunto de preguntas
    en formato GIFT, compatible con Moodle.

    Args:
        image_description (str): El texto que describe la imagen.

    Returns:
        str: Un string que contiene las preguntas en formato GIFT.
    """
    # En los f-strings de Python, las llaves dobles {{ y }} se usan para
    # representar llaves literales { y } en el texto final.
    prompt_template = f"""
    Eres un asistente de creación de contenido educativo para Moodle, experto en el formato de preguntas GIFT.

    Basado en la siguiente descripción de una imagen en francés:
    "{image_description}"

    Tu tarea es generar 4 preguntas en francés, seleccionando aleatoriamente entre los siguientes tipos: Opción múltiple, Verdadero/Falso, Respuesta corta o Emparejamiento.

    Debes devolver **únicamente el texto en formato GIFT**, sin ninguna explicación adicional. El formato debe ser perfecto.

    Ejemplo de formato de salida:

    ::Pregunta 1:: Quelle est la couleur principale de la voiture ? {{{{
    ~Bleu
    =Rouge
    ~Vert
    }}}}

    ::Pregunta 2:: L'homme porte un chapeau. {{{{TRUE}}}}
    """

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o-mini",  # Modelo más reciente y capaz, bueno para generar contenido creativo.
        "messages": [{"role": "user", "content": prompt_template}],
        "temperature": 0.6 # Temperatura media para obtener variedad en las preguntas sin ser demasiado aleatorio.
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        
        # Aquí se extrae directamente el texto de la respuesta, que ya viene en formato GIFT.
        gift_text = response.json()['choices'][0]['message']['content']
        return gift_text
    except requests.exceptions.RequestException as e:
        print(f"Error generando preguntas GIFT: {e}")
        # Devuelve una pregunta GIFT de error para que Moodle pueda procesarla.
        return "::Error:: No se pudieron generar las preguntas. {{=OK}}"