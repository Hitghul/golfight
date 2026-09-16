import pygame
from src.core.scene import Scene
from src.constants import WIDTH, HEIGHT, BG_COLOR
from src.utils.ui import draw_button, draw_text

class SettingsScene(Scene):
    def __init__(self):
        self.next = None
        self.current_mouse_pos = (0, 0)

    def process_inputs(self, inputs):
        self.current_mouse_pos = inputs.mouse_pos
        if inputs.escape:
            self.next = "MENU"
            
        btn_windowed = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 70, 200, 50)
        btn_fullscreen = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
        btn_back = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 70, 200, 50)

        if inputs.mouse_down:
            if btn_windowed.collidepoint(inputs.mouse_down):
                pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            elif btn_fullscreen.collidepoint(inputs.mouse_down):
                pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            elif btn_back.collidepoint(inputs.mouse_down):
                self.next = "MENU"

    def render(self, screen):
        screen.fill(BG_COLOR)
        
        btn_windowed = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 70, 200, 50)
        btn_fullscreen = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
        btn_back = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 70, 200, 50)

        draw_text(screen, "SETTINGS", (WIDTH // 2, HEIGHT // 4), font_size=60, center=True)
        draw_button(screen, "Windowed", btn_windowed, (50, 50, 50), (100, 100, 100), self.current_mouse_pos)
        draw_button(screen, "Fullscreen", btn_fullscreen, (50, 50, 50), (100, 100, 100), self.current_mouse_pos)
        draw_button(screen, "Menu", btn_back, (150, 50, 50), (200, 50, 50), self.current_mouse_pos)

    def get_next_scene(self):
        return self.next