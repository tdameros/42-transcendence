import {_GameSocketIO} from './_GameSocketIO';

import {io} from 'socket.io-client';

export class _RedirectionSocketIO {
    constructor(engine, gameSocketIOClass = _GameSocketIO) {
        this._engine = engine;
        this._initRedirectionSocketIO(gameSocketIOClass);
    }

    _initRedirectionSocketIO(gameSocketIOClass) {
        this._socketIO = io('http://localhost:4242', { // TODO use real server address
            query: JSON.stringify({
                'json_web_token': {
                    'user_id': '0', // TODO use client account primary key
                },
                'game_id': 'game_1',
            }),
        });

        this._socketIO.on('connect_error', (arg_string) => {
            const arg = JSON.parse(arg_string.message)

            console.log(arg)

            if (arg.hasOwnProperty('error')) {
                console.error('Connection error:', arg['error']);
                return ;
            }

            const gameServerUri = arg['game_server_uri']
            console.log('game_server_uri received: ', gameServerUri);
            this._engine.setSocket(new gameSocketIOClass(this._engine, gameServerUri));
        });

        this._socketIO.connect();
    }

    emit(event, data) {
        this._socketIO.emit(event, data);
    }
}