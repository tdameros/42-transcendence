(
    `sed 's/^/export /' ~/git/transcendence/common/src/.env`
    export PONG_GAME_SERVERS_MIN_PORT=42200
    export PONG_GAME_SERVERS_MAX_PORT=42210
    export GAME_SERVER_PATH=~/git/transcendence/pong_server/src/game_server/
    export PATH_TO_SSL_CERTS=~/git/transcendence/ssl/certs/
    export DEBUG=True

    cd src/game_creator/
    python3 manage.py test
)
exit_code=$?

kill -9 `pgrep '[P]ython'`

exit $exit_code
