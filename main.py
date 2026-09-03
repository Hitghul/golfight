import pygame
import sys

WIDTH, HEIGHT = 1024, 768
FPS = 60

# Initialisation de Pygame
pygame.init()

# Création de la fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Golfight")

# FPS
clock = pygame.time.Clock()

def main():
    running = True
    
    # Boucle de jeu principale
    while running:

        # Quitter le programme
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Remplir l'écran en vert
        screen.fill((34, 139, 34))  
        
        # Rafraîchir l'écran
        pygame.display.flip()
        
        clock.tick(FPS)

    # Fermeture
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()