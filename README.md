# Gym Form Checker

Prototipo funcional orientado a evaluar la técnica de ejercicios de gimnasio (Squat, Pushup, Deadlift) usando modelos de visión por computadora basados en deep learning. Proyecto Final para la materia Visión por Computadora II (CEIA).

## Arquitectura del Pipeline
1. **YOLOv8-cls (Fine-tuned)**: Clasifica el frame actual en una de 4 clases (Squat, Pushup, Deadlift, Standing).
2. **MediaPipe BlazePose**: Extrae 33 keypoints 3D de la persona.
3. **Motor de Forma**: Calcula los ángulos articulares y emite feedback en tiempo real (OK / MAL).

## Instalación y Configuración

```bash
# 1. Crear y activar entorno virtual
uv venv .venv
# source .venv/bin/activate  # en Linux/macOS
# .venv\Scripts\activate     # en Windows

# 2. Instalar dependencias
uv pip install -e .

# 3. Configurar variables de entorno
cp .env.example .env
# Editar .env y agregar la API KEY de Roboflow
```

## Estructura
- `notebooks/`: Análisis de datos (EDA), entrenamiento y evaluación del pipeline.
- `src/form_checker/`: Lógica central (cálculo de ángulos, reglas por ejercicio, conteo de reps).
- `paper/`: Documento final en formato IEEE.
