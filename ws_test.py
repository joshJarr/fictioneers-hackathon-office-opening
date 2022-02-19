#!/usr/bin/env python

import asyncio
import websockets

async def hello():
    async with websockets.connect('ws://127.0.0.1:5678') as websocket:
      while True:
        name = input("Device ID is? ")
        await websocket.send(name)
        print("> {}".format(name))

        greeting = await websocket.recv()
        print("< {}".format(greeting))

asyncio.get_event_loop().run_until_complete(hello())