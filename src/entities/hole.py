import math
from src.constants import HOLE_RADIUS

class Hole:
    def __init__(self, x, y):
        self.pos = (x, y)

    def is_ball_in(self, ball):
        return math.dist(ball.pos, self.pos) < HOLE_RADIUS and ball.body.velocity.length < 100