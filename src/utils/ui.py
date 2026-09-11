import pygame

def draw_text(surface, text, pos, font_size=28, color=(255, 255, 255), center=False):
    font = pygame.font.SysFont("Arial", font_size, bold=True)
    text_surf = font.render(text, True, color)
    if center:
        surface.blit(text_surf, text_surf.get_rect(center=pos))
    else:
        surface.blit(text_surf, pos)

def draw_button(surface, text, rect, base_color, hover_color, mouse_pos, font_size=36):
    font = pygame.font.SysFont("Arial", font_size)
    is_hovered = rect.collidepoint(mouse_pos)
    color = hover_color if is_hovered else base_color
    
    pygame.draw.rect(surface, color, rect, border_radius=8)
    text_surf = font.render(text, True, (255, 255, 255))
    surface.blit(text_surf, text_surf.get_rect(center=rect.center))
    
def draw_overlay(surface):
    overlay = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    surface.blit(overlay, (0, 0))