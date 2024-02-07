#!/bin/bash

export PONG_GAME_SERVERS_MIN_PORT=42200
export PONG_GAME_SERVERS_MAX_PORT=42210
export GAME_SERVER_PATH=~/git/transcendence/pong_server/src/game_server/


(cd src/game_creator/ && python3 manage.py test) || exit $?
kill -9 `pgrep '[P]ython'`

(cd src/game_creator/ && python3 manage.py runserver)
