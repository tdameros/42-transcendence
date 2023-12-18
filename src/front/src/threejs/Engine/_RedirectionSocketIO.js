import {io} from "socket.io-client";
import {_GameSocketIO} from "./_GameSocketIO";

export class _RedirectionSocketIO {
    constructor(server) {
        this._server = server;
        this._initRedirectionSocketIO();
    }

    _initRedirectionSocketIO() {
        this._socket = io('http://localhost:4242', { // TODO use real server address
            query: JSON.stringify({
                'json_web_token': {
                    'user_id': 'player_1', // TODO use client account primary key
                },
                'game_id': 'game_1',
            }),
        });

        this._socket.on('connect', () => {
            console.log('connection to redirection server established');
        });

        this._socket.on('disconnect', () => {
            console.log('disconnected from redirection server');
        });

        this._socket.on('error', (message) => {
            console.log('Server error message: ', message);
            this._socket.disconnect();
            this._socket = null;
        });

        this._socket.on('game_server_uri', async (gameServerUri) => {
            console.log('game_server_uri received: ', gameServerUri);
            this._socket.disconnect();
            this._server._socket = new _GameSocketIO(this._server, gameServerUri);
        });

        this._socket.connect();
    }

    emit(event, data) {
        this._socket.emit(event, data);
    }
}