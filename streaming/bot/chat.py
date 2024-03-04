from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from streaming.agent import *

from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class ChatBot(BaseModel):
    agent: Optional[ChatGPT] = None
    history: Optional[List[ChatMessage]] = None

    def __init__(self):
        super().__init__()
        self.agent = ChatGPT()
        self.history = []

    def respond(self, input_text: str):
        self.history.append(ChatMessage(role="user", content=input_text))
        output_text = self.agent(input_text, self.history)
        self.history.append(ChatMessage(role="bot", content=output_text))
        return output_text


@app.websocket("/chat")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    bot = ChatBot()

    try:
        while True:
            request: str = await ws.receive_text()
            response: str = bot.respond(request)
            await ws.send_text(response)

    except WebSocketDisconnect:
        print("Connection closed by the client.")
