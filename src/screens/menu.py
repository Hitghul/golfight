import pygame
import sys
from src.core.scene import Scene
from src.constants import WIDTH, HEIGHT, BG_COLOR
from src.utils.ui import draw_button, draw_text

class MenuScene(Scene):
    def __init__(self):
        self.next = None
        self.current_mouse_pos = (0, 0)

    def _get_buttons(self):
        center_x = WIDTH // 2 - 100
        center_y = HEIGHT // 2
        return {
            "solo": pygame.Rect(center_x, center_y - 100, 200, 50),
            "1v1": pygame.Rect(center_x, center_y - 35, 200, 50),
            "settings": pygame.Rect(center_x, center_y + 30, 200, 50),
            "quit": pygame.Rect(center_x, center_y + 95, 200, 50),
        }

    def process_inputs(self, inputs):
        self.current_mouse_pos = inputs.mouse_pos
        if inputs.mouse_down:
            buttons = self._get_buttons()
            if buttons["solo"].collidepoint(inputs.mouse_down):
                self.next = "SOLO"
            elif buttons["1v1"].collidepoint(inputs.mouse_down):
                self.next = "1V1"
            elif buttons["settings"].collidepoint(inputs.mouse_down):
                self.next = "SETTINGS"
            elif buttons["quit"].collidepoint(inputs.mouse_down):
                pygame.quit()
                sys.exit()

    def render(self, screen):
        screen.fill(BG_COLOR)
        buttons = self._get_buttons()

        draw_text(screen, "GOLFIGHT", (WIDTH // 2, HEIGHT // 4), font_size=72, center=True)
        draw_button(screen, "Solo", buttons["solo"], (50, 50, 50), (100, 100, 100), self.current_mouse_pos)
        draw_button(screen, "1 Vs 1", buttons["1v1"], (50, 50, 50), (100, 100, 100), self.current_mouse_pos)
        draw_button(screen, "Settings", buttons["settings"], (50, 50, 50), (100, 100, 100), self.current_mouse_pos)
        draw_button(screen, "Leave", buttons["quit"], (150, 50, 50), (200, 50, 50), self.current_mouse_pos)

    def get_next_scene(self):
        return self.next