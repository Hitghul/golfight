from channels.generic.websocket import AsyncJsonWebsocketConsumer

online_players = {}

class LobbyConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        self.username = user.username
        if not user.is_authenticated:
            await self.close()
            return
        await self.accept()
        online_players[self.username] = self.channel_name
        await self.channel_layer.group_add("lobby", self.channel_name)
        await self.send_players()

    async def disconnect(self, code):
        online_players.pop(self.username, None)
        await self.channel_layer.group_discard("lobby", self.channel_name)
        await self.send_players()

    async def send_players(self):
        await self.channel_layer.group_send(
            "lobby",
            {"type": "players.list", "players": sorted(online_players)},
        )

    async def players_list(self, event):
        await self.send_json({"type": "players", "players": event["players"]})

    async def receive_json(self, content):
        action = content.get("action")
        target = content.get("to")

        if target not in online_players or target == self.username:
            return

        address = online_players[target]
        if action == "invite":
            await self.channel_layer.send(
                address,
                {"type": "invite.received", "from": self.username},
            )
        elif action == "answer":
            await self.channel_layer.send(
                address,
                {"type": "invite.answer", "from": self.username, "accepted": content.get("accepted")},
            )

    async def invite_received(self, event):
        await self.send_json({"type": "invite", "from": event["from"]})

    async def invite_answer(self, event):
        await self.send_json({"type": "answer", "from": event["from"], "accepted": event["accepted"]})