# app/services/blip_service.py

# --- Importaciones Necesarias ---
from PIL import Image # Python Imaging Library (Pillow) para abrir y manipular imágenes.
from transformers import BlipProcessor, BlipForConditionalGeneration # Clases de la librería Hugging Face para el modelo BLIP.
import torch # PyTorch, aunque no se usa explícitamente en el código, es la base de transformers.

# --- Carga del Modelo al Iniciar (se hace una sola vez) ---
# Esta sección de código se ejecuta una única vez cuando el servicio se importa por primera vez.
# Cargar el modelo en memoria al inicio evita tener que cargarlo en cada petición, lo que sería muy lento.

# Define la ruta a la carpeta donde se encuentra el modelo descargado.
MODEL_PATH = "./model/blip2-frances" 
print("Cargando modelo BLIP-2 en CPU...")
try:
    # Carga el 'procesador', que prepara las imágenes para el modelo (cambia tamaño, normaliza, etc.).
    processor = BlipProcessor.from_pretrained(MODEL_PATH)
    # Carga el modelo de generación de texto condicional, que es el "cerebro" que crea la descripción.
    model = BlipForConditionalGeneration.from_pretrained(MODEL_PATH)
    print("Modelo cargado exitosamente.")
except Exception as e:
    # Si la carga falla (ej. archivos corruptos o ruta incorrecta), se informa del error
    # y se dejan las variables como None para manejarlo después.
    print(f"Error crítico al cargar el modelo: {e}")
    processor = None
    model = None
# ---------------------------------------------------------

def describe_image(image_name: str) -> str:
    """
    Genera una descripción en francés para una imagen dada utilizando el modelo BLIP-2.

    Args:
        image_name (str): El nombre del archivo de la imagen (ej: "gato.jpg").

    Returns:
        str: La descripción generada o un mensaje de error.
    """
    # Verificación inicial: si el modelo no se cargó correctamente, no se puede continuar.
    if not model or not processor:
        return "Error: El modelo BLIP no está cargado."
    
    try:
        # Construye la ruta completa al archivo de la imagen.
        image_path = f"images/{image_name}"
        # Abre la imagen usando Pillow y la convierte al formato RGB, que es el estándar para el modelo.
        raw_image = Image.open(image_path).convert('RGB')
        
        # Paso 1: Procesar la imagen. El procesador la convierte a tensores numéricos.
        inputs = processor(images=raw_image, return_tensors="pt")
        
        print(f"Generando descripción para {image_name} en CPU (esto puede tardar)...")
        # Paso 2: Generar la descripción. El modelo toma los tensores y produce una secuencia de texto.
        # `max_new_tokens` limita la longitud de la descripción para que sea más rápida y concisa.
        out = model.generate(**inputs, max_new_tokens=75)
        
        # Paso 3: Decodificar el resultado. El procesador convierte la salida del modelo a texto legible.
        description = processor.decode(out[0], skip_special_tokens=True)
        print(f"Descripción generada: '{description}'")
        
        return description

    except FileNotFoundError:
        # Maneja el caso en que el archivo de la imagen no se encuentre en la ruta especificada.
        return "Erreur: L'image n'a pas été trouvée."
    except Exception as e:
        # Captura cualquier otro error que pueda ocurrir durante el proceso.
        return f"Erreur lors de la description de l'image: {e}"