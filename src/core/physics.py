import pymunk
from src.constants import FPS, COLLISION_TYPE_BALL

def setup_ball_collision_handler(space, on_ball_collision=None):
    def pre_solve(arbiter, space_obj, data):
        # Ball-ball restitution
        arbiter.elasticity = 0.90
        arbiter.friction = 0.35

    def post_solve(arbiter, space_obj, data):
        impulse = arbiter.total_impulse.length
        if impulse > 1.0:
            shape_a, shape_b = arbiter.shapes
            ball_a = getattr(shape_a, "ball", None)
            ball_b = getattr(shape_b, "ball", None)
            if ball_a is not None:
                ball_a.last_hit_impulse = impulse
            if ball_b is not None:
                ball_b.last_hit_impulse = impulse
            if on_ball_collision and callable(on_ball_collision):
                on_ball_collision(ball_a, ball_b, impulse)

    space.on_collision(
        COLLISION_TYPE_BALL,
        COLLISION_TYPE_BALL,
        pre_solve=pre_solve,
        post_solve=post_solve
    )

def create_space(on_ball_collision=None):
    space = pymunk.Space()
    space.gravity = (0, 0)
    space.damping = 0.4
    setup_ball_collision_handler(space, on_ball_collision)
    return space

def update_space(space, substeps=3):
    dt = 1.0 / FPS
    for _ in range(substeps):
        space.step(dt / substeps)

def reset_body_momentum(body):
    body.velocity = (0, 0)
    body.angular_velocity = 0
    body.angle = 0