import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import cv2
from pathlib import Path
import pandas as pd

load_dotenv()
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)

def run_eda():
    dataset_path = Path('notebooks/Exercise-Frame-Labelling-8')
    splits = ['train', 'val', 'test']
    classes = [d for d in os.listdir(dataset_path / 'train') if os.path.isdir(dataset_path / 'train' / d)]
    
    os.makedirs('data', exist_ok=True)

    data_counts = {split: {cls: 0 for cls in classes} for split in splits}
    for split in splits:
        for cls in classes:
            cls_path = dataset_path / split / cls
            if cls_path.exists():
                data_counts[split][cls] = len(list(cls_path.glob('*.jpg')))

    df_counts = pd.DataFrame(data_counts)
    df_counts['total'] = df_counts.sum(axis=1)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=df_counts.index, y=df_counts['total'], palette='viridis')
    plt.title('Distribución Total de Clases (Corregida)')
    plt.xlabel('Clase')
    plt.ylabel('Cantidad de Imágenes')
    plt.savefig('data/class_distribution.png')
    plt.close()

    df_counts_splits = df_counts.drop(columns=['total'])
    df_counts_splits.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='viridis')
    plt.title('Distribución de Clases por Split (Corregida)')
    plt.xlabel('Clase')
    plt.ylabel('Cantidad de Imágenes')
    plt.legend(title='Split')
    plt.savefig('data/split_distribution.png')
    plt.close()
    
    # Muestras
    fig, axes = plt.subplots(len(classes), 5, figsize=(15, 3 * len(classes)))
    for i, cls in enumerate(classes):
        cls_path = dataset_path / 'train' / cls
        images = list(cls_path.glob('*.jpg'))
        samples = np.random.choice(images, min(5, len(images)), replace=False) if len(images) > 0 else []
        for j, img_path in enumerate(samples):
            img = cv2.imread(str(img_path))
            if img is not None:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                axes[i, j].imshow(img)
            axes[i, j].axis('off')
            if j == 0:
                axes[i, j].set_title(cls, fontsize=14, loc='left')
    plt.tight_layout()
    plt.savefig('data/sample_images.png')
    plt.close()
    
    print("EDA re-generado exitosamente. Gráficos actualizados en data/.")

if __name__ == '__main__':
    run_eda()
