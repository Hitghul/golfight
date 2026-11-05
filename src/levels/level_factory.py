from src.entities.ball import Ball
from src.entities.wall import Wall
from src.entities.hole import Hole
from src.entities.zone import SandZone, WaterZone
from src.constants import BALL_COLOR_P1, BALL_COLOR_P2

def create_zones(raw_zones):
    zones = []
    for z in raw_zones:
        rect = z.get("rect", [])
        if len(rect) == 4:
            if z.get("type") == "sand":
                zones.append(SandZone(*rect))
            elif z.get("type") == "water":
                zones.append(WaterZone(*rect))
    return zones

def build_level(space, raw_data):
    walls = [Wall(space, (w[0], w[1]), (w[2], w[3])) for w in raw_data["walls"]]
    ball = Ball(space, raw_data["start_pos"][0], raw_data["start_pos"][1], color=BALL_COLOR_P1, player_id=1)
    hole = Hole(raw_data["hole_pos"][0], raw_data["hole_pos"][1])
    zones = create_zones(raw_data.get("zones", []))
    return walls, ball, hole, zones

def build_versus_level(space, raw_data):
    walls = [Wall(space, (w[0], w[1]), (w[2], w[3])) for w in raw_data["walls"]]
    start_x, start_y = raw_data["start_pos"]
    ball1 = Ball(space, start_x, start_y - 25, color=BALL_COLOR_P1, player_id=1)
    ball2 = Ball(space, start_x, start_y + 25, color=BALL_COLOR_P2, player_id=2)
    hole = Hole(raw_data["hole_pos"][0], raw_data["hole_pos"][1])
    zones = create_zones(raw_data.get("zones", []))
    return walls, ball1, ball2, hole, zones
