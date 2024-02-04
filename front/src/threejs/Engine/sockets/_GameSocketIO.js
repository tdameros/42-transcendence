import {Scene} from '../../Scene/Scene';

import {io} from 'socket.io-client';

export class _GameSocketIO {
  #engine;
  #socketIO;

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
      this.#engine.scene = new Scene(data['scene']['matches'],
          data['player_location']);
      this.#engine.startListeningForKeyHooks();
    });

    this.#socketIO.on('update_player', (data) => {
      console.log('update_player received');
      const playerLocation = data['player_location'];
      this.#engine.scene
          .setPlayerPaddleDirection(playerLocation,
              data['direction']);
      this.#engine.scene
          .setPlayerPaddlePosition(playerLocation,
              data['position']);
    });

    this.#socketIO.on('update_ball', (data) => {
      console.log('update_ball received');
      const matchIndex = data['match_index'];
      const match = this.#engine.scene.matches[matchIndex];
      match.setBallMovement(data['movement']);
      match.setBallPosition(data['position']);
    });

    this.#socketIO.connect();
  }

  emit(event, data) {
    this.#socketIO.emit(event, data);
  }
}
