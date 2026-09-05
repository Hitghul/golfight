import pygame
import sys
from src.core.events import poll_events
from src.core.scene import Scene
from src.screens.menu import MenuScene
from src.screens.solo import SoloScene
from src.screens.versus import VersusScene
from src.constants import FPS

class GameEngine:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.scene_registry = {
            "MENU": MenuScene,
            "SOLO": SoloScene,
            "1V1": VersusScene
        }
        self.current_scene: Scene = self.scene_registry["MENU"]()

    def run(self):
        while True:
            inputs = poll_events()
            if inputs.quit:
                self.quit_game()
                
            self.current_scene.process_inputs(inputs)
            self.current_scene.update()
            
            next_scene = self.current_scene.get_next_scene()
            if next_scene:
                self.current_scene = self.scene_registry[next_scene]()

            self.current_scene.render(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)

    def quit_game(self):
        pygame.quit()
        sys.exit()