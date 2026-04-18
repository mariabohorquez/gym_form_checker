"""Reglas de evaluación para cada ejercicio.
Retornan 3 estados: 'OK', 'MAL', 'SIN_DATO'.
"""

def evaluate_squat(angles_dict, keypoints_visibility):
    """
    Evalúa la sentadilla (Squat).
    Espera un diccionario con los ángulos calculados, por ejemplo:
    - 'knee_angle': cadera -> rodilla -> tobillo
    - 'torso_angle': hombro -> cadera -> rodilla
    """
    # Lógica base (se expandirá luego)
    # 1. Verificar visibilidad de puntos clave
    if min(keypoints_visibility.values()) < 0.5:
        return 'SIN_DATO'
        
    # 2. Lógica de ángulos
    knee_angle = angles_dict.get('knee_angle', 180)
    
    if knee_angle <= 90:
        return 'OK'
    else:
        # Podría ser la fase concéntrica, manejado luego por el rep counter
        return 'MAL'

def evaluate_pushup(angles_dict, keypoints_visibility):
    """
    Evalúa la flexión (Push-up).
    """
    if min(keypoints_visibility.values()) < 0.5:
        return 'SIN_DATO'
        
    elbow_angle = angles_dict.get('elbow_angle', 180)
    alignment_angle = angles_dict.get('alignment_angle', 180)
    
    if elbow_angle <= 90 and alignment_angle > 165: # < 15° de desviación de 180
        return 'OK'
    return 'MAL'

def evaluate_deadlift(angles_dict, keypoints_visibility):
    """
    Evalúa el peso muerto (Deadlift).
    """
    if min(keypoints_visibility.values()) < 0.5:
        return 'SIN_DATO'
        
    back_angle = angles_dict.get('back_angle', 180)
    
    if back_angle > 155:
        return 'OK'
    return 'MAL'
