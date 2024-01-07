import {io} from 'socket.io-client';
import {Scene} from '../Scene';

export class _GameSocketIO {
    constructor(engine, uri) {
        this._engine = engine;
        this._initGameSocketIO(uri);
    }

    _initGameSocketIO(uri) {
        this._socket = io(uri, {
            query: {
                'json_web_token': {
                    'player_id': 'player_1', // TODO use client account primary key
                },
            },
        });

        this._socket.on('connect', () => {
            console.log('connection to game server established');
        });

        this._socket.on('connect_error', (error) => {
            console.error('Connection error:', error);
        });

        this._socket.on('disconnect', () => {
            console.log('disconnected from game server');
        });

        this._socket.on('debug', (message) => {
            console.warn('Server debug message: ', message);
        });

        this._socket.on('scene', (sceneData) => {
            console.log('scene data received');
            this._engine.stopAnimationLoop();
            this._engine._scene = new Scene(sceneData['boards'],
                                            sceneData['balls'],
                                            sceneData['players']);
        });

        this._socket.on('update_player_movement', (data) => {
            this._engine._scene.updatePlayerMovement(data);
        });

        this._socket.connect();
    }

    emit(event, data) {
        this._socket.emit(event, data);
    }
}