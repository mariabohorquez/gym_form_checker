import os
import torch
from ultralytics import YOLO

def train():
    dataset_path = os.path.abspath('notebooks/Exercise-Frame-Labelling-8')
    print("CUDA disponible:", torch.cuda.is_available())
    
    models = ['yolov8n', 'yolov8s', 'yolo11n']
    
    for model_name in models:
        print(f"\\n{'='*50}\\nIniciando entrenamiento de {model_name}-cls\\n{'='*50}")
        model = YOLO(f"{model_name}-cls.pt")  # load a pretrained model
        model.train(
            data=dataset_path,
            epochs=50,
            imgsz=224,
            device=0 if torch.cuda.is_available() else 'cpu',
            project='notebooks/runs/cls',
            name=model_name,
            exist_ok=True,
            batch=16, # Reducido para evitar el WinError 1455 sin perder velocidad
            workers=2 # Usamos 2 workers para mantener buen tiempo de entrenamiento sin colapsar la RAM de Windows
        )

if __name__ == "__main__":
    train()
