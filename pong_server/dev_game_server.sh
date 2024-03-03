#!/bin/bash

`sed 's/^/export /' ~/git/transcendence/common/src/.env`
export PONG_GAME_SERVERS_MIN_PORT=42200
export PONG_GAME_SERVERS_MAX_PORT=42210
export PATH_TO_SSL_CERTS=~/git/transcendence/ssl/certs/

(
    cd src/game_server &&
    python3 main.py 42 dev 1 None 2 3
)
