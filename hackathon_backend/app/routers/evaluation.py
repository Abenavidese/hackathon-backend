# Importa la clase APIRouter de FastAPI para crear un grupo de rutas.
from fastapi import APIRouter
# Importa los modelos Pydantic para validar la solicitud y estructurar la respuesta.
from app.schemas.evaluation import EvaluationRequest, EvaluationResponse 
# Importa el servicio que contiene la lógica para comunicarse con OpenAI.
from app.services import openai_service

# Crea una instancia de APIRouter.
router = APIRouter()

# Define un endpoint en la ruta "/evaluate" que responde a peticiones POST.
# 'response_model=EvaluationResponse' le indica a FastAPI que la respuesta
# debe cumplir con la estructura del modelo EvaluationResponse.
@router.post("/evaluate", response_model=EvaluationResponse)
def evaluate_student_description(request: EvaluationRequest):
    """
    Endpoint para recibir el texto de un estudiante y un texto de referencia,
    y devolver una evaluación generada por IA.

    Args:
        request (EvaluationRequest): El cuerpo de la solicitud, que debe contener
                                     'student_text' y 'reference_text'.

    Returns:
        EvaluationResponse: Un objeto JSON con la evaluación, feedback y texto corregido.
    """
    # 1. Llama a la función del servicio de OpenAI, pasándole los dos textos
    # que vienen en el cuerpo de la solicitud.
    feedback_data = openai_service.get_ai_feedback(
        student_text=request.student_text,
        reference_text=request.reference_text
    )
    
    # 2. Construye la respuesta final usando el modelo Pydantic.
    # Se utiliza .get() con valores por defecto para manejar de forma segura
    # el caso en que el servicio devuelva un error y el diccionario no
    # contenga todas las claves esperadas.
    return EvaluationResponse(
        evaluation=feedback_data.get("evaluation", "Error"),
        feedback=feedback_data.get("feedback", "No se recibió retroalimentación."),
        corrected_text=feedback_data.get("corrected_text", request.student_text)
    )