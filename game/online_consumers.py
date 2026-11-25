from channels.generic.websocket import AsyncJsonWebsocketConsumer

from lobby.consumers import rooms


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
        await self.send_json({"type": "welcome", "player": self.player, "map": room["map"]})

    async def disconnect(self, code):
        await self.channel_layer.group_discard(f"game_{self.room_id}", self.channel_name)