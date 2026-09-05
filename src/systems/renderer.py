import pygame
from src.constants import BG_COLOR, WALL_COLOR, BALL_COLOR, HOLE_COLOR, BALL_RADIUS, HOLE_RADIUS

def draw_entities(screen, walls, ball, hole, hide_ball=False):
    screen.fill(BG_COLOR)
    pygame.draw.circle(screen, HOLE_COLOR, hole.pos, HOLE_RADIUS)
    for wall in walls:
        pygame.draw.line(screen, WALL_COLOR, wall.p1, wall.p2, 10)
    if not hide_ball:
        pygame.draw.circle(screen, BALL_COLOR, ball.pos, BALL_RADIUS)