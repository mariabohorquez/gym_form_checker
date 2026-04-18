"""Módulo para el conteo de repeticiones utilizando detección de picos en los ángulos."""

class RepCounter:
    def __init__(self):
        self.count = 0
        self.state = "up"  # Puede ser "up" o "down" dependiendo del ejercicio
        self.history = []
        
    def update_squat(self, knee_angle):
        """
        Cuenta repeticiones para la sentadilla basándose en el ángulo de la rodilla.
        La rodilla empieza extendida (~180°), baja (<90°) y vuelve a subir.
        """
        if knee_angle < 90:
            if self.state == "up":
                self.state = "down"
        
        if knee_angle > 160:
            if self.state == "down":
                self.state = "up"
                self.count += 1
                
        return self.count

    def update_pushup(self, elbow_angle):
        """
        Cuenta repeticiones para pushup basándose en el codo.
        """
        if elbow_angle < 90:
            if self.state == "up":
                self.state = "down"
                
        if elbow_angle > 160:
            if self.state == "down":
                self.state = "up"
                self.count += 1
                
        return self.count

    def update_deadlift(self, hip_angle):
        """
        Cuenta repeticiones para el deadlift basándose en la extensión de la cadera.
        """
        # A desarrollar en la etapa 3
        pass
