import pygame
from src.core.scene import Scene
from src.core.physics import create_space, update_space, reset_body_momentum
from src.levels.map_loader import load_raw_map_data, get_random_map_name
from src.levels.level_factory import build_level
from src.systems.slingshot import Slingshot
from src.systems.renderer import draw_entities, draw_aim_line
from src.utils.ui import draw_text, draw_button, draw_overlay

class SoloScene(Scene):
    def __init__(self):
        self.next = None
        self.space = create_space()
        self.walls, self.ball, self.hole = build_level(self.space, load_raw_map_data(get_random_map_name()))
        
        self.slingshot = Slingshot()
        
        self.score = 0
        self.is_won = False
        self.win_timer = 0
        self.current_mouse_pos = (0, 0)

    def _get_quit_btn(self):
        from src.constants import WIDTH
        return pygame.Rect(WIDTH - 120, 20, 100, 40)

    def process_inputs(self, inputs):
        self.current_mouse_pos = inputs.mouse_pos
        
        if inputs.escape:
            self.next = "MENU"
            
        if inputs.mouse_down:
            if self._get_quit_btn().collidepoint(inputs.mouse_down):
                self.next = "MENU"
            elif not self.is_won and self.ball.is_stopped():
                self.slingshot.start(inputs.mouse_down, self.ball)
                
        if inputs.mouse_up and self.slingshot.aiming and not self.is_won:
            if self.slingshot.release(inputs.mouse_up, self.ball):
                self.score += 1

    def update(self):
        update_space(self.space)

        if not self.is_won and self.hole.is_ball_in(self.ball):
            self.is_won = True
            self.win_timer = pygame.time.get_ticks()
            reset_body_momentum(self.ball.body)

        if self.is_won and pygame.time.get_ticks() - self.win_timer > 2000:
            self.next = "SOLO"

    def render(self, screen):
        draw_entities(screen, self.walls, self.ball, self.hole, hide_ball=self.is_won)
        
        aim_vector = self.slingshot.get_aim_vector(self.current_mouse_pos)
        draw_aim_line(screen, self.ball.pos, aim_vector)
        
        draw_text(screen, f"Hits : {self.score}", (20, 20))
        draw_button(screen, "Leave", self._get_quit_btn(), (150, 50, 50), (200, 50, 50), self.current_mouse_pos, 20)

        if self.is_won:
            w, h = screen.get_size()
            draw_overlay(screen)
            draw_text(screen, "Scored !", (w//2, h//2), 50, (255, 215, 0), center=True)

    def get_next_scene(self):
        return self.next