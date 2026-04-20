"""Módulo para el conteo de repeticiones con smoothing y hysteresis."""

class RepCounter:
    def __init__(self, smooth_window=5):
        self.count = 0
        self.state = "up"
        self.smooth_window = smooth_window
        self.angle_buffer = []
        self.last_rep_frame = -100

    def _smooth_angle(self, angle):
        """Smooth angle using moving average"""
        self.angle_buffer.append(angle)
        if len(self.angle_buffer) > self.smooth_window:
            self.angle_buffer.pop(0)
        return sum(self.angle_buffer) / len(self.angle_buffer)

    def update_squat(self, knee_angle):
        """Squat: count rep when going down (<85°) then back up (>130°)"""
        smooth_angle = self._smooth_angle(knee_angle)

        # Hysteresis thresholds to avoid noise
        if smooth_angle < 95 and self.state == "up":
            self.state = "down"
        elif smooth_angle > 130 and self.state == "down":
            self.state = "up"
            self.count += 1

        return self.count

    def update_pushup(self, elbow_angle):
        """Pushup: count rep when going down (<80°) then back up (>160°)"""
        smooth_angle = self._smooth_angle(elbow_angle)

        if smooth_angle < 80 and self.state == "up":
            self.state = "down"
        elif smooth_angle > 160 and self.state == "down":
            self.state = "up"
            self.count += 1

        return self.count

    def update_deadlift(self, hip_angle):
        """Deadlift: count rep when going down (<120°) then back up (>150°)"""
        smooth_angle = self._smooth_angle(hip_angle)

        if smooth_angle < 120 and self.state == "up":
            self.state = "down"
        elif smooth_angle > 150 and self.state == "down":
            self.state = "up"
            self.count += 1

        return self.count
