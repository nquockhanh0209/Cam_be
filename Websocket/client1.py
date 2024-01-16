import websockets
import asyncio
import os
from dotenv import load_dotenv
load_dotenv() 
# Server data
PORT = os.getenv('PORT')
# The main function that will handle connection and communication 
# with the server
async def listen():
    url = "ws://127.0.0.1:"+ PORT
    # Connect to the server
    async with websockets.connect(url) as ws:
        # Send a greeting message
        await ws.send("Hello Server!")
        # Stay alive forever, listening to incoming msgs
        while True:
            msg = await ws.recv()
            print(msg)

# Start the connection
asyncio.get_event_loop().run_until_complete(listen())