import cv2
import numpy as np

try:
    from ultralytics import YOLO
except ImportError:
    YOLO = None

from .angle_calculator import calc_angle, extract_keypoints
from .form_rules import evaluate_squat, evaluate_pushup, evaluate_deadlift
from .rep_counter import RepCounter
from .mediapipe_compat import Solutions, DrawingModule

class VideoProcessor:
    def __init__(self, cls_model_path=None):
        """
        Inicializa el procesador de video con compatibilidad MediaPipe 0.10.
        """
        self.mp_pose = Solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mp_drawing = DrawingModule
        
        self.cls_model = None
        if cls_model_path and YOLO is not None:
            self.cls_model = YOLO(cls_model_path)
            
        self.rep_counters = {
            'squat': RepCounter(),
            'pushup': RepCounter(),
            'deadlift': RepCounter()
        }

    def process_video(self, input_path, output_path, forced_exercise=None):
        """
        Procesa el video frame a frame.
        forced_exercise: 'squat', 'pushup' o 'deadlift'. Si es None, usa YOLO para predecir.
        """
        # Reset counters and state for each new video
        for rc in self.rep_counters.values():
            rc.count = 0
            rc.state = "up"
            rc.angle_buffer = []

        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            print(f"Error abriendo video {input_path}")
            return
            
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        frames_processed = 0
        ok_frames = 0
        alerts = []

        prev_knee_angle = None  # For squat direction detection

        # Smoothing buffer for exercise classification
        classification_buffer = []
        smooth_window = 90
        committed_exercise = None   # Exercise we've locked onto
        committed_frames = 0        # Consecutive frames the committed exercise has been dominant

        # Smoothing buffer for form status (majority voting over 10 frames)
        form_status_buffer = []
        form_smooth_window = 10

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frames_processed += 1

            # 1. Clasificación del ejercicio (si no está forzado)
            current_exercise = forced_exercise
            if current_exercise is None and self.cls_model is not None:
                results_cls = self.cls_model(frame, verbose=False)
                top1_idx = results_cls[0].probs.top1
                current_exercise_pred = results_cls[0].names[top1_idx].lower()

                # Map to exercise type
                if 'squat' in current_exercise_pred: pred_exercise = 'squat'
                elif 'push' in current_exercise_pred: pred_exercise = 'pushup'
                elif 'dead' in current_exercise_pred: pred_exercise = 'deadlift'
                else: pred_exercise = 'other'

                # Add to smoothing buffer
                classification_buffer.append(pred_exercise)
                if len(classification_buffer) > smooth_window:
                    classification_buffer.pop(0)

                from collections import Counter
                votes = Counter(classification_buffer)
                majority = votes.most_common(1)[0][0]
                majority_pct = votes[majority] / len(classification_buffer)

                # Sticky classification: once committed, require 70% supermajority to switch
                if committed_exercise is None:
                    # Not yet committed — commit once majority holds for 30 frames
                    if majority_pct >= 0.5 and len(classification_buffer) >= 30:
                        committed_exercise = majority
                        committed_frames = 0
                elif majority == committed_exercise:
                    committed_frames += 1
                else:
                    # Different majority — only switch if it has 70% of votes
                    if majority_pct >= 0.70:
                        committed_exercise = majority
                        committed_frames = 0

                current_exercise = committed_exercise or majority

            if current_exercise is None:
                current_exercise = 'squat'
                
            # 2. Pose Estimation con MediaPipe
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(image_rgb)

            form_status = 'SIN_DATO'
            coaching_msg = ''
            reps = 0

            if results.pose_landmarks:
                self.mp_drawing.draw_landmarks(frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)

                keypoints = extract_keypoints(results.pose_landmarks)

                # Nombres de landmarks basados en mediapipe pose
                # 11: left_shoulder, 12: right_shoulder
                # 23: left_hip, 24: right_hip
                # 25: left_knee, 26: right_knee
                # 27: left_ankle, 28: right_ankle
                # 13: left_elbow, 14: right_elbow
                # 15: left_wrist, 16: right_wrist

                def p(idx):
                    return [keypoints[idx]['x'], keypoints[idx]['y']]
                def v(idx):
                    return keypoints[idx]['visibility']

                angles = {}
                visibility = {}
                display_angles = {}  # Angles to show on screen

                if current_exercise == 'squat':
                    try:
                        k_l = calc_angle(p(23), p(25), p(27))
                        k_r = calc_angle(p(24), p(26), p(28))
                        t_l = calc_angle(p(11), p(23), p(25))

                        angles['knee_angle'] = min(k_l, k_r)
                        angles['torso_angle'] = t_l

                        visibility['knee'] = min(v(23), v(25), v(27))
                        visibility['hip'] = min(v(11), v(23), v(25))

                        display_angles = {
                            'Rodilla': angles['knee_angle'],
                            'Torso': angles['torso_angle'],
                        }

                        form_status, coaching_msg = evaluate_squat(angles, visibility)
                        # Suppress "go lower" cues when person is rising
                        going_up = (prev_knee_angle is not None and angles['knee_angle'] > prev_knee_angle + 2)
                        if going_up and form_status in ('MEJORAR', 'MAL') and 'baja' in coaching_msg.lower():
                            coaching_msg = 'Subiendo...'
                        prev_knee_angle = angles['knee_angle']
                        reps = self.rep_counters['squat'].update_squat(angles['knee_angle'])
                    except KeyError:
                        form_status = 'SIN_DATO'

                elif current_exercise == 'pushup':
                    try:
                        e_angle = calc_angle(p(11), p(13), p(15))
                        # Use knee instead of ankle — ankle often invisible when lying down
                        a_angle = calc_angle(p(11), p(23), p(25))

                        angles['elbow_angle'] = e_angle
                        angles['alignment_angle'] = a_angle

                        visibility['elbow'] = min(v(11), v(13), v(15))
                        visibility['alignment'] = min(v(11), v(23), v(25))

                        display_angles = {
                            'Codo': angles['elbow_angle'],
                            'Alineacion': angles['alignment_angle'],
                        }

                        form_status, coaching_msg = evaluate_pushup(angles, visibility)
                        reps = self.rep_counters['pushup'].update_pushup(angles['elbow_angle'])
                    except KeyError:
                        form_status = 'SIN_DATO'

                elif current_exercise == 'deadlift':
                    try:
                        b_angle = calc_angle(p(11), p(23), p(25))
                        # Spine lean: horizontal distance shoulder-hip (detects rounded lower back)
                        spine_lean = abs(keypoints[11]['x'] - keypoints[23]['x'])

                        angles['back_angle'] = b_angle
                        angles['spine_lean'] = spine_lean
                        visibility['back'] = min(v(11), v(23), v(25))

                        display_angles = {
                            'Espalda': b_angle,
                            'Lean': spine_lean * 100,  # scale to % for readability
                        }

                        form_status, coaching_msg = evaluate_deadlift(angles, visibility)
                        reps = self.rep_counters['deadlift'].update_deadlift(b_angle)
                    except KeyError:
                        form_status = 'SIN_DATO'
                else:
                    reps = 0

            # Smooth form status using majority voting (ignore SIN_DATO)
            if form_status != 'SIN_DATO':
                form_status_buffer.append((form_status, coaching_msg))
                if len(form_status_buffer) > form_smooth_window:
                    form_status_buffer.pop(0)

                # Use majority vote from buffer (vote on status only)
                from collections import Counter
                votes = Counter(s for s, _ in form_status_buffer)
                form_status = votes.most_common(1)[0][0]
                # Pick coaching message from the most recent frame with the winning status
                for s, m in reversed(form_status_buffer):
                    if s == form_status:
                        coaching_msg = m
                        break

            if form_status == 'OK':
                ok_frames += 1
                color = (0, 255, 0)    # Green
            elif form_status == 'MEJORAR':
                color = (0, 200, 255)  # Orange-yellow
            elif form_status == 'MAL':
                color = (0, 0, 255)    # Red
            elif form_status == 'NEUTRAL':
                color = (200, 200, 200)  # Light gray
            else:
                color = (128, 128, 128)  # Gray for SIN_DATO

            # Renderizado principal
            cv2.putText(frame, f"Ej: {current_exercise.upper()}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, f"Forma: {form_status}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            cv2.putText(frame, f"Reps: {reps}", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            if coaching_msg:
                cv2.putText(frame, coaching_msg, (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

            # Angulos en tiempo real
            h_frame = frame.shape[0]
            for i, (label, val) in enumerate(display_angles.items()):
                y_pos = h_frame - 20 - (i * 35)
                cv2.putText(frame, f"{label}: {val:.1f}", (10, y_pos),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 2)

            out.write(frame)
            
        cap.release()
        out.release()
        
        print(f"Video guardado: {output_path}")
        print(f"Frames totales: {frames_processed}, % OK form: {(ok_frames/frames_processed)*100:.1f}%")
        return {
            'frames': frames_processed,
            'ok_frames': ok_frames,
            'exercise': current_exercise
        }

    def _draw_landmarks_solutions(self, frame, pose_landmarks):
        """Draw landmarks using old solutions API"""
        self.mp_drawing.draw_landmarks(frame, pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
        return frame

    def _draw_landmarks_tasks(self, frame, pose_landmarks):
        """Draw landmarks using new tasks API"""
        h, w, c = frame.shape
        for landmark in pose_landmarks.landmark:
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
        return frame
