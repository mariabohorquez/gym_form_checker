import os
from src.form_checker.video_processor import VideoProcessor

def generate_demos():
    print("Iniciando procesamiento de demostración con YOLO + MediaPipe...")
    os.makedirs('demo_results', exist_ok=True)

    # Use trained YOLO model for exercise classification
    model_path = 'notebooks/runs/cls/yolov8n/weights/best.pt'
    processor = VideoProcessor(cls_model_path=model_path)
    
    videos = [
        ("videos/squat_demo.mp4",           "demo_results/squat_demo_evaluated.mp4"),
        ("videos/squat_2.fhls-795.mp4",     "demo_results/squat2_demo_evaluated.mp4"),
        ("videos/pushup_demo.mp4",           "demo_results/pushup_demo_evaluated.mp4"),
        ("videos/deadlift_demo.mp4",         "demo_results/deadlift_old_evaluated.mp4"),
        ("videos/deadlift_new.fhls-830.mp4", "demo_results/deadlift_new_evaluated.mp4"),
    ]

    for in_path, out_path in videos:
        if os.path.exists(in_path):
            print(f"Procesando {in_path}...")
            try:
                processor.process_video(input_path=in_path, output_path=out_path)
                print(f"✅ Terminado: {out_path}")
            except Exception as e:
                print(f"Error en {ex_type}: {str(e)}")
        else:
            print(f"⚠️ Video no encontrado: {in_path}")

if __name__ == "__main__":
    generate_demos()
