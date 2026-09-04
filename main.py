import pygame
from src.constants import WIDTH, HEIGHT
from src.core.engine import GameEngine

def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Golfight")
    
    engine = GameEngine(screen, pygame.time.Clock())
    engine.run()

if __name__ == "__main__":
    main()