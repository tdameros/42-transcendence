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
    kill -9 $(pgrep '[P]ython')
    sleep 1
    clear
    `sed 's/^/export /' ../.env`
    python -m unittest discover test
    (
        cd src/redirection_server_deprecated &&
        find . -name '*.py' |
        entr -z -d python3 main.py
    )
done
