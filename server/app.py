import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from server.game import Game

app = FastAPI()

async def receive_shots(ws, game):
    try:
        while True:
            start, end = await ws.receive_json()
            game.shoot(start, end)
    except WebSocketDisconnect:
        pass

@app.websocket("/ws")
async def play(ws: WebSocket):
    await ws.accept()
    game = Game()
    await ws.send_json(game.level_message())
    receiver = asyncio.create_task(receive_shots(ws, game))
    while not receiver.done():
        if game.update():
            await ws.send_json(game.level_message())
        await ws.send_json(game.ball.pos)
        await asyncio.sleep(1 / 60)

app.mount("/", StaticFiles(directory="web", html=True))
