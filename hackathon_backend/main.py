# main.py

# --- Importaciones de FastAPI y Módulos ---
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware # Importante para la comunicación Moodle <-> API

# Importa los 'routers' que contienen los endpoints de la aplicación.
# Cada router agrupa endpoints relacionados (ej: todo lo de evaluación en evaluation.py).
from app.routers import exercise, evaluation, quiz, summarize

# --- Creación de la Instancia de la Aplicación FastAPI ---
# Se crea la aplicación principal y se le asigna metadatos como título y descripción.
# Esto es útil para la documentación automática (ej: en /docs).
app = FastAPI(
    title="Hackathon MOOC+IA API",
    description="API para evaluar descripciones de imágenes en francés.",
    version="1.0.0"
)

# --- Configuración de CORS (Cross-Origin Resource Sharing) ---
# Esto es un mecanismo de seguridad que permite que un frontend (como Moodle)
# que se ejecuta en un origen diferente (ej: https://localhost) pueda
# hacer peticiones a esta API (que se ejecuta en http://localhost:8000).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost", "http://localhost"], # Lista de orígenes que tienen permiso.
    allow_credentials=True,       # Permite el envío de cookies o cabeceras de autorización.
    allow_methods=["*"],          # Permite todos los métodos HTTP (GET, POST, PUT, DELETE, etc.).
    allow_headers=["*"],          # Permite todas las cabeceras en las peticiones.
)

# --- Montar la Carpeta de Imágenes Estáticas ---
# Esta línea hace que la carpeta 'images' del proyecto sea accesible públicamente
# a través de la URL '/static'. Por ejemplo, una imagen 'images/ejemplo.jpg'
# estaría disponible en 'http://localhost:8000/static/ejemplo.jpg'.
app.mount("/static", StaticFiles(directory="images"), name="static")


# --- Inclusión de los Routers en la Aplicación Principal ---
# Aquí se incorporan los endpoints definidos en los archivos importados.
# El 'prefix' añade '/api' al inicio de todas las rutas de ese router.
# El 'tags' agrupa los endpoints en la documentación automática.
app.include_router(evaluation.router, prefix="/api", tags=["Evaluation"])
app.include_router(exercise.router, prefix="/api", tags=["Exercise"])
app.include_router(quiz.router, prefix="/api", tags=["Quiz"])
app.include_router(summarize.router, prefix="/api", tags=["Summarize"])


# --- Endpoint Raíz (Root) ---
# Define una ruta para la raíz de la API (la URL principal).
# Es útil para comprobar rápidamente que la API está funcionando.
@app.get("/", tags=["Root"])
def read_root():
    """
    Devuelve un mensaje de bienvenida cuando se accede a la raíz de la API.
    """
    return {"message": "Bienvenue à l'API du Hackathon MOOC+IA"}