"""Reglas de evaluación para cada ejercicio.
Retornan tupla (estado, mensaje_coaching).
Estados: 'OK', 'MEJORAR', 'MAL', 'SIN_DATO', 'NEUTRAL'
"""

def evaluate_squat(angles_dict, keypoints_visibility):
    if min(keypoints_visibility.values()) < 0.4:
        return 'SIN_DATO', ''

    knee_angle = angles_dict.get('knee_angle', 180)
    torso_angle = angles_dict.get('torso_angle', 90)

    # Neutral zone: person is standing between reps — don't penalize
    if knee_angle > 130:
        return 'NEUTRAL', 'Preparando...'

    # OK: deep squat + upright torso
    if knee_angle <= 90 and (45 <= torso_angle <= 100):
        return 'OK', 'Buena tecnica!'

    # MEJORAR
    if knee_angle <= 105 and (40 <= torso_angle <= 110):
        if knee_angle > 90:
            return 'MEJORAR', 'Baja un poco mas'
        return 'MEJORAR', 'Controla el torso'

    # MAL — specific coaching
    if knee_angle > 90:
        return 'MAL', 'Dobla mas las rodillas'
    if torso_angle < 45:
        return 'MAL', 'Levanta el torso'
    if torso_angle > 100:
        return 'MAL', 'No te inclines tanto'
    return 'MAL', 'Corrige la postura'


def evaluate_pushup(angles_dict, keypoints_visibility):
    if min(keypoints_visibility.values()) < 0.3:
        return 'SIN_DATO', ''

    elbow_angle = angles_dict.get('elbow_angle', 180)
    alignment_angle = angles_dict.get('alignment_angle', 180)

    # Neutral zone: arms extended at top
    if elbow_angle > 150:
        return 'NEUTRAL', 'Posicion inicial'

    # OK: good depth + straight body
    if elbow_angle < 110 and alignment_angle > 150:
        return 'OK', 'Buena tecnica!'

    # MEJORAR
    if elbow_angle < 125 and alignment_angle > 140:
        if elbow_angle >= 110:
            return 'MEJORAR', 'Baja mas el pecho'
        return 'MEJORAR', 'Alinea la cadera'

    # MAL — specific coaching
    if elbow_angle >= 125:
        return 'MAL', 'Baja mas el pecho'
    if alignment_angle <= 140:
        return 'MAL', 'Caderas caidas'
    return 'MAL', 'Corrige la postura'


def evaluate_deadlift(angles_dict, keypoints_visibility):
    if min(keypoints_visibility.values()) < 0.4:
        return 'SIN_DATO', ''

    back_angle = angles_dict.get('back_angle', 180)
    spine_lean = angles_dict.get('spine_lean', 0)

    # Rounded lower back detection
    if spine_lean > 0.20 and back_angle < 155:
        return 'MAL', 'Espalda redondeada!'

    # OK: full extension + neutral spine
    if back_angle > 155 and spine_lean <= 0.15:
        return 'OK', 'Buena extension!'

    # MEJORAR
    if back_angle > 140:
        return 'MEJORAR', 'Extiende la cadera'

    # MAL
    if back_angle <= 140:
        return 'MAL', 'Levanta el torso'
    return 'MAL', 'Corrige la postura'
