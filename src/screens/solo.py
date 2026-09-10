from src.core.scene import Scene
from src.core.physics import create_space, update_space
from src.levels.map_loader import load_raw_map_data, get_random_map_name
from src.levels.level_factory import build_level
from src.systems.slingshot import Slingshot
from src.systems.renderer import draw_entities, draw_aim_line

class SoloScene(Scene):
    def __init__(self):
        self.next = None
        self.space = create_space()
        self.walls, self.ball, self.hole = build_level(self.space, load_raw_map_data(get_random_map_name()))
        self.slingshot = Slingshot()
        self.current_mouse_pos = (0, 0)

    def process_inputs(self, inputs):
        self.current_mouse_pos = inputs.mouse_pos
        if inputs.escape: self.next = "MENU"
            
        if inputs.mouse_down and self.ball.is_stopped():
            self.slingshot.start(inputs.mouse_down, self.ball)
                
        if inputs.mouse_up and self.slingshot.aiming:
            self.slingshot.release(inputs.mouse_up, self.ball)

    def update(self):
        update_space(self.space)

    def render(self, screen):
        draw_entities(screen, self.walls, self.ball, self.hole)
        aim_vector = self.slingshot.get_aim_vector(self.current_mouse_pos)
        draw_aim_line(screen, self.ball.pos, aim_vector)

    def get_next_scene(self):
        return self.next