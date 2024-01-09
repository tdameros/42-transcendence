import {_GameSocketIO} from './_GameSocketIO';
import {_errorEvent} from "./_errorEvent";
import {_waitForConnection} from "./_waitForConnection";

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

        this._socketIO.on('connect', () => {
            console.log('connection to redirection server established');
        });

        this._socketIO.on('connect_error', (error) => {
            console.error('Connection error:', error);
        });

        this._socketIO.on('disconnect', () => {
            console.log('disconnected from redirection server');
        });

        this._socketIO.on('error', async (message) => {
            await _errorEvent(this, message)
        });

        this._socketIO.on('game_server_uri', async (gameServerUri) => {
            try {
                await _waitForConnection(this._socketIO);
            } catch (e) {
                console.error('_RedirectionSocket game_server_uri event: ', e);
                return;
            }

            console.log('game_server_uri received: ', gameServerUri);
            this._engine.setSocket(new gameSocketIOClass(this._engine, gameServerUri));
        });

        this._socketIO.connect();
    }

    emit(event, data) {
        this._socketIO.emit(event, data);
    }
}