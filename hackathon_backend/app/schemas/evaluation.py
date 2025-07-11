# Importa la clase base 'BaseModel' de Pydantic para crear modelos de datos.
from pydantic import BaseModel

# --- Modelo para la Solicitud de Evaluación (Request) ---
class EvaluationRequest(BaseModel):
    """
    Define la estructura de los datos que la API necesita recibir para
    realizar una evaluación. Valida la entrada.
    """
    # El texto que el estudiante ha escrito.
    student_text: str
    # El texto de referencia correcto (ej. el generado por el modelo BLIP).
    reference_text: str

# --- Modelo para la Respuesta de Evaluación (Response) ---
class EvaluationResponse(BaseModel):
    """
    Define la estructura de la respuesta que la API enviará de vuelta
    al cliente (ej. el plugin de Moodle) tras la evaluación.
    """
    # El resultado de la evaluación, ej: "Correcto" o "Incorrecto".
    evaluation: str
    # La retroalimentación en texto para el estudiante.
    feedback: str
    # El texto del estudiante con las correcciones aplicadas.
    corrected_text: str