import pymunk
from src.constants import FPS

def create_space():
    space = pymunk.Space()
    space.gravity = (0, 0)
    space.damping = 0.4
    return space

def update_space(space, substeps=3):
    dt = 1.0 / FPS
    for _ in range(substeps):
        space.step(dt / substeps)

def reset_body_momentum(body):
    body.velocity = (0, 0)
    body.angular_velocity = 0
    body.angle = 0