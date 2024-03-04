import time
import json
import asyncio
import websockets

from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout

'''
Simple chat client with streaming i/o.
This needs a server with a websocket endpoint.
'''

# for sending and receiving data
send_queue = asyncio.Queue()

async def input(ws, session):
    print("🟢 Ready to send. Type away")
    try:
        while True:
            message = await session.prompt_async("<user>: ")
            await send_queue.put(message)
    except Exception as e:
        print(f"Error during input: {str(e)}")
        raise
    except KeyboardInterrupt:
        pass  # Handle Ctrl+C

async def sender(ws):
    try:
        while True:
            message = await send_queue.get()
            # Latency
            global SEND
            SEND = time.time()
            # Send messages to the server
            await ws.send(message)

    except Exception as e:
        print(f"Error while sending: {str(e)}")
        raise
    except KeyboardInterrupt:
        pass  # Handle Ctrl+C

async def receiver(ws):
    global received_messages
    try:
        while True:
            # Receive data from the server
            message = await ws.recv()
            # Latency
            RECV = time.time()
            # Parse output on client side
            with patch_stdout():
                print(f"[{round(RECV-SEND, 3)}s] <bot>: {message}", flush=True)

    except websockets.exceptions.ConnectionClosed:
        print("Connection closed by the server.")
    except Exception as e:
        print(f"Error while receiving: {str(e)}")
        raise
    except KeyboardInterrupt:
        pass  # Handle Ctrl+C

async def run():
    session = PromptSession()
    uri = "ws://127.0.0.1:8010/chat"

    async with websockets.connect(uri) as ws:
        functions = [input(ws, session), sender(ws), receiver(ws)]
        await asyncio.gather(*functions)


if __name__ == "__main__":
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("\nExiting the program.")