import {io} from 'socket.io-client';
import {_GameSocketIO} from './_GameSocketIO';

export class _RedirectionSocketIO {
    constructor(server, gameSocketIOClass = _GameSocketIO) {
        this._server = server;
        this._initRedirectionSocketIO(gameSocketIOClass);
    }

    _initRedirectionSocketIO(gameSocketIOClass) {
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

        this._socket.on('connect_error', (error) => {
            console.error('Connection error:', error);
        });

        this._socket.on('disconnect', () => {
            console.log('disconnected from redirection server');
        });

        this._socket.on('error', async (message) => {
            try {
                await this._waitForConnection();
            } catch (e) {
                console.error('_RedirectionSocket error event: ', e);
                return;
            }

            console.error('Server error message: ', message);
            this._socket.disconnect();
            this._server._socket = null;
        });

        this._socket.on('game_server_uri', async (gameServerUri) => {
            try {
                await this._waitForConnection();
            } catch (e) {
                console.error('_RedirectionSocket game_server_uri event: ', e);
                return;
            }

            console.log('game_server_uri received: ', gameServerUri);
            this._socket.disconnect();
            this._server._socket = new gameSocketIOClass(this._server, gameServerUri);
        });

        this._socket.connect();
    }

    async _waitForConnection(waitTime = 100, timeout = 10000) {
        for (let i = 0; !this._socket.connected && i < timeout; i += waitTime) {
            await new Promise(resolve => setTimeout(resolve, waitTime));
        }

        if (!this._socket.connected) {
            throw new Error('_waitForConnection timed out');
        }
    }

    emit(event, data) {
        this._socket.emit(event, data);
    }
}