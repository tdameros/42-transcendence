#!/bin/bash

export PONG_GAME_SERVERS_MIN_PORT=42200
export PONG_GAME_SERVERS_MAX_PORT=42210
export PONG_GAME_APP_PATH=~/git/transcendence/pong_server/

(cd src/game_creator/ && python3 manage.py runserver 4242)
