import pymunk
from src.constants import BALL_RADIUS, BALL_MASS

class Ball:
    def __init__(self, space, x, y):
        self.body = pymunk.Body(BALL_MASS, pymunk.moment_for_circle(BALL_MASS, 0, BALL_RADIUS))
        self.body.position = (x, y)
        self.shape = pymunk.Circle(self.body, BALL_RADIUS)
        self.shape.elasticity = 0.85
        self.shape.friction = 0.5
        space.add(self.body, self.shape)

    @property
    def pos(self):
        return (int(self.body.position.x), int(self.body.position.y))

    def is_stopped(self, threshold=5):
        return self.body.velocity.length < threshold