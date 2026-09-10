import math
from src.core.physics import reset_body_momentum

class Slingshot:
    def __init__(self, max_power=200, multiplier=5):
        self.aiming = False
        self.mouse_start = (0, 0)
        self.max_power = max_power
        self.multiplier = multiplier

    def start(self, pos, ball):
        self.aiming = True
        self.mouse_start = pos
        reset_body_momentum(ball.body)

    def get_aim_vector(self, current_pos):
        if not self.aiming: return None
        dx = self.mouse_start[0] - current_pos[0]
        dy = self.mouse_start[1] - current_pos[1]
        dist = math.hypot(dx, dy)
        if dist > self.max_power:
            return (dx / dist) * self.max_power, (dy / dist) * self.max_power
        return dx, dy

    def release(self, current_pos, ball):
        vector = self.get_aim_vector(current_pos)
        self.aiming = False
        if vector and math.hypot(*vector) > 10:
            force = (vector[0] * self.multiplier, vector[1] * self.multiplier)
            ball.body.apply_impulse_at_local_point(force)
            return True
        return False