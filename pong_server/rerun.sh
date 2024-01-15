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
    python -m unittest discover test
    find . -name '*.py' | entr -z -d python3 -m src.redirection_server
done
