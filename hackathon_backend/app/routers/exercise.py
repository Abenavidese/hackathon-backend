# app/routers/exercise.py

# --- Importaciones Necesarias ---
import random  # Para seleccionar elementos de forma aleatoria.
import os      # Para interactuar con el sistema operativo, como listar archivos de un directorio.
from fastapi import APIRouter
from pydantic import BaseModel

# Importa el servicio que contiene la lógica para describir imágenes.
from app.services import blip_service

# Crea una instancia de APIRouter para agrupar las rutas de esta sección.
router = APIRouter()

# --- Modelo de Datos para la Respuesta ---
class NewExerciseResponse(BaseModel):
    """
    Define la estructura de la respuesta que se enviará al cliente
    cuando solicite un nuevo ejercicio.
    """
    image_url: str      # La URL para acceder a la imagen.
    reference_text: str # La descripción de la imagen generada por BLIP.

# --- Definición del Endpoint ---
# Define un endpoint en la ruta "/exercise/new" que responde a peticiones GET.
# 'response_model' asegura que la respuesta se ajuste al modelo NewExerciseResponse.
@router.get("/exercise/new", response_model=NewExerciseResponse)
def get_new_exercise():
    """
    Endpoint que selecciona una imagen al azar, genera su descripción
    y devuelve ambos datos para crear un nuevo ejercicio.
    """
    # 1. Obtiene una lista de todos los nombres de archivo en el directorio 'images'.
    image_files = os.listdir("images")
    # Elige un nombre de archivo de la lista de forma aleatoria.
    random_image_name = random.choice(image_files)

    # 2. Llama al servicio de BLIP para que genere una descripción para la imagen seleccionada.
    description = blip_service.describe_image(random_image_name)

    # 3. Construye y devuelve la respuesta utilizando el modelo Pydantic.
    # La URL se formatea para apuntar al endpoint de archivos estáticos.
    return NewExerciseResponse(
        image_url=f"/static/{random_image_name}",
        reference_text=description
    )