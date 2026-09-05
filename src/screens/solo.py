from src.core.scene import Scene
from src.core.physics import create_space, update_space
from src.levels.map_loader import load_raw_map_data, get_random_map_name
from src.levels.level_factory import build_level
from src.systems.renderer import draw_entities

class SoloScene(Scene):
    def __init__(self):
        self.next = None
        self.space = create_space()
        
        raw_data = load_raw_map_data(get_random_map_name())
        self.walls, self.ball, self.hole = build_level(self.space, raw_data)

    def process_inputs(self, inputs):
        if inputs.escape: self.next = "MENU"

    def update(self):
        update_space(self.space)

    def render(self, screen):
        draw_entities(screen, self.walls, self.ball, self.hole)

    def get_next_scene(self):
        return self.next