#!/usr/bin/env python

import asyncio
import websockets

connected = set()

async def handler(websocket, path):
    global connected
    # Register.
    connected.add(websocket)
    try:
        while True:
            id = await websocket.recv()

            # Test code for the socket
            print("< {}".format(id))
            greeting = "Hello {}!".format(id)
            await asyncio.wait([ws.send(greeting) for ws in connected])


            # Try and get a user for the given {id}

            # If no user,
              # make one! and get their story state

            # Using the story state,
            # determine if the user is in the correct beat to progress

            # If we can progress
              # send a request progressing the story
              # Get the hook ID
              # Match the hook ID with the content
              # return the content via the socket

            # If we cannot progress
              # Find the error message for this character per the users beat
              # Send this message to the socket.

    finally:
        # Unregister.
        connected.remove(websocket)

start_server = websockets.serve(handler, '127.0.0.1', 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()