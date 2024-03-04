import {io} from 'socket.io-client';

import {userManagementClient} from '@utils/api';
import {ToastNotifications} from '@components/notifications';
import {getRouter} from '@js/Router.js';

import {Scene} from '../Scene/Scene.js';
import {PlayerLocation} from '../Scene/PlayerLocation.js';
import {sleep} from '../sleep.js';

export class _GameSocketIO {
  #engine;
  #socketIO;
  #isConnected = false;

  constructor(engine) {
    this.#engine = engine;
  }

  async init(URI) {
    this.#socketIO = io(URI, {
      auth: {
        token: await userManagementClient.getValidAccessToken()},
    });

    this.#socketIO.on('connect', async () => {
      this.#isConnected = true;
    });

    this.#socketIO.on('connect_error', (jsonString) => {
      let error;
      try {
        error = JSON.parse(jsonString.message);
      } catch {
        ToastNotifications.addErrorNotification('Server connection error');
        return;
      }
      if (error['status_code'] !== 0) {
        console.error('Connection error:', error['message']);
        ToastNotifications.addErrorNotification(`Connection error: ${error['message']}`);
      } else {
        ToastNotifications.addErrorNotification('The game is already over');
        getRouter().redirect('/');
      }
    });

    this.#socketIO.on('disconnect', () => {
      console.log('disconnected from game server');
    });

    this.#socketIO.on('fatal_error', async (data) => {
      console.error('Server fatal error: ', data['error_message']);
      ToastNotifications.addErrorNotification(`Server fatal error: ${data['error_message']}`);
      getRouter().redirect('/');
    });

    this.#socketIO.on('debug', (message) => {
      console.log('Server debug message: ', message);
    });

    this.#socketIO.on('scene', async (data) => {
      while (!this.#isConnected) {
        await sleep(50);
      }
      console.log('game scene received');

      const scene = new Scene();
      await scene.init(
          this.#engine,
          data['scene'],
          data['player_location'],
      );
      this.#engine.scene = scene;
      this.#engine.scene.updateCamera();
      this.#engine.startListeningForKeyHooks();
    });

    this.#socketIO.on('update_paddle', async (data) => {
      while (!(this.#engine.scene instanceof Scene)) {
        await sleep(50);
      }
      console.log('update_paddle received');

      const paddle = new PlayerLocation(data['player_location'])
          .getPlayerFromScene(this.#engine.scene).paddle;
      paddle.setDirection(data['direction']);
      paddle.setPosition(data['position']);
    });

    this.#socketIO.on('prepare_ball_for_match', async (data) => {
      while (!(this.#engine.scene instanceof Scene)) {
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
      while (!(this.#engine.scene instanceof Scene)) {
        await sleep(50);
      }
      console.log('update_ball received');

      const match = this.#engine.scene
          .getMatchFromLocation(data['match_location']);
      match.setBallMovement(data['movement']);
      match.setBallPosition(data['position']);
    });

    this.#socketIO.on('player_won_match', async (data) => {
      while (!(this.#engine.scene instanceof Scene)) {
        await sleep(50);
      }
      console.log('player_won_match received');

      const winnerIndex = data['winner_index'];
      const finishedMatchLocation = data['finished_match_location'];
      this.#engine.scene.removeLooserFromMatch(finishedMatchLocation,
          1 - winnerIndex);

      const winner = this.#engine.scene
          .getMatchFromLocation(finishedMatchLocation)
          .players[winnerIndex];

      const newMatchJson = data['new_match_json'];
      await this.#engine.scene.createMatchIfDoesntExist(newMatchJson);

      const newWinnerIndex = finishedMatchLocation['match'] % 2;
      this.#engine.scene.addWinnerToMatch(
          newMatchJson['location'], winner, winnerIndex, newWinnerIndex,
      );
      winner.resetPoints();

      this.#engine.scene.deleteMatch(finishedMatchLocation);

      this.#engine.scene.updateCamera();
    });

    this.#socketIO.on('player_scored_a_point', async (data) => {
      while (!(this.#engine.scene instanceof Scene)) {
        await sleep(50);
      }

      const playerLocation = new PlayerLocation(data['player_location']);
      const match = playerLocation.getPlayerMatchFromScene(this.#engine.scene);
      match.players[playerLocation.playerIndex].addPoint();
    });

    this.#socketIO.on('game_over', async (data) => {
      while (!(this.#engine.scene instanceof Scene)) {
        await sleep(50);
      }
      console.log('game_over received');

      const winnerIndex = data['winner_index'];
      this.#engine.scene.matches[0].players[winnerIndex].addPoint();
      const currentPlayerLocation = this.#engine.scene.currentPlayerLocation;
      if (currentPlayerLocation.isLooser) {
        // TODO Handle the case where the player lost before the final
        this.#engine.component.loadEndGameCard('eliminated', 0, 0);
      } else if (currentPlayerLocation.playerIndex === winnerIndex) {
        // TODO Handle the case when the player wins the game
        const finalMatch = currentPlayerLocation.getPlayerMatchFromScene(
            this.#engine.scene,
        );
        const winnerScore = finalMatch.players[winnerIndex].score;
        const looserScore = finalMatch.players[1 - winnerIndex].score;
        this.#engine.component.loadEndGameCard('win', winnerScore, looserScore);
      } else {
        const finalMatch = currentPlayerLocation.getPlayerMatchFromScene(
            this.#engine.scene,
        );
        const winnerScore = finalMatch.players[winnerIndex].score;
        const looserScore = finalMatch.players[1 - winnerIndex].score;
        this.#engine.component.loadEndGameCard(
            'loose', winnerScore, looserScore,
        );
        // TODO Handle the case when the player looses the game
      }
    });

    this.#socketIO.connect();
  }

  disconnect() {
    try {
      this.#socketIO.disconnect();
    } catch (error) {}
  }

  emit(event, data) {
    try {
      this.#socketIO.emit(event, data);
    } catch (error) {}
  }
}
