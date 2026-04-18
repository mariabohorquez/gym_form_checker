# Pasos de Reproducibilidad

Sigue estos pasos para reproducir los resultados de este proyecto:

1.  **Preparar el entorno**: Instalar dependencias usando `uv` como se indica en el `README.md`.
2.  **Configurar credenciales**: Asegúrate de tener una cuenta en Roboflow y tu `API_KEY` guardada en el archivo `.env`.
3.  **Descargar y Explorar Datos**: Ejecuta secuencialmente las celdas en `notebooks/01_eda_dataset.ipynb` para descargar el dataset y generar los gráficos de distribución.
4.  **Entrenar Modelos YOLO**: Ejecuta `notebooks/02_model_training.ipynb` para hacer el fine-tuning de los clasificadores (YOLOv8n, YOLOv8s y YOLO11n). Se guardarán los pesos en la carpeta `runs/`.
5.  **Evaluar Motor y Generar Demo**: Copia o descarga los videos de muestra de Reddit en la carpeta `videos/` (ej. `squat_demo.mp4`). Ejecuta `notebooks/04_demo_evaluation.ipynb` para correr el pipeline end-to-end y obtener los videos procesados finales.
