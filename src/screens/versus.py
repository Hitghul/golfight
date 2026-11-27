import math
import pygame
from src.core.scene import Scene
from src.core.physics import create_space, update_space, reset_body_momentum
from src.levels.map_loader import load_raw_map_data, get_random_map_name
from src.levels.level_factory import create_zones
from src.entities.ball import Ball
from src.entities.hole import Hole
from src.entities.wall import Wall
from src.systems.slingshot import Slingshot
from src.systems.renderer import draw_entities, draw_aim_line
from src.utils.ui import draw_text, draw_button, draw_overlay
from src.constants import WIDTH, HEIGHT, FPS, WALL_COLOR, BALL_RADIUS, HOLE_RADIUS, HOLE_COLOR, BALL_COLOR_P1, BALL_COLOR_P2

class VersusScene(Scene):
    def __init__(self):
        self.next = None
        self.collision_flash_timer = 0
        self.last_collision_info = ""

        self.space = create_space(on_ball_collision=self._on_ball_collision)
        raw_data = load_raw_map_data(get_random_map_name())
        self.walls = [Wall(self.space, (w[0], w[1]), (w[2], w[3])) for w in raw_data["walls"]]
        self.zones = create_zones(raw_data.get("zones", []))

        self.ball1 = None
        self.ball2 = None
        self.hole1 = None
        self.hole2 = None

        self.slingshot = Slingshot()
        self.active_ball_for_shot = None
        self.current_player = 1
        self.score_p1 = 0
        self.score_p2 = 0
        self.winner = None
        self.win_timer = 0
        self.current_mouse_pos = (0, 0)

        self.phase = "placement"
        self.placement_step = 0
        self.wall_start = None

    def _on_ball_collision(self, ball_a, ball_b, impulse):
        self.collision_flash_timer = pygame.time.get_ticks()
        self.last_collision_info = f"Impact P1 - P2 ({int(impulse)} Ns)"

    def _get_quit_btn(self):
        return pygame.Rect(WIDTH - 120, 20, 100, 40)

    def _get_skip_btn(self):
        return pygame.Rect(WIDTH - 230, 20, 100, 40)

    def _limit_wall(self, p1, p2, max_len=75):
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        dist = math.hypot(dx, dy)
        if dist > max_len:
            return (int(p1[0] + dx * max_len / dist), int(p1[1] + dy * max_len / dist))
        return p2

    def process_inputs(self, inputs):
        self.current_mouse_pos = inputs.mouse_pos

        if inputs.escape:
            self.next = "MENU"

        if pygame.mouse.get_pressed()[2]:
            self.wall_start = None

        if inputs.mouse_down:
            pos = inputs.mouse_down
            if self._get_quit_btn().collidepoint(pos):
                self.next = "MENU"
                return

            if self.phase == "placement":
                if self.placement_step == 0:
                    self.ball2 = Ball(self.space, pos[0], pos[1], color=BALL_COLOR_P2, player_id=2)
                elif self.placement_step == 1:
                    self.hole2 = Hole(pos[0], pos[1], color=BALL_COLOR_P2)
                elif self.placement_step == 2:
                    self.ball1 = Ball(self.space, pos[0], pos[1], color=BALL_COLOR_P1, player_id=1)
                elif self.placement_step == 3:
                    self.hole1 = Hole(pos[0], pos[1], color=BALL_COLOR_P1)
                    self.phase = "trap"
                self.placement_step += 1

            elif self.phase == "trap":
                if self._get_skip_btn().collidepoint(pos):
                    self.wall_start = None
                    self.phase = "shoot"
                    return
                if self.wall_start is None:
                    self.wall_start = pos
                else:
                    end_pos = self._limit_wall(self.wall_start, pos)
                    if math.hypot(end_pos[0] - self.wall_start[0], end_pos[1] - self.wall_start[1]) > 10:
                        self.walls.append(Wall(self.space, self.wall_start, end_pos, thickness=12))
                        self.wall_start = None
                        self.phase = "shoot"

            elif self.phase == "shoot" and self.winner is None:
                active_ball = self.ball1 if self.current_player == 1 else self.ball2
                dist_to_active = math.hypot(active_ball.pos[0] - pos[0], active_ball.pos[1] - pos[1])
                if dist_to_active < 30 and active_ball.is_stopped():
                    self.active_ball_for_shot = active_ball
                    self.slingshot.start(pos, active_ball)

        if inputs.mouse_up and self.slingshot.aiming and self.active_ball_for_shot:
            if self.slingshot.release(inputs.mouse_up, self.active_ball_for_shot):
                if self.current_player == 1:
                    self.score_p1 += 1
                else:
                    self.score_p2 += 1
                self.phase = "moving"
            self.active_ball_for_shot = None

    def update(self):
        if self.phase != "placement" and self.winner is None:
            dt = 1.0 / FPS
            for zone in self.zones:
                if zone.apply(self.ball1, dt) == "WATER_HAZARD":
                    self.score_p1 += 1
                if zone.apply(self.ball2, dt) == "WATER_HAZARD":
                    self.score_p2 += 1

            self.hole1.apply_gravity(self.ball1)
            self.hole2.apply_gravity(self.ball2)

        update_space(self.space)

        if self.phase != "placement" and self.winner is None:
            if self.hole1.is_ball_in(self.ball1):
                self.winner = "Player 1"
                self.win_timer = pygame.time.get_ticks()
                reset_body_momentum(self.ball1.body)
            elif self.hole2.is_ball_in(self.ball2):
                self.winner = "Player 2"
                self.win_timer = pygame.time.get_ticks()
                reset_body_momentum(self.ball2.body)
            elif self.phase == "moving" and self.ball1.is_stopped() and self.ball2.is_stopped():
                self.current_player = 2 if self.current_player == 1 else 1
                self.phase = "trap"

        if self.winner and pygame.time.get_ticks() - self.win_timer > 2500:
            self.next = "1V1"

    def render(self, screen):
        hide_p1 = (self.winner is not None and "Player 1" in self.winner)
        hide_p2 = (self.winner is not None and "Player 2" in self.winner)
        balls_to_draw = []
        if self.ball1 and not hide_p1:
            balls_to_draw.append(self.ball1)
        if self.ball2 and not hide_p2:
            balls_to_draw.append(self.ball2)

        draw_entities(screen, self.walls, balls_to_draw, [self.hole1, self.hole2], zones=self.zones)

        if self.phase == "placement":
            steps = [
                ("P1: place P2 ball", BALL_COLOR_P1, BALL_COLOR_P2, False),
                ("P1: place P2 hole", BALL_COLOR_P1, BALL_COLOR_P2, True),
                ("P2: place P1 ball", BALL_COLOR_P2, BALL_COLOR_P1, False),
                ("P2: place P1 hole", BALL_COLOR_P2, BALL_COLOR_P1, True),
            ]
            label, text_col, item_col, is_hole = steps[self.placement_step]
            if is_hole:
                pygame.draw.circle(screen, HOLE_COLOR, self.current_mouse_pos, HOLE_RADIUS)
                pygame.draw.circle(screen, item_col, self.current_mouse_pos, HOLE_RADIUS + 3, 2)
            else:
                pygame.draw.circle(screen, item_col, self.current_mouse_pos, BALL_RADIUS)
            draw_text(screen, label, (WIDTH // 2, 30), font_size=24, color=text_col, center=True)

        elif self.phase == "trap":
            trapper = 2 if self.current_player == 1 else 1
            trapper_col = BALL_COLOR_P2 if trapper == 2 else BALL_COLOR_P1
            draw_text(screen, f"P{trapper}: place a wall", (WIDTH // 2, 30), font_size=24, color=trapper_col, center=True)
            draw_button(screen, "Skip", self._get_skip_btn(), (70, 70, 70), (110, 110, 110), self.current_mouse_pos, 20)
            if self.wall_start:
                end_pos = self._limit_wall(self.wall_start, self.current_mouse_pos)
                pygame.draw.line(screen, WALL_COLOR, self.wall_start, end_pos, 10)

        else:
            if self.winner is None:
                active_ball = self.ball1 if self.current_player == 1 else self.ball2
                ring_color = BALL_COLOR_P1 if self.current_player == 1 else BALL_COLOR_P2
                pygame.draw.circle(screen, ring_color, active_ball.pos, 16, 2)

            if self.slingshot.aiming and self.active_ball_for_shot:
                aim_vector = self.slingshot.get_aim_vector(self.current_mouse_pos)
                draw_aim_line(screen, self.active_ball_for_shot.pos, aim_vector)

            turn_color = BALL_COLOR_P1 if self.current_player == 1 else BALL_COLOR_P2
            draw_text(screen, f"Turn: Player {self.current_player}", (WIDTH // 2, 30), font_size=24, color=turn_color, center=True)

        draw_text(screen, f"P1: {self.score_p1}", (20, 20), font_size=20, color=BALL_COLOR_P1)
        draw_text(screen, f"P2: {self.score_p2}", (20, 50), font_size=20, color=BALL_COLOR_P2)

        if pygame.time.get_ticks() - self.collision_flash_timer < 1500 and self.last_collision_info:
            draw_text(screen, self.last_collision_info, (WIDTH // 2, 65), font_size=20, color=(255, 230, 80), center=True)

        draw_button(screen, "Leave", self._get_quit_btn(), (150, 50, 50), (200, 50, 50), self.current_mouse_pos, 20)

        if self.winner:
            draw_overlay(screen)
            draw_text(screen, f"{self.winner} wins!", (WIDTH // 2, HEIGHT // 2), 48, (255, 215, 0), center=True)

    def get_next_scene(self):
        return self.next
