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
        self.walls, self.ball, self.hole = build_level(self.space, self.level)
        self.slingshot = Slingshot()
        await self.send_json({**self.level, "score": self.score})

    async def receive_json(self, content):
        start, end = content
        self.shoot(start, end)

    def shoot(self, start, end):
        if self.ball.is_stopped():
            self.slingshot.start(start, self.ball)
            self.slingshot.release(end, self.ball)

    async def game_loop(self):
        while self.connected:
            self.hole.apply_gravity(self.ball)
            update_space(self.space)
            if self.hole.is_ball_in(self.ball):
                self.score += 1
                await self.load_level()
            await self.send_json(self.ball.pos)
            await asyncio.sleep(1 / 60)
