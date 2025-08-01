## Proyecto Hackaton 2025 implementado agente de IA

Este prototípo tiene como objetivo servir un backend para la integracion de agentes de IA como pluggin a la plataforma de moodle
---


Este proyecto, desarrollado para la Hackathon 2025, es un prototipo funcional de un backend que potencia un plugin de Moodle para la enseñanza del idioma francés. La solución utiliza un ecosistema de agentes de IA para crear, evaluar y complementar ejercicios de aprendizaje de forma automática e inteligente.

El sistema es capaz de generar ejercicios visuales pidiendo al estudiante que describa una imagen, para luego usar un modelo de lenguaje avanzado para evaluar la respuesta en términos de coherencia gramatical y contextual, ofreciendo retroalimentación instantánea y personalizada.

## Funcionalidades Principales
Este backend ofrece una API con cuatro funcionalidades clave diseñadas para integrarse con Moodle:

Generación de Ejercicios (/exercise/new): Selecciona una imagen aleatoria del sistema y utiliza el modelo BLIP-2 para generar una descripción de referencia en francés. Esto crea la base para un ejercicio de "describe la imagen".

Evaluación Inteligente (/evaluate): Recibe la descripción del estudiante y la compara con el texto de referencia usando GPT-4. Proporciona una calificación ("Correcto" o "Incorrecto"), feedback constructivo y una versión corregida del texto.

Creación de Cuestionarios (/quiz/generate): A partir de la descripción de una imagen, utiliza GPT-4o-mini para generar automáticamente un cuestionario de 4 preguntas en formato GIFT, listo para ser importado en Moodle.



## 📂 Estructura del Proyecto

```text
moodle_protipo/
|
└──hackthon_backend/
|    ├── app/ # app general
|    |    ├── routers/ # Incluye los routers de la aplicación
|    |    ├── schemas/ # Plantilla de las solicitudes a la aplicacion
|    |    ├── services/ # Servicios de la aplicación
|    ├── images/ # Imagenes de prueba
|    ├── model/ # modelo blip-2 de la aplicación
|    ├── .env # archivo con las variables de entorno

|
└──moodle/ #se genera al levantar el docker
|    ├── mod/ # Carpeta para instalar plugings
|    |      ├── iafrance/ # Pluging generado para la hackaton
└──moodledata/ #se genera al levantar el docker
└── README.md # Manual de uso de la aplicación
└── docker-compose.yml #Archivo para levantar docker con moodle
└── .gitignore #Archivo para ignorar archivos que no se desean subir
```


---

##  Funcionalidades Implementadas

### servicios Activos

- [x] **/summarize**
- [x] **/quiz/generate** 
- [x] **/exercise/new**
- [x] **/evaluate**

---

## Tecnologías Usadas

- BLIP-2 
- OPEN AI
- GEMINI
- [Pydantic](https://docs.pydantic.dev/) – Validación de datos
- [Uvicorn](https://www.uvicorn.org/) – Servidor ASGI para FastAPI


---

## Configuración y Ejecución

## 1. Clona el proyecto
```bash
https://github.com/Abenavidese/hackathon-backend.git
```
### 2. Levantar Docker
Dentro de la carpeta

```bash
docker-compose up -d
```
Espere hasta que salga un mensaje de confirmación 

### 3. Descargar el modelo
Debido a problemas relacionados al peso del modelo este esta alojado externamente en google drive
Descargar desde el siguiente link
```bash
https://drive.google.com/drive/folders/18QREuHuFtVeuWUPTvGTe-7ZHvxAJdHfD?usp=share_link
```
luego agrega
```bash
cd hackathon_backend
```
mueve la carpeta descargada dentro del backend

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Correr moodle 
Una vez realizado todo puedes abrir tu instancia de moodle en
```bash
http://localhost:8000
```
### 6. Correr backend 
Correr backend
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 7. Descargar el pluggin
Debido a problemas relacionados al peso del plugin este esta alojado externamente en google drive
Descargar desde el siguiente link
```bash
https://drive.google.com/file/d/1vfXjRdy-mjrLmRSKA199MH8amkAaOsku/view?usp=sharing
```
- descompríme el archivo
luego navegamos a
```bash
cd moodle/mod
```
mueve la carpeta descargada dentro del mod

### 8. Actualizacion de direcciones ip
Dado que es un proyecto con ejecución unicamente local se tendran que modificar las direcciones ip si se desea correr

La dirección se debera modificar en 
```bash
moodle/mod/iafrance/view.php
```
### 9. Proyecto listo!

Una vez realizado estos pasos deberias ver una ventana que solcita actualizar el plugin, una vez actualizado
Dirigete a my courses ---> activa el modo de edicion --- > Add new activity or resource ---- > iafrance


## NOTA

Este proyecto originalmente estaba alojado en https://github.com/Abenavidese/blip-backend
pero debido a problemas tecnicos se cambio de repositorio
### Autor


- Anthony Alexander Benavides Erique























