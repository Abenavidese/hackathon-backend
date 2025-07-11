# Importa la clase base 'BaseModel' de la librería Pydantic.
from pydantic import BaseModel

# --- Modelo para la Solicitud (Request) ---
class GiftRequest(BaseModel):
    """
    Define la estructura que deben tener los datos de entrada para
    solicitar la generación de preguntas en formato GIFT.
    """
    # El cliente debe proporcionar un campo 'image_description' que sea una cadena de texto.
    # Pydantic se encarga de validar que este dato se reciba correctamente.
    image_description: str

# --- Modelo para la Respuesta (Response) ---
class GiftResponse(BaseModel):
    """
    Define la estructura de la respuesta que la API enviará
    después de generar las preguntas.
    """
    # La respuesta contendrá un campo 'gift_text' con el texto de las preguntas
    # en formato GIFT. Esto crea una respuesta de API predecible.
    gift_text: str