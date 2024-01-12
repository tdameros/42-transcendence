import {Scene} from '../../Scene';

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
            console.error('Server error message: ', message);
        });

        this._socketIO.on('debug', (message) => {
            console.log('Server debug message: ', message);
        });

        this._socketIO.on('scene', (data) => {
            console.log('game scene received');
            // this._engine.stopAnimationLoop();
            const scene = data['scene'];
            this._engine.setScene(new Scene(scene['boards'],
                                            scene['balls'],
                                            scene['players'],
                                            scene['player_move_speed'],
                                            data['player_index']));
            this._engine.startListeningForKeyHooks();
        });

        this._socketIO.on('update_player', (data) => {
            const player_index = data['player_index']
            this._engine.getScene()
                        .updateOtherPlayerMovement(player_index,
                                                   data['direction']);
            this._engine.getScene()
                        .updateOtherPlayerPosition(player_index,
                                                   data['position'])
        });

        this._socketIO.connect();
    }

    emit(event, data) {
        this._socketIO.emit(event, data);
    }
}