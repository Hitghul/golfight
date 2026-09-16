import pygame
import sys
from src.core.events import poll_events
from src.core.scene import Scene
from src.screens.menu import MenuScene
from src.screens.solo import SoloScene
from src.screens.versus import VersusScene
from src.screens.settings import SettingsScene
from src.constants import FPS, WIDTH, HEIGHT, BG_COLOR

class GameEngine:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.logical_surface = pygame.Surface((WIDTH, HEIGHT))
        self.scene_registry = {
            "MENU": MenuScene,
            "SOLO": SoloScene,
            "1V1": VersusScene,
            "SETTINGS": SettingsScene
        }
        self.current_scene: Scene = self.scene_registry["MENU"]()

    def _map_mouse(self, pos, current_w, current_h):
        ratio = min(current_w / WIDTH, current_h / HEIGHT)
        new_w, new_h = int(WIDTH * ratio), int(HEIGHT * ratio)
        offset_x = (current_w - new_w) // 2
        offset_y = (current_h - new_h) // 2
        
        x, y = pos
        x = int((x - offset_x) / ratio)
        y = int((y - offset_y) / ratio)
        return (x, y)

    def run(self):
        while True:
            inputs = poll_events()
            if inputs.quit:
                self.quit_game()

            if inputs.resized:
                current_size = self.screen.get_size()
                if inputs.resized != current_size:
                    self.screen = pygame.display.set_mode(inputs.resized, pygame.RESIZABLE)

            current_w, current_h = self.screen.get_size()

            inputs.mouse_pos = self._map_mouse(inputs.mouse_pos, current_w, current_h)
            if inputs.mouse_down is not None:
                inputs.mouse_down = self._map_mouse(inputs.mouse_down, current_w, current_h)
            if inputs.mouse_up is not None:
                inputs.mouse_up = self._map_mouse(inputs.mouse_up, current_w, current_h)

            self.current_scene.process_inputs(inputs)
            self.current_scene.update()
            
            next_scene = self.current_scene.get_next_scene()
            if next_scene:
                self.current_scene = self.scene_registry[next_scene]()
            self.current_scene.render(self.logical_surface)

            ratio = min(current_w / WIDTH, current_h / HEIGHT)
            new_w, new_h = int(WIDTH * ratio), int(HEIGHT * ratio)
            scaled_surface = pygame.transform.scale(self.logical_surface, (new_w, new_h))
            
            self.screen.fill(BG_COLOR)
            offset_x = (current_w - new_w) // 2
            offset_y = (current_h - new_h) // 2
            self.screen.blit(scaled_surface, (offset_x, offset_y))

            pygame.display.flip()
            self.clock.tick(FPS)

    def quit_game(self):
        pygame.quit()
        sys.exit()