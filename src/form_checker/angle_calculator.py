"""Módulo para calcular ángulos usando puntos (x, y) de MediaPipe."""
import numpy as np

def calc_angle(a, b, c):
    """
    Calcula el ángulo (en grados) en la articulación 'b' formada por los puntos a, b y c.
    
    Args:
        a, b, c: Tuplas o listas [x, y] que representan los keypoints.
                 'b' es el vértice del ángulo.
    
    Returns:
        float: Ángulo en grados entre 0 y 180.
    """
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
        
    return angle

def extract_keypoints(pose_landmarks):
    """
    Extrae los landmarks de MediaPipe y los convierte en un diccionario
    con nombres amigables (ej: 'left_shoulder', 'right_knee').
    """
    # MediaPipe Pose tiene 33 landmarks. Mapearemos los índices más relevantes.
    # Esta es la base que usaremos luego en los notebooks.
    # Ref: https://developers.google.com/mediapipe/solutions/vision/pose_landmarker
    keypoints = {}
    if pose_landmarks:
        for idx, landmark in enumerate(pose_landmarks.landmark):
            keypoints[idx] = {
                'x': landmark.x,
                'y': landmark.y,
                'z': landmark.z,
                'visibility': landmark.visibility
            }
    return keypoints
