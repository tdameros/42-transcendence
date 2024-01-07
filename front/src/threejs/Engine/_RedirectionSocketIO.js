import {io} from 'socket.io-client';
import {_GameSocketIO} from './_GameSocketIO';

export class _RedirectionSocketIO {
    constructor(engine, gameSocketIOClass = _GameSocketIO) {
        this._engine = engine;
        this._initRedirectionSocketIO(gameSocketIOClass);
    }

    _initRedirectionSocketIO(gameSocketIOClass) {
        this._socketIO = io('http://localhost:4242', { // TODO use real server address
            query: JSON.stringify({
                'json_web_token': {
                    'user_id': 'player_1', // TODO use client account primary key
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
            try {
                await this._waitForConnection();
            } catch (e) {
                console.error('_RedirectionSocket error event: ', e);
                return;
            }

            console.error('Server error message: ', message);
            this._socketIO.disconnect();
            this._engine.setSocket(null);
        });

        this._socketIO.on('game_server_uri', async (gameServerUri) => {
            try {
                await this._waitForConnection();
            } catch (e) {
                console.error('_RedirectionSocket game_server_uri event: ', e);
                return;
            }

            console.log('game_server_uri received: ', gameServerUri);
            this._socketIO.disconnect();
            this._engine.setSocket(new gameSocketIOClass(this._engine, gameServerUri));
        });

        this._socketIO.connect();
    }

    async _waitForConnection(waitTime = 100, timeout = 10000) {
        for (let i = 0; !this._socketIO.connected && i < timeout; i += waitTime) {
            await new Promise(resolve => setTimeout(resolve, waitTime));
        }

        if (!this._socketIO.connected) {
            throw new Error('_waitForConnection timed out');
        }
    }

    emit(event, data) {
        this._socketIO.emit(event, data);
    }
}