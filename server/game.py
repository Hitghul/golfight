import asyncio
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from src.core.physics import create_space, update_space
from src.levels.map_loader import load_raw_map_data, get_random_map_name
from src.levels.level_factory import build_level
from src.systems.slingshot import Slingshot

class GameConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.connected = True
        self.score = 0
        await self.load_level()
        asyncio.create_task(self.game_loop())

    async def disconnect(self, code):
        self.connected = False
    
    async def load_level(self):
        self.level = load_raw_map_data(get_random_map_name())
        self.space = create_space()
        self.walls, ball, self.hole = build_level(self.space, self.level)
        self.balls = [ball]
        self.slingshot = Slingshot()
        self.turn = 0
        self.hits = 0
        await self.send_json({"type": "level", **self.level, "score": self.score, "max_power": self.slingshot.max_power})

    async def receive_json(self, content):
        start, end = content
        self.shoot(start, end)

    def shoot(self, start, end):
        ball = self.balls[self.turn]
        if ball.is_stopped():
            self.slingshot.start(start, ball)
            if self.slingshot.release(end, ball):
                self.hits += 1

    async def game_loop(self):
        while self.connected:
            for ball in self.balls:
                self.hole.apply_gravity(ball)
            update_space(self.space)
            for ball in self.balls:
                if self.hole.is_ball_in(ball):
                    self.score += 1
                    await self.send_json({"type": "scored"})
                    await asyncio.sleep(2)
                    await self.load_level()
                    break
            await self.send_json({"type": "state", "balls": [ball.pos for ball in self.balls], "turn": self.turn, "can_shoot": self.balls[self.turn].is_stopped(), "hits": self.hits})
            await asyncio.sleep(1 / 60)
