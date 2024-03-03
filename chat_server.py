import time
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

@app.websocket("/chat")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()

    try:
        while True:
            # Receive data from the client
            data = await ws.receive_text()
            time.sleep(2)
            await ws.send_text(f"{data}")

    except WebSocketDisconnect:
        print("Connection closed by the client.")
