from src.entities.ball import Ball
from src.entities.wall import Wall
from src.entities.hole import Hole

def build_level(space, raw_data):
    walls = [Wall(space, (w[0], w[1]), (w[2], w[3])) for w in raw_data["walls"]]
    ball = Ball(space, raw_data["start_pos"][0], raw_data["start_pos"][1])
    hole = Hole(raw_data["hole_pos"][0], raw_data["hole_pos"][1])
    return walls, ball, hole