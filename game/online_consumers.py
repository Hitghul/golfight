import asyncio

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from lobby.consumers import rooms, in_room
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
        "winner": None,
        "votes": set(),
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
        while self.room_id in games:
            game = games[self.room_id]
            for ball in game["balls"]:
                game["hole"].apply_gravity(ball)
            update_space(game["space"])
            if game["winner"] is None:
                for player, ball in enumerate(game["balls"]):
                    if game["hole"].is_ball_in(ball):
                        game["winner"] = player
                        game["score"][player] += 1
                        await self.channel_layer.group_send(f"game_{self.room_id}",{"type": "game.send", "data": {"type": "scored", "player": player, "score": game["score"]}},)
                        break
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
        if "vote" in content:
            await self.vote(content["vote"])
            return
        game = games[self.room_id]
        if game["winner"] is not None:
            return
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

    async def vote(self, choice):
        game = games[self.room_id]
        if game["winner"] is None:
            return
        if choice == "replay":
            game["votes"].add(self.username)
            if len(game["votes"]) == 2:
                await self.new_round()
        elif choice == "quit":
            await self.end_session()

    async def end_session(self):
        room = rooms.pop(self.room_id, None)
        if room is not None:
            for name in room["players"]:
                in_room.discard(name)
        games.pop(self.room_id, None)
        await self.channel_layer.group_send(f"game_{self.room_id}",{"type": "game.send", "data": {"type": "quit"}}, )

    async def new_round(self):
        old = games[self.room_id]
        game = new_game(rooms[self.room_id]["map"])
        game["score"] = old["score"]
        game["connected"] = old["connected"]
        games[self.room_id] = game
        await self.channel_layer.group_send(
            f"game_{self.room_id}",
            {"type": "game.send", "data": level_message(game)},
        )