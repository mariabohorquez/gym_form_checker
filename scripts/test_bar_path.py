"""Quick test: bar path tracking on one deadlift video.
Writes to demo_results/deadlift_barpath_test.mp4 — doesn't touch anything else.
Bar position = midpoint of both wrists (MediaPipe landmarks 15 & 16).
"""
import cv2
import numpy as np
from collections import deque
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.form_checker.mediapipe_compat import Solutions, DrawingModule
from src.form_checker.angle_calculator import extract_keypoints

TRAIL_LENGTH = 60   # frames of trail to keep
INPUT  = "videos/deadlift_new.fhls-830.mp4"
OUTPUT = "demo_results/deadlift_barpath_test.mp4"

mp_pose = Solutions.pose
pose    = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(INPUT)
w   = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h   = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
out = cv2.VideoWriter(OUTPUT, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))

trail = deque(maxlen=TRAIL_LENGTH)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb     = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)

    if results.pose_landmarks:
        DrawingModule.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        kp = extract_keypoints(results.pose_landmarks)

        lw_vis = kp[15]['visibility']
        rw_vis = kp[16]['visibility']

        if lw_vis > 0.4 and rw_vis > 0.4:
            bx = int(((kp[15]['x'] + kp[16]['x']) / 2) * w)
            by = int(((kp[15]['y'] + kp[16]['y']) / 2) * h)
            trail.append((bx, by))

    # Draw fading trail
    for i, (px, py) in enumerate(trail):
        alpha = (i + 1) / len(trail)           # 0 → faded, 1 → bright
        radius = max(3, int(6 * alpha))
        # Cyan trail, fading to darker
        color = (int(255 * alpha), int(200 * alpha), 0)
        cv2.circle(frame, (px, py), radius, color, -1)

    # Label
    cv2.putText(frame, "Bar Path (wrist midpoint)", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    out.write(frame)

cap.release()
out.release()
print(f"Done: {OUTPUT}")
