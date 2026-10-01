from src.core.physics import create_space, update_space
from src.levels.map_loader import load_raw_map_data, get_random_map_name
from src.levels.level_factory import build_level
from src.systems.slingshot import Slingshot

class Game:
    def __init__(self):
        self.level = load_raw_map_data(get_random_map_name())
        self.space = create_space()
        self.walls, self.ball, self.hole = build_level(self.space, self.level)
        self.slingshot = Slingshot()

    def shoot(self, start, end):
        if self.ball.is_stopped():
            self.slingshot.start(start, self.ball)
            self.slingshot.release(end, self.ball)

    def update(self):
        self.hole.apply_gravity(self.ball)
        update_space(self.space)
