import pygame
import sys
from src.screens.menu import MenuScene
from src.constants import FPS

class GameEngine:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.current_scene = MenuScene()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            self.current_scene.render(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)