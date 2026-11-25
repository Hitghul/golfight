import asyncio

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from lobby.consumers import rooms
from src.core.physics import create_space, update_space
from src.levels.level_factory import build_versus_level
from src.levels.map_loader import load_raw_map_data
from src.systems.slingshot import Slingshot

games = {}


def new_game(map_name):
    level = load_raw_map_data(map_name)
    space = create_space()
    walls, ball1, ball2, hole = build_versus_level(space, level)
    return {
        "level": level,
        "space": space,
        "walls": walls,
        "balls": [ball1, ball2],
        "hole": hole,
        "slingshot": Slingshot(),
        "turn": 0,
        "hits": [0, 0],
        "score": [0, 0],
        "connected": set(),
    }


def level_message(game):
    return {
        "type": "level",
        **game["level"],
        "score": game["score"],
        "max_power": game["slingshot"].max_power,
        "colors": [ball.color for ball in game["balls"]],
    }


class OnlineConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.username = self.scope["user"].username
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        if self.room_id not in rooms:
            await self.close()
            return

        room = rooms[self.room_id]
        if self.username not in room["players"]:
            await self.close()
            return

        self.player = room["players"].index(self.username)
        await self.accept()
        await self.channel_layer.group_add(f"game_{self.room_id}", self.channel_name)
        if self.room_id not in games:
            games[self.room_id] = new_game(room["map"])
            asyncio.create_task(self.game_loop())
        game = games[self.room_id]
        game["connected"].add(self.username)
        await self.send_json(level_message(game))
        await self.send_json({"type": "you", "player": self.player})

    async def game_loop(self):
        game = games[self.room_id]
        while self.room_id in games:
            for ball in game["balls"]:
                game["hole"].apply_gravity(ball)
            update_space(game["space"])
            state = {
                "type": "state",
                "balls": [ball.pos for ball in game["balls"]],
                "turn": game["turn"],
                "can_shoot": game["balls"][game["turn"]].is_stopped(),
                "hits": game["hits"],
            }
            await self.channel_layer.group_send(f"game_{self.room_id}", {"type": "game.send", "data": state})
            await asyncio.sleep(1 / 60)

    async def receive_json(self, content):
        game = games[self.room_id]
        if game["turn"] != self.player:
            return
        start, end = content
        ball = game["balls"][self.player]
        if ball.is_stopped():
            game["slingshot"].start(start, ball)
            if game["slingshot"].release(end, ball):
                game["hits"][self.player] += 1
                game["turn"] = (game["turn"] + 1) % 2

    async def disconnect(self, code):
        await self.channel_layer.group_discard(f"game_{self.room_id}", self.channel_name)
        if self.room_id in games:
            games[self.room_id]["connected"].discard(self.username)
            if not games[self.room_id]["connected"]:
                games.pop(self.room_id)

    async def game_send(self, event):
        await self.send_json(event["data"])
