"""Init del paquete form_checker."""
from .angle_calculator import calc_angle, extract_keypoints
from .form_rules import evaluate_squat, evaluate_pushup, evaluate_deadlift
from .rep_counter import RepCounter

__all__ = [
    'calc_angle',
    'extract_keypoints',
    'evaluate_squat',
    'evaluate_pushup',
    'evaluate_deadlift',
    'RepCounter'
]
