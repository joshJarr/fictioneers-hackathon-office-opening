#!/usr/bin/env python

import asyncio
import websockets
import requests
import json
import contentful
import time

import RPi.GPIO as GPIO

from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

client = contentful.Client(
  '0got9kbaqo5d',  # This is the space ID. A space is like a project folder in Contentful terms
  'pRt-hmb1QffZQXfOQpLKrw9kzK8Z342aQeWtaVoAQ3o'  # This is the access token for this space. Normally you get both ID and the token in the Contentful web app
)

# Mocked user ID
id = 'aaaaaaaaa3'

# character = 'fic'
character = 'tio'
# character = 'neers'
# character = 'end'

async def main(websocket, path):
  while True:
    # TODO: Replace with RFID reader.
    print('input pls')
    id, text = reader.read()
    print(id)
    print(text)

    # Mocked user ID
    id = str(id) + '123'
    await websocket.send('wake')

    # Get a  token for the given user.
    token_headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'Authorization' : 's_84adbe13806cfc63.Rwq7EJWRymjtd_WOIHznF6Q8ZUZ2XQ_ETsPecK4MpJs'
    }
    token_body = {"user_id": id}
    token_response = requests.post('https://api.fictioneers.co.uk/api/v1/auth/token' , headers=token_headers, data=json.dumps(token_body))
    token = token_response.json()['id_token']
    print('========token')
    print(token_response)
    print(token_response.json())

    # Try and get a user for the given {id}
    user_response = requests.get(f'https://api.fictioneers.co.uk/api/v1/users/me', params={'include_narrative_state': True}, headers={'Authorization' : f'Bearer {token}'})
    print('========Try and get a user')
    print(user_response)
    print(user_response.json())

    # If no user,
    if user_response.status_code == 403:
      # make one! and get their story state
      create_user_body = {
        "published_timeline_id": "rT5vuTQvGBudLRqe0lZ4",
        "timezone": "Europe/London",
        "disable_time_guards": False,
        "pause_at_beats": False
      }
      create_user_response = requests.post(f'https://api.fictioneers.co.uk/api/v1/users/' , headers={'Authorization' : f'Bearer {token}'}, data=json.dumps(create_user_body))
      print('======== 403')
      user_story_state = create_user_response.json()['data']['narrative_state']


    else:
      # Using the story state,
      print('======== pass')
      print(user_response)
      print(user_response.json())
      user_story_state = user_response.json()['data']['narrative_state']


    print('========')
    print(user_story_state);
    current_beat_id = user_story_state['current_beat']['id']

    # determine if the user is in the correct beat to progress
    beats = {
      "fic": ['x0HkthOzIo2ThOiTM3zu'],
      "tio": ['eiBtt7JiCvryJc0EaL7m', 'mRXTWvwNjk1IPyQhlB8r'],
      "neers": ['qGXCLk7Brh1tbA4J6TIi'],
      "end": ['bE84ZDGlQ5k6LyDUFoGQ'],
    }


    if current_beat_id in beats[character]:
      print('were with the right character')


      # send a request progressing the story
      # /api/v1/user-story-state/progress-events
      progress_story_body = {
        "max_steps": 1,
        "pause_at_beats": False
      }

      progress_story_response = requests.post(f'https://api.fictioneers.co.uk/api/v1/user-story-state/progress-events' , headers={'Authorization' : f'Bearer {token}'}, data=json.dumps(progress_story_body))
      print('========')
      print('progressed story')
      print(progress_story_response.json())
      # Get the content ID
      # new_content_id = progress_story_response['meta']['upserted_event_hooks'][0]['content_integrations'][0]['content_id']
      upserted_hooks = progress_story_response.json()['meta']['upserted_event_hooks']
      print(upserted_hooks)
      content_integrations = upserted_hooks[0]['content_integrations']
      print(content_integrations)
      content_id = content_integrations[0]['content_id']
      print(content_integrations)
      # new_content_id = '1hKQPk0TnyeWrUd1BN9jUd'
      entry = client.entry(content_id)
      script = entry.script

      print('========')
      print('content')
      print(script)

    else:
      # If we cannot progress
      print('wrong character!')
      await websocket.send('sleep')

      # Find the error message for this character per the users beat
      script = [
        {
          "length": 8,
          "text": "Zzz... Zzz... Zzz...",
          "expression": "sleeping"
        }
      ]


    await websocket.send(json.dumps(script))
    time.sleep(10)
  #END WHILE

start_server = websockets.serve(main, '127.0.0.1', 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
