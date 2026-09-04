from src.core.scene import Scene
from src.constants import WIDTH, HEIGHT, BG_COLOR
from src.utils.ui import draw_text

class MenuScene(Scene):
    def render(self, screen):
        screen.fill(BG_COLOR)
        draw_text(screen, "GOLFIGHT", (WIDTH//2, HEIGHT//4), font_size=70, center=True)