import pymunk
from src.constants import BALL_RADIUS, BALL_MASS, SHOOT_SPEED_THRESHOLD, COLLISION_TYPE_BALL, BALL_COLOR

class Ball:
    def __init__(self, space, x, y, color=BALL_COLOR, player_id=1):
        self.space = space
        self.color = color
        self.player_id = player_id
        self.last_hit_impulse = 0.0
        
        self.body = pymunk.Body(BALL_MASS, pymunk.moment_for_circle(BALL_MASS, 0, BALL_RADIUS))
        self.body.position = (x, y)
        self.body.velocity_func = self._update_velocity
        self.shape = pymunk.Circle(self.body, BALL_RADIUS)
        self.shape.elasticity = 0.90
        self.shape.friction = 0.4
        self.shape.collision_type = COLLISION_TYPE_BALL
        self.shape.ball = self
        space.add(self.body, self.shape)

    def _update_velocity(self, body, gravity, damping, dt):
        pymunk.Body.update_velocity(body, gravity, damping, dt)
        if body.velocity.length < 2:
            body.velocity = (0, 0)

    @property
    def speed(self):
        return self.body.velocity.length

    @property
    def pos(self):
        return (int(self.body.position.x), int(self.body.position.y))

    def is_stopped(self, threshold=SHOOT_SPEED_THRESHOLD):
        return self.speed <= threshold