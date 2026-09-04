import pygame
from src.core.scene import Scene
from src.constants import WIDTH, HEIGHT, BG_COLOR
from src.utils.ui import draw_button, draw_text

class MenuScene(Scene):
    def __init__(self):
        self.btn_solo = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 40, 200, 60)
        self.btn_1v1 = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 40, 200, 60)

    def render(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(BG_COLOR)
        
        draw_text(screen, "GOLFIGHT", (WIDTH//2, HEIGHT//4), font_size=72, center=True)
        draw_button(screen, "Solo", self.btn_solo, (50, 50, 50), (100, 100, 100), mouse_pos)
        draw_button(screen, "1 Vs 1", self.btn_1v1, (50, 50, 50), (100, 100, 100), mouse_pos)