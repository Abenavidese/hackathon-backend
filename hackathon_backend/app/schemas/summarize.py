# Importa la clase base 'BaseModel' de la librería Pydantic.
from pydantic import BaseModel

# --- Modelo para la Solicitud (Request) ---
class SummarizeRequest(BaseModel):
    """
    Define la estructura de los datos que la API espera recibir
    cuando un cliente solicita resumir un video.
    """
    # Espera un campo llamado 'video_url' que debe ser una cadena de texto (string).
    # Pydantic validará automáticamente que el dato recibido cumpla con este tipo.
    video_url: str

# --- Modelo para la Respuesta (Response) ---
class SummarizeResponse(BaseModel):
    """
    Define la estructura de los datos que la API enviará de vuelta
    al cliente como respuesta.
    """
    # La respuesta contendrá un campo llamado 'summary_text', que será una cadena de texto.
    # Esto asegura que la respuesta de la API sea consistente.
    summary_text: str