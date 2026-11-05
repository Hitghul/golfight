import pygame
from src.constants import SAND_DAMPING
from src.core.physics import reset_body_momentum

class Zone:
    def __init__(self, x, y, w, h, zone_type="generic"):
        self.rect = pygame.Rect(x, y, w, h)
        self.zone_type = zone_type

    def contains(self, pos):
        return self.rect.collidepoint(pos)


class SandZone(Zone):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h, "sand")

    def apply(self, ball, dt):
        if self.contains(ball.pos):
            factor = max(0.0, 1.0 - (SAND_DAMPING * dt))
            ball.body.velocity = (ball.body.velocity.x * factor, ball.body.velocity.y * factor)
            return "SAND_DRAG"
        return None


class WaterZone(Zone):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h, "water")

    def apply(self, ball, dt):
        if self.contains(ball.pos):
            reset_body_momentum(ball.body)
            target_pos = getattr(ball, "last_safe_pos", ball.pos)
            ball.body.position = target_pos
            if hasattr(ball, "penalties"):
                ball.penalties += 1
            return "WATER_HAZARD"
        return None

