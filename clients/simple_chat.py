import asyncio
import time

import websockets

'''
Simple chat client with i/o streaming for a single interaction.
Note that this needs a websocket endpoint on the server.
'''

async def sender(ws):
    print("🟢 Ready to send text. Type away")
    try:
        # Send messages to the server
        message = input("Enter message: ")

        global SEND
        SEND = time.time()
        await ws.send(message)

    except Exception as e:
        print(f"Error while sending: {str(e)}")
        raise


async def receiver(ws):
    try:
        # Receive data from the server
        data = await ws.recv()
        RECV = time.time()

        # Display the received message on the client side
        print(f"Received message: {data} with latency {round(RECV-SEND, 3)}s")


    except websockets.exceptions.ConnectionClosed:
        print("Connection closed by the server.")
    except Exception as e:
        print(f"Error while receiving: {str(e)}")
        raise


async def run():
    uri = "ws://127.0.0.1:8010/chat"

    async with websockets.connect(uri) as ws:
        functions = [sender(ws), receiver(ws)]
        await asyncio.gather(*functions)


if __name__ == "__main__":
    asyncio.run(run())
