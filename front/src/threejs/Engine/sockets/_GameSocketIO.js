import {Scene} from '../../Scene';
import {_errorEvent} from './_errorEvent'

import {io} from 'socket.io-client';

export class _GameSocketIO {
    constructor(engine, uri) {
        this._engine = engine;
        this._initGameSocketIO(uri);
    }

    _initGameSocketIO(uri) {
        // TODO use uri not uri[0]. I currently do this because I need the
        //      server to send me a user_id so that I can test properly
        this._socketIO = io(uri[0], {
            query: JSON.stringify({
                'json_web_token': {
                    'user_id': uri[1],
                },
            }),
        });

        this._socketIO.on('connect', () => {
            console.log('connection to game server established');
        });

        this._socketIO.on('connect_error', (error) => {
            console.error('Connection error:', error);
        });

        this._socketIO.on('disconnect', () => {
            console.log('disconnected from game server');
        });

        this._socketIO.on('error', async (message) => {
            await _errorEvent(this, message)
        });

        this._socketIO.on('debug', (message) => {
            console.warn('Server debug message: ', message);
        });

        this._socketIO.on('scene', (sceneData) => {
            console.log('game scene received');
            // this._engine.stopAnimationLoop();
            this._engine._scene = new Scene(sceneData['boards'],
                                            sceneData['balls'],
                                            sceneData['players']);
        });

        this._socketIO.on('update_player_movement', (data) => {
            this._engine._scene.updatePlayerMovement(data);
        });

        this._socketIO.connect();
    }

    emit(event, data) {
        this._socketIO.emit(event, data);
    }
}