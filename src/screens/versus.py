import math
import pygame
from src.core.scene import Scene
from src.core.physics import create_space, update_space, reset_body_momentum
from src.levels.map_loader import load_raw_map_data, get_random_map_name
from src.levels.level_factory import build_versus_level
from src.systems.slingshot import Slingshot
from src.systems.renderer import draw_entities, draw_aim_line
from src.utils.ui import draw_text, draw_button, draw_overlay
from src.constants import WIDTH, HEIGHT, SHOOT_SPEED_THRESHOLD, BALL_COLOR_P1, BALL_COLOR_P2

class VersusScene(Scene):
    def __init__(self):
        self.next = None
        self.collision_flash_timer = 0
        self.last_collision_info = ""

        self.space = create_space(on_ball_collision=self._on_ball_collision)
        self.walls, self.ball1, self.ball2, self.hole = build_versus_level(
            self.space, load_raw_map_data(get_random_map_name())
        )

        self.slingshot = Slingshot()
        self.active_ball_for_shot = None
        self.current_player = 1
        self.score_p1 = 0
        self.score_p2 = 0
        self.winner = None
        self.win_timer = 0
        self.current_mouse_pos = (0, 0)

    def _on_ball_collision(self, ball_a, ball_b, impulse):
        self.collision_flash_timer = pygame.time.get_ticks()
        self.last_collision_info = f"Impact P1 - P2 ({int(impulse)} Ns)"

    def _get_quit_btn(self):
        return pygame.Rect(WIDTH - 120, 20, 100, 40)

    def process_inputs(self, inputs):
        self.current_mouse_pos = inputs.mouse_pos

        if inputs.escape:
            self.next = "MENU"

        if inputs.mouse_down:
            if self._get_quit_btn().collidepoint(inputs.mouse_down):
                self.next = "MENU"
                return

            if self.winner is None:
                active_ball = self.ball1 if self.current_player == 1 else self.ball2
                dist_to_active = math.hypot(active_ball.pos[0] - inputs.mouse_down[0], active_ball.pos[1] - inputs.mouse_down[1])

                if dist_to_active < 30 and active_ball.is_stopped():
                    self.active_ball_for_shot = active_ball
                    self.slingshot.start(inputs.mouse_down, active_ball)

        if inputs.mouse_up and self.slingshot.aiming and self.active_ball_for_shot:
            if self.slingshot.release(inputs.mouse_up, self.active_ball_for_shot):
                if self.current_player == 1:
                    self.score_p1 += 1
                    self.current_player = 2
                else:
                    self.score_p2 += 1
                    self.current_player = 1
            self.active_ball_for_shot = None

    def update(self):
        if self.winner is None:
            self.hole.apply_gravity(self.ball1)
            self.hole.apply_gravity(self.ball2)

        update_space(self.space)

        if self.winner is None:
            if self.hole.is_ball_in(self.ball1):
                self.winner = "Player 1"
                self.win_timer = pygame.time.get_ticks()
                reset_body_momentum(self.ball1.body)
            elif self.hole.is_ball_in(self.ball2):
                self.winner = "Player 2"
                self.win_timer = pygame.time.get_ticks()
                reset_body_momentum(self.ball2.body)

        if self.winner and pygame.time.get_ticks() - self.win_timer > 2500:
            self.next = "1V1"

    def render(self, screen):
        hide_p1 = (self.winner is not None and "Player 1" in self.winner)
        hide_p2 = (self.winner is not None and "Player 2" in self.winner)
        balls_to_draw = []
        if not hide_p1:
            balls_to_draw.append(self.ball1)
        if not hide_p2:
            balls_to_draw.append(self.ball2)

        draw_entities(screen, self.walls, balls_to_draw, self.hole)

        # Active player indicator
        if self.winner is None:
            active_ball = self.ball1 if self.current_player == 1 else self.ball2
            ring_color = BALL_COLOR_P1 if self.current_player == 1 else BALL_COLOR_P2
            pygame.draw.circle(screen, ring_color, active_ball.pos, 16, 2)

        if self.slingshot.aiming and self.active_ball_for_shot:
            aim_vector = self.slingshot.get_aim_vector(self.current_mouse_pos)
            draw_aim_line(screen, self.active_ball_for_shot.pos, aim_vector)

        draw_text(screen, f"P1: {self.score_p1}", (20, 20), font_size=20, color=BALL_COLOR_P1)
        draw_text(screen, f"P2: {self.score_p2}", (20, 50), font_size=20, color=BALL_COLOR_P2)

        turn_color = BALL_COLOR_P1 if self.current_player == 1 else BALL_COLOR_P2
        draw_text(screen, f"Turn: Player {self.current_player}", (WIDTH // 2, 30), font_size=24, color=turn_color, center=True)

        if pygame.time.get_ticks() - self.collision_flash_timer < 1500 and self.last_collision_info:
            draw_text(screen, self.last_collision_info, (WIDTH // 2, 65), font_size=20, color=(255, 230, 80), center=True)

        draw_button(screen, "Leave", self._get_quit_btn(), (150, 50, 50), (200, 50, 50), self.current_mouse_pos, 20)

        if self.winner:
            draw_overlay(screen)
            draw_text(screen, f"{self.winner} wins!", (WIDTH // 2, HEIGHT // 2), 48, (255, 215, 0), center=True)

    def get_next_scene(self):
        return self.next