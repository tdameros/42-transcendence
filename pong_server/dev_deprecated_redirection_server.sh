#!/bin/bash

trap 'rerun' QUIT
function rerun() {
    echo "stop and run server"
}

trap 'quit' INT
function quit() {
    exit 0
}

while true; do
    kill -9 `pgrep '[P]ython'`
    sleep 1
    clear
    export PONG_GAME_SERVERS_MIN_PORT=60200
    export PONG_GAME_SERVERS_MAX_PORT=60210
    python -m unittest discover test
    (
        cd src/redirection_server_deprecated &&
        ( find . -name '*.py' && find ../game_server -name '*.py' ) |
        entr -z -d python3 main.py
    )
done
