# Importa la clase APIRouter de FastAPI para crear un conjunto de rutas modular.
from fastapi import APIRouter
# Importa los modelos Pydantic para validar la solicitud y estructurar la respuesta.
from app.schemas.summarize import SummarizeRequest, SummarizeResponse
# Importa el servicio que contiene la lógica para resumir videos.
from app.services import summarize_service

# Crea una instancia de APIRouter. Todas las rutas definidas aquí
# se podrán incluir en la aplicación principal de FastAPI.
router = APIRouter()

# Define un endpoint en la ruta "/summarize" que responde a peticiones POST.
# 'response_model=SummarizeResponse' le dice a FastAPI que la respuesta
# debe tener la estructura del modelo SummarizeResponse. Esto es útil para
# la validación, la documentación automática y el autocompletado del editor.
@router.post("/summarize", response_model=SummarizeResponse)
async def get_video_summary(request: SummarizeRequest):
    """
    Endpoint para recibir una URL de YouTube, procesarla y devolver un resumen.

    Args:
        request (SummarizeRequest): El cuerpo de la solicitud, que debe contener
                                    una 'video_url' según el modelo Pydantic.

    Returns:
        SummarizeResponse: Un objeto JSON con el resumen del video.
    """
    # Llama a la función del servicio de resumen, pasándole la URL del video
    # que viene en el cuerpo de la solicitud.
    summary = summarize_service.summarize_youtube_video(request.video_url)
    
    # Crea una instancia del modelo de respuesta con el resumen obtenido
    # y la devuelve. FastAPI se encargará de convertirla a JSON.
    return SummarizeResponse(summary_text=summary)