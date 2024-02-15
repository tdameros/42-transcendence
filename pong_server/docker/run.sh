#!/bin/bash

# Copy the volume code to the src folder so that I can modify it without
# changing anything on the host machine
cp -r /app/pong_server_code /app/src

# Copy the shared code to the game_creator folder
rm -rf /app/src/game_creator/shared_code
cp -r /app/src/shared_code /app/src/game_creator/shared_code

# Copy the shared code to the game_server folder
rm -rf /app/src/game_server/shared_code
cp -r /app/src/shared_code /app/src/game_server/shared_code

# Run game_creator
gunicorn -c /app/gunicorn.conf.py
