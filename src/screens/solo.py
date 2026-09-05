from src.core.scene import Scene
from src.core.physics import create_space, update_space
from src.entities.ball import Ball
from src.entities.wall import Wall
from src.entities.hole import Hole
from src.systems.renderer import draw_entities

class SoloScene(Scene):
    def __init__(self):
        self.next = None
        self.space = create_space()
        self.space.gravity = (0, 900)  # test de gravité
        
        # test
        self.ball = Ball(self.space, 512, 100)
        self.hole = Hole(800, 500)
        self.walls = [Wall(self.space, (200, 600), (824, 600))]

    def process_inputs(self, inputs):
        if inputs.escape: self.next = "MENU"

    def update(self):
        update_space(self.space)

    def render(self, screen):
        draw_entities(screen, self.walls, self.ball, self.hole)

    def get_next_scene(self):
        return self.next