#!/bin/bash

export PONG_GAME_SERVERS_MIN_PORT=42200
export PONG_GAME_SERVERS_MAX_PORT=42210
export PATH_TO_SSL_CERTS=~/git/transcendence/ssl/certs/

(
    cd src/game_server &&
    python3 main.py test 1 3 4 5
)
