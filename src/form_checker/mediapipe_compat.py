"""Compatibility layer to use MediaPipe 0.10 with old solutions-like API"""
import cv2
import mediapipe as mp
from mediapipe.tasks.python import vision


class PoseLandmark:
    def __init__(self, landmark):
        self.x = landmark.x
        self.y = landmark.y
        self.z = landmark.z
        self.visibility = landmark.visibility if hasattr(landmark, 'visibility') else 1.0


class PoseLandmarksResult:
    def __init__(self, landmarks):
        self.landmark = [PoseLandmark(lm) for lm in landmarks]


class DrawingUtils:
    @staticmethod
    def draw_landmarks(frame, pose_landmarks, connections):
        """Draw pose landmarks and skeleton connections on frame"""
        h, w, c = frame.shape
        landmarks = pose_landmarks.landmark

        # Draw connections (skeleton lines)
        if connections:
            for connection in connections:
                start_idx, end_idx = connection
                if start_idx < len(landmarks) and end_idx < len(landmarks):
                    start = landmarks[start_idx]
                    end = landmarks[end_idx]
                    start_x, start_y = int(start.x * w), int(start.y * h)
                    end_x, end_y = int(end.x * w), int(end.y * h)
                    if (0 <= start_x < w and 0 <= start_y < h and
                        0 <= end_x < w and 0 <= end_y < h):
                        cv2.line(frame, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)

        # Draw landmarks (joints)
        for landmark in landmarks:
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            if 0 <= x < w and 0 <= y < h:
                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
        return frame


class PoseCompat:
    """Wraps MediaPipe 0.10 tasks to look like old solutions.Pose"""

    def __init__(self, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.landmarker = None
        self.available = False

        try:
            from mediapipe.tasks.python.core.base_options import BaseOptions
            from mediapipe import tasks
            import urllib.request
            import os

            # Download model if not present
            model_path = '/tmp/pose_landmarker.task'
            if not os.path.exists(model_path):
                print("Downloading PoseLandmarker model...")
                urls = [
                    "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task",
                    "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_heavy/float16/1/pose_landmarker_heavy.task",
                ]
                for url in urls:
                    try:
                        urllib.request.urlretrieve(url, model_path)
                        version = "lite" if "lite" in url else "heavy"
                        print(f"✓ {version} model downloaded")
                        break
                    except Exception as e:
                        continue
                else:
                    raise RuntimeError("Could not download pose_landmarker model from any source")

            options = vision.PoseLandmarkerOptions(
                base_options=BaseOptions(model_asset_path=model_path),
                running_mode=vision.RunningMode.IMAGE)
            self.landmarker = vision.PoseLandmarker.create_from_options(options)
            self.available = True
            print("✓ PoseLandmarker initialized successfully")
        except Exception as e:
            print(f"⚠ MediaPipe pose landmarker not available ({type(e).__name__}: {str(e)[:100]})")
            self.available = False

    def process(self, image_rgb):
        """Process image and return landmarks in old API format"""
        class Result:
            pose_landmarks = None

        if not self.available or self.landmarker is None:
            return Result()

        try:
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
            result = self.landmarker.detect(mp_image)

            if result.pose_landmarks:
                Result.pose_landmarks = PoseLandmarksResult(result.pose_landmarks[0])

            return Result()
        except Exception as e:
            return Result()


class Solutions:
    """Fake mp.solutions module"""

    class pose:
        # MediaPipe BlazePose 33-point skeleton connections
        POSE_CONNECTIONS = [
            (0, 1), (1, 2), (2, 3), (3, 7), (0, 4), (4, 5), (5, 6), (6, 8),
            (9, 10), (11, 12), (11, 13), (13, 15), (15, 17), (15, 19), (15, 21),
            (17, 19), (12, 14), (14, 16), (16, 18), (16, 20), (16, 22), (18, 20),
            (11, 23), (12, 24), (23, 24), (23, 25), (24, 26), (25, 27), (26, 28),
            (27, 29), (28, 30), (29, 31), (30, 32),
        ]

        @staticmethod
        def Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5):
            return PoseCompat(min_detection_confidence, min_tracking_confidence)


class DrawingModule:
    @staticmethod
    def draw_landmarks(frame, pose_landmarks, connections):
        """Draw landmarks on frame"""
        return DrawingUtils.draw_landmarks(frame, pose_landmarks, connections)
