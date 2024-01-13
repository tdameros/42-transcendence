import {Scene} from '../../Scene';

import {io} from 'socket.io-client';

export class _GameSocketIO {
    #engine
    #socketIO

    constructor(engine, uri) {
        this.#engine = engine;
        this.#initGameSocketIO(uri);
    }

    #initGameSocketIO(uri) {
        // TODO use uri not uri[0]. I currently do this because I need the
        //      server to send me a user_id so that I can test properly
        this.#socketIO = io(uri[0], {
            query: JSON.stringify({
                'json_web_token': {
                    'user_id': uri[1],
                },
            }),
        });

        this.#socketIO.on('connect', () => {
            console.log('connection to game server established');
        });

        this.#socketIO.on('connect_error', (error) => {
            console.error('Connection error:', error);
        });

        this.#socketIO.on('disconnect', () => {
            console.log('disconnected from game server');
        });

        this.#socketIO.on('error', async (message) => {
            console.error('Server error message: ', message);
        });

        this.#socketIO.on('debug', (message) => {
            console.log('Server debug message: ', message);
        });

        this.#socketIO.on('scene', (data) => {
            console.log('game scene received');
            // this.#engine.stopAnimationLoop();
            const scene = data['scene'];
            this.#engine.scene = new Scene(scene['boards'],
                                           scene['balls'],
                                           scene['players'],
                                           scene['player_move_speed'],
                                           data['player_index']);
            this.#engine.startListeningForKeyHooks();
        });

        this.#socketIO.on('update_player', (data) => {
            const player_index = data['player_index']
            this.#engine.scene
                        .updateOtherPlayerMovement(player_index,
                                                   data['direction']);
            this.#engine.scene
                        .updateOtherPlayerPosition(player_index,
                                                   data['position'])
        });

        this.#socketIO.connect();
    }

    emit(event, data) {
        this.#socketIO.emit(event, data);
    }
}