from src.core.scene import Scene
from src.constants import WIDTH, HEIGHT, BG_COLOR
from src.utils.ui import draw_text

class SoloScene(Scene):
    def __init__(self):
        self.next = None

    def process_inputs(self, inputs):
        if inputs.escape:
            self.next = "MENU"

    def render(self, screen):
        screen.fill(BG_COLOR)
        draw_text(screen, "MODE SOLO", (WIDTH//2, HEIGHT//2), center=True)
        draw_text(screen, "ECHAP pour revenir au Menu", (WIDTH//2, HEIGHT//2 + 50), font_size=20, center=True)

    def get_next_scene(self):
        return self.next