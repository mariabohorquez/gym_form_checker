# Gym Form Checker

Prototipo funcional que analiza la técnica de ejercicios de gimnasio (Sentadilla, Flexión, Peso Muerto) en tiempo real usando visión por computadora. Proyecto Final — Visión por Computadora II, CEIA, Universidad de Buenos Aires.

## Demo

https://github.com/mariabohorquez/gym_form_checker/blob/master/demo_results/squat_demo_evaluated_h264.mp4

Ver todos los videos procesados en [`demo_results/`](demo_results/) con overlay de forma, estado y conteo de repeticiones.

## Arquitectura del Pipeline

1. **YOLOv8-cls / YOLO11n-cls (Fine-tuned):** Clasifica el frame en una de 4 clases (Squat, Pushup, Deadlift, Standing). Entrenado sobre el dataset Exercise Frame Labelling v8 — 99.4% Top-1 accuracy.
2. **MediaPipe BlazePose:** Extrae 33 keypoints 3D del cuerpo en tiempo real.
3. **Motor Biomecánico:** Calcula ángulos articulares clave y aplica reglas deterministas por ejercicio. Emite feedback en 3 estados: `OK`, `MAL`, `SIN_DATO`.
4. **Contador de Repeticiones:** Detecta transiciones de ángulo para contar reps válidas automáticamente.

## Instalación

Requiere Python 3.10+ y [uv](https://github.com/astral-sh/uv).

```bash
# 1. Clonar el repositorio
git clone https://github.com/magabohorquez/gym_form_checker
cd gym_form_checker

# 2. Crear entorno virtual e instalar dependencias
uv venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows

uv pip install -e .
```

## Dataset

Se utiliza el dataset [Exercise Frame Labelling v8](https://universe.roboflow.com/roboflow-100/exercise-frame-labelling) de Roboflow Universe.

Para descargarlo, agregar una API Key de Roboflow en `.env`:

```env
ROBOFLOW_API_KEY=tu_api_key_aqui
```

Luego ejecutar el notebook `notebooks/01_eda_dataset.ipynb`, que descarga el dataset automáticamente.

## Uso

```bash
# Correr la demo sobre los 3 videos de ejemplo
python scripts/run_demo.py

# Regenerar gráficos del EDA
python scripts/run_eda.py

# Reentrenar los modelos YOLO
python scripts/train_all.py
```

## Estructura del Proyecto

```
gym_form_checker/
├── src/form_checker/        # Lógica central del pipeline
│   ├── video_processor.py   # Pipeline principal (YOLO + MediaPipe)
│   ├── form_rules.py        # Reglas biomecánicas por ejercicio
│   ├── rep_counter.py       # Contador de repeticiones
│   └── angle_calculator.py  # Cálculo de ángulos articulares
├── notebooks/               # EDA y entrenamiento
│   ├── 01_eda_dataset.ipynb # Análisis exploratorio del dataset
│   └── 02_model_training.ipynb # Fine-tuning de clasificadores YOLO
├── paper/                   # Documento IEEE
├── presentation/            # Slides + guion de presentación
├── scripts/                 # Scripts utilitarios
├── data/                    # Gráficos del EDA
└── demo_results/            # Videos de demostración procesados
```

## Paper

El informe completo en formato IEEE está disponible en `paper/gym_form_checker.pdf`.

## Autor

María Gabriela Bohórquez
