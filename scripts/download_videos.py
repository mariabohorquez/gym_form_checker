import subprocess
import os
import sys

def download_video(url, output_name):
    print(f"Descargando {output_name}...")
    
    # Usar sys.executable para mantenernos en el venv
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "-S", "ext:mp4:m4a",
        "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
        "-o", f"videos/{output_name}",
        url
    ]
    subprocess.run(cmd)

if __name__ == "__main__":
    os.makedirs("videos", exist_ok=True)
    
    # Videos que encontramos en Reddit/YouTube (ejemplos muy directos de form check)
    videos = [
        # Pushup: r/formcheck o youtube shorts equivalentes
        ("https://www.youtube.com/shorts/qPpwfWnFvK4", "pushup_demo.mp4"),
        # Squat: form check clásico
        ("https://www.youtube.com/shorts/aJ5i12S8VfQ", "squat_demo.mp4"),
        # Deadlift: clásico deadlift form check
        ("https://www.youtube.com/shorts/O46D9j0YlWk", "deadlift_demo.mp4")
    ]
    
    for url, name in videos:
        download_video(url, name)
    print("Descarga completada!")
