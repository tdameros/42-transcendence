import {Scene} from '../Scene/Scene.js';

import {io} from 'socket.io-client';
import {PlayerLocation} from '../Scene/PlayerLocation.js';
import {sleep} from '../sleep.js';

import {userManagementClient} from '@utils/api/index.js';

export class _GameSocketIO {
  #engine;
  #socketIO;

  constructor(engine, URI) {
    this.#engine = engine;
    this.#initGameSocketIO(URI);
  }

  #initGameSocketIO(URI) {
    console.log(userManagementClient.userId);
    this.#socketIO = io(URI, {
      query: JSON.stringify({
        'json_web_token': {
          'user_id': userManagementClient.userId,
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

      this.#engine.scene = new Scene(
          data['scene'],
          data['player_location'],
      );
      this.#engine.startListeningForKeyHooks();
    });

    this.#socketIO.on('update_paddle', async (data) => {
      while (! (this.#engine.scene instanceof Scene)) {
        await sleep(50);
      }
      console.log('update_paddle received');

      const paddle = new PlayerLocation(data['player_location'])
          .getPlayerFromScene(this.#engine.scene).paddle;
      paddle.setDirection(data['direction']);
      paddle.setPosition(data['position']);
    });

    this.#socketIO.on('prepare_ball_for_match', async (data) => {
      while (! (this.#engine.scene instanceof Scene)) {
        await sleep(50);
      }
      console.log('prepare_ball_for_match received');

      const match = this.#engine.scene
          .getMatchFromLocation(data['match_location']);
      match.prepare_ball_for_match(
          data['ball_start_time'],
          data['ball_movement'],
      );
    });

    this.#socketIO.on('update_ball', async (data) => {
      while (! (this.#engine.scene instanceof Scene)) {
        await sleep(50);
      }
      console.log('update_ball received');

      const match = this.#engine.scene
          .getMatchFromLocation(data['match_location']);
      match.setBallMovement(data['movement']);
      match.setBallPosition(data['position']);
    });

    this.#socketIO.on('player_won_match', async (data) => {
      while (! (this.#engine.scene instanceof Scene)) {
        await sleep(50);
      }
      console.log('player_won_match received');

      const winnerIndex = data['winner_index'];
      const finishedMatchLocation = data['finished_match_location'];
      this.#engine.scene.removeLooserFromMatch(
          finishedMatchLocation, 1 - winnerIndex,
      );

      const winner = this.#engine.scene
          .getMatchFromLocation(finishedMatchLocation)
          .players[winnerIndex];

      const newMatchJson = data['new_match_json'];
      this.#engine.scene.createMatchIfDoesntExist(newMatchJson);

      this.#engine.scene.addWinnerToMatch(
          newMatchJson['location'], winner, winnerIndex,
      );

      this.#engine.scene.deleteMatch(finishedMatchLocation);
    });

    this.#socketIO.connect();
  }

  emit(event, data) {
    this.#socketIO.emit(event, data);
  }
}
