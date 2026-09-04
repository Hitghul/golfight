import pygame
from dataclasses import dataclass

@dataclass
class GameInputs:
    quit: bool = False
    escape: bool = False
    mouse_down: tuple | None = None
    mouse_pos: tuple = (0, 0)

def poll_events() -> GameInputs:
    inputs = GameInputs(mouse_pos=pygame.mouse.get_pos())
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inputs.quit = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            inputs.escape = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            inputs.mouse_down = event.pos
    return inputs