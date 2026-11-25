import itertools

from channels.generic.websocket import AsyncJsonWebsocketConsumer

online_players = {}
pending_invites = set()
rooms = {}
in_room = set()
room_ids = itertools.count(1)
MAPS = ["map_square.json", "map_triangle.json", "map_octagon.json"]


class LobbyConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        self.username = user.username
        self.room_id = None
        if not user.is_authenticated:
            await self.close()
            return
        await self.accept()
        online_players[self.username] = self.channel_name
        await self.channel_layer.group_add("lobby", self.channel_name)
        await self.send_players()

    async def disconnect(self, code):
        if self.room_id in rooms and not rooms[self.room_id]["started"]:
            room = rooms.pop(self.room_id, None)
            if room is not None:
                for name in room["players"]:
                    in_room.discard(name)
                await self.channel_layer.group_send(f"room_{self.room_id}", {"type": "room.closed", "from": self.username})
        if online_players.get(self.username) == self.channel_name:
            online_players.pop(self.username)
        await self.channel_layer.group_discard("lobby", self.channel_name)
        await self.send_players()

    async def send_players(self):
        free = []
        for name in sorted(online_players):
            if name not in in_room:
                free.append(name)
        await self.channel_layer.group_send(
            "lobby",
            {"type": "players.list", "players": free},
        )

    async def players_list(self, event):
        await self.send_json({"type": "players", "players": event["players"]})

    async def receive_json(self, content):
        action = content.get("action")
        if action == "map" or action == "ready":
            await self.room_action(action, content)
            return
        target = content.get("to")

        if target not in online_players or target == self.username:
            return

        if target in in_room or self.username in in_room:
            return

        address = online_players[target]

        if action == "invite":
            pending_invites.add((self.username, target))
            await self.channel_layer.send(
                address,
                {"type": "invite.received", "from": self.username},
            )
        elif action == "answer":
            if (target, self.username) not in pending_invites:
                return
            pending_invites.discard((target, self.username))
            await self.channel_layer.send(
                address,
                {"type": "invite.answer", "from": self.username, "accepted": content.get("accepted")},
            )
            if content.get("accepted"):
                room_id = next(room_ids)
                rooms[room_id] = {
                    "players": [target, self.username],
                    "map": "map_square.json",
                    "ready": set(),
                    "started": False,
                }
                in_room.add(target)
                in_room.add(self.username)
                for name in rooms[room_id]["players"]:
                    await self.channel_layer.send(
                        online_players[name],
                        {"type": "room.joined", "room_id": room_id},
                    )
                await self.send_players()

    async def invite_received(self, event):
        await self.send_json({"type": "invite", "from": event["from"]})

    async def invite_answer(self, event):
        await self.send_json({
            "type": "answer",
            "from": event["from"],
            "accepted": event["accepted"],
        })

    async def room_joined(self, event):
        self.room_id = event["room_id"]
        await self.channel_layer.group_add(f"room_{self.room_id}", self.channel_name)
        await self.room_update(event)

    async def room_action(self, action, content):
        if self.room_id not in rooms:
            return
        room = rooms[self.room_id]

        if action == "map":
            if content.get("map") not in MAPS:
                return
            room["map"] = content.get("map")
            room["ready"].clear()
        elif action == "ready":
            room["ready"].add(self.username)
        await self.channel_layer.group_send(f"room_{self.room_id}", {"type": "room.update"})
        if len(room["ready"]) == 2:
            room["started"] = True
            await self.channel_layer.group_send(f"room_{self.room_id}", {"type": "game.start", "map": room["map"], "room_id": self.room_id})

    async def room_update(self, event):
        room = rooms[self.room_id]
        await self.send_json({
            "type": "room",
            "players": room["players"],
            "map": room["map"],
            "ready": sorted(room["ready"]),
        })

    async def room_closed(self, event):
        self.room_id = None
        await self.send_json({"type": "room_closed", "from": event["from"]})

    async def game_start(self, event):
        await self.send_json({"type": "start", "map": event["map"], "room_id": event["room_id"]})
