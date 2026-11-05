from channels.generic.websocket import AsyncJsonWebsocketConsumer

online_players = set()

class LobbyConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        self.username = user.username
        if not user.is_authenticated:
            await self.close()
            return
        await self.accept()
        online_players.add(self.username)
        await self.channel_layer.group_add("lobby", self.channel_name)
        await self.send_players()

    async def disconnect(self, code):
        online_players.discard(self.username)
        await self.channel_layer.group_discard("lobby", self.channel_name)
        await self.send_players()

    async def send_players(self):
        await self.channel_layer.group_send(
            "lobby",
            {"type": "players.list", "players": sorted(online_players)},
        )

    async def players_list(self, event):
        await self.send_json({"players": event["players"]})