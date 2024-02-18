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
    echo "Killing container"
    docker kill `docker ps |
                    grep pong-server |
                    grep -v nginx |
                    awk '{print $1}'`

    echo "Deleting container"
    docker rm `docker ps -a |
                   grep pong-server |
                   grep -v nginx |
                   awk '{print $1}'`

    echo "Starting container"
    find ./src/game_server -name '*.py' |
        entr -z -d sh -c 'make -C ~/git/transcendence/ &&
                          echo "Container started" &&
                          tail -f /dev/null'

done
