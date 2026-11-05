import pygame
from src.constants import (
    BG_COLOR, WALL_COLOR, BALL_COLOR, HOLE_COLOR, BALL_RADIUS, HOLE_RADIUS, AIM_COLOR,
    SAND_COLOR, WATER_COLOR
)

def draw_entities(screen, walls, balls, hole, zones=None, hide_ball=False):
    screen.fill(BG_COLOR)
    if zones:
        for z in zones:
            color = SAND_COLOR if z.zone_type == "sand" else WATER_COLOR
            pygame.draw.rect(screen, color, z.rect, border_radius=4)
            border_col = (180, 130, 20) if z.zone_type == "sand" else (20, 100, 200)
            pygame.draw.rect(screen, border_col, z.rect, 1, border_radius=4)
    pygame.draw.circle(screen, HOLE_COLOR, hole.pos, HOLE_RADIUS)
    for wall in walls:
        pygame.draw.line(screen, WALL_COLOR, wall.p1, wall.p2, 10)
    if not hide_ball:
        ball_list = balls if isinstance(balls, (list, tuple)) else [balls]
        for b in ball_list:
            color = getattr(b, "color", BALL_COLOR)
            pygame.draw.circle(screen, color, b.pos, BALL_RADIUS)

def draw_aim_line(screen, ball_pos, aim_vector):
    if aim_vector:
        target = (ball_pos[0] + aim_vector[0], ball_pos[1] + aim_vector[1])
        pygame.draw.line(screen, AIM_COLOR, ball_pos, target, 4)
