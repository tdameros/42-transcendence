#!/bin/bash

pylint () {
    (
        cd $1 &&
        isort . &&
        flake8 . --max-line-length=95
    )
}

pylint src/game_creator
pylint src/game_server
pylint src/shared_code

pylint src/redirection_server_deprecated
