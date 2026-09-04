import pygame
import sys
from src.constants import WIDTH, HEIGHT, BG_COLOR, FPS

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Golfight")
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BG_COLOR)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()