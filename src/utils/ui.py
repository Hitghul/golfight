import pygame

def draw_text(surface, text, pos, font_size=28, color=(255, 255, 255), center=False):
    font = pygame.font.SysFont("Arial", font_size, bold=True)
    text_surface = font.render(text, True, color)
    if center:
        surface.blit(text_surface, text_surface.get_rect(center=pos))
    else:
        surface.blit(text_surface, pos)