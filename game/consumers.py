import asyncio
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from src.core.physics import create_space, update_space
from src.levels.map_loader import load_raw_map_data, get_random_map_name
from src.levels.level_factory import build_level, build_versus_level
from src.systems.slingshot import Slingshot

class GameConsumer(AsyncJsonWebsocketConsumer):
    players = 1

    async def connect(self):
        await self.accept()
        self.connected = True
        self.score = [0] * self.players
        await self.load_level()
        asyncio.create_task(self.game_loop())

    async def disconnect(self, code):
        self.connected = False
    
    async def load_level(self):
        self.level = load_raw_map_data(get_random_map_name())
        self.space = create_space()
        if self.players == 1:
            self.walls, ball, self.hole = build_level(self.space, self.level)
            self.balls = [ball]
        else:
            self.walls, ball1, ball2, self.hole = build_versus_level(self.space, self.level)
            self.balls = [ball1, ball2]
        self.slingshot = Slingshot()
        self.turn = 0
        self.hits = [0] * self.players
        await self.send_json({"type": "level", **self.level, "score": self.score, "max_power": self.slingshot.max_power, "colors": [ball.color for ball in self.balls]})

    async def receive_json(self, content):
        start, end = content
        self.shoot(start, end)

    def shoot(self, start, end):
        ball = self.balls[self.turn]
        if ball.is_stopped():
            self.slingshot.start(start, ball)
            if self.slingshot.release(end, ball):
                self.hits[self.turn] += 1
                self.turn = (self.turn + 1) % self.players

    async def game_loop(self):
        while self.connected:
            for ball in self.balls:
                self.hole.apply_gravity(ball)
            update_space(self.space)
            for player, ball in enumerate(self.balls):
                if self.hole.is_ball_in(ball):
                    self.score[player] += 1
                    await self.send_json({"type": "scored", "player": player})
                    await asyncio.sleep(2)
                    await self.load_level()
                    break
            await self.send_json({"type": "state", "balls": [ball.pos for ball in self.balls], "turn": self.turn, "can_shoot": self.balls[self.turn].is_stopped(), "hits": self.hits})
            await asyncio.sleep(1 / 60)


class VersusConsumer(GameConsumer):
    players = 2
