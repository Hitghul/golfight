import math
from src.constants import HOLE_RADIUS, FPS

class Hole:
    def __init__(self, x, y, radius=HOLE_RADIUS):
        self.pos = (x, y)
        self.radius = radius
        self.influence_radius = radius * 3.0  # 45px autour du centre
        self.attraction_strength = 2800.0     # Accélération pour courber nettement la trajectoire
        self.capture_speed = 180.0            # Vitesse maximale pour être aspirée

    def apply_gravity(self, ball, dt=1.0 / FPS):
        """Applique l'effet de cuvette physique : dévie la trajectoire selon la vitesse."""
        dx = self.pos[0] - ball.body.position.x
        dy = self.pos[1] - ball.body.position.y
        dist = math.hypot(dx, dy)

        if 0 < dist < self.influence_radius:
            nx, ny = dx / dist, dy / dist

            # Pente non-linéaire : très forte attraction près du bord du trou
            intensity = 1.0 - (dist / self.influence_radius)
            accel = self.attraction_strength * (intensity ** 1.5)

            # Application directe sur la vitesse (évite d'être réinitialisé par les substeps de Pymunk)
            vx = ball.body.velocity.x + (nx * accel * dt)
            vy = ball.body.velocity.y + (ny * accel * dt)

            # Amortissement sur la lèvre du trou (perte d'énergie de la cuvette)
            if dist < self.radius + 5:
                damping = max(0.0, 1.0 - (2.0 * dt))
                vx *= damping
                vy *= damping

            ball.body.velocity = (vx, vy)

    def is_ball_in(self, ball):
        """Détermine si la balle est tombée au fond du trou."""
        dist = math.dist(ball.pos, self.pos)
        return dist < (self.radius * 0.75) and ball.body.velocity.length < self.capture_speed