#!/bin/bash

pip install --no-cache-dir -r /app/common/docker/requirements.txt

# Copy the volume code to the src folder so that I can modify it without
# changing anything on the host machine
cp -r /app/pong_server_code /app/src

# Copy the shared code to the game_creator folder
rm -rf /app/src/game_creator/shared_code
cp -r /app/src/shared_code /app/src/game_creator/shared_code

# Copy the shared code to the game_server folder
rm -rf /app/src/game_server/shared_code
cp -r /app/src/shared_code /app/src/game_server/shared_code

# Copy the common code to the game_creator folder
rm -rf /app/src/game_creator/common
cp -r /app/common/ /app/src/game_creator/common

# Copy the common code to the game_server folder
rm -rf /app/src/game_server/common
cp -r /app/common/ /app/src/game_server/common


# Run game_creator
gunicorn -c /app/gunicorn.conf.py
