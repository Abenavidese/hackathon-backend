# Importa la clase APIRouter para crear un conjunto de rutas modular.
from fastapi import APIRouter
# Importa los modelos Pydantic para la solicitud y la respuesta.
from app.schemas.quiz import GiftRequest, GiftResponse
# Importa el servicio que se comunica con la API de OpenAI.
from app.services import openai_service

# Crea una instancia de APIRouter.
router = APIRouter()

# Define un endpoint en la ruta "/quiz/generate" que responde a peticiones POST.
# 'response_model=GiftResponse' asegura que la respuesta de la API tendrá
# la estructura definida en el modelo GiftResponse.
@router.post("/quiz/generate", response_model=GiftResponse)
def create_gift_quiz(request: GiftRequest):
    """
    Endpoint para generar un cuestionario en formato GIFT a partir de la
    descripción de una imagen.

    Args:
        request (GiftRequest): El cuerpo de la solicitud, que debe contener
                               una 'image_description'.

    Returns:
        GiftResponse: Un objeto JSON con el texto del cuestionario en formato GIFT.
    """
    # Llama a la función del servicio de OpenAI, pasándole la descripción
    # de la imagen que viene en la solicitud.
    gift_formatted_text = openai_service.generate_gift_questions(
        image_description=request.image_description
    )
    
    # Crea una instancia del modelo de respuesta con el texto GIFT obtenido
    # y la devuelve para que FastAPI la envíe como respuesta JSON.
    return GiftResponse(gift_text=gift_formatted_text)