import pygame
import sys
from src.screens.menu import MenuScene
from src.constants import FPS
from src.core.events import poll_events

class GameEngine:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.current_scene = MenuScene()

    def run(self):
        while True:
            inputs = poll_events()
            if inputs.quit:
                pygame.quit()
                sys.exit()
                
            self.current_scene.process_inputs(inputs)
            self.current_scene.update()
            
            self.current_scene.render(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)