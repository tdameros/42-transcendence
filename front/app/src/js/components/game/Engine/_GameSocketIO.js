import {io} from 'socket.io-client';

import {userManagementClient} from '@utils/api';
import {ToastNotifications} from '@components/notifications';
import {getRouter} from '@js/Router.js';
import {ErrorPage} from '@utils/ErrorPage.js';

import {Scene} from '../Scene/Scene.js';
import {PlayerLocation} from '../Scene/PlayerLocation.js';
import {sleep} from '../sleep.js';
import {CollisionHandler} from '@components/game/Scene/CollisionHandler.js';
import {ServerTime} from '@components/game/ServerTime.js';

export class _GameSocketIO {
  #engine;
  #socketIO;
  #gameHasStarted = false;
  #reconnectAttempts = 0;
  #maxReconnectAttempts = 5;

  constructor(engine) {
    this.#engine = engine;
  }

  async init(URI) {
    if (this.#reconnectAttempts === -1) {
      return;
    }
    if (this.#reconnectAttempts >= this.#maxReconnectAttempts) {
      getRouter().redirect('/');
      return;
    }
    let accessToken;
    try {
      accessToken = await userManagementClient.getValidAccessToken();
      if (accessToken === null) {
        getRouter().redirect('/signin/');
        return;
      }
    } catch (error) {
      ErrorPage.loadNetworkError();
      return;
    }
    this.#socketIO = io(URI, {
      auth: {
        token: accessToken,
      },
    });

    this.#socketIO.on('connect', async () => {
      this.requestTimeSync(Date.now());
    });

    this.#socketIO.on('connect_error', async (jsonString) => {
      await this.#connectErrorHandler(jsonString, URI);
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

    this.#socketIO.on('time_sync', (timeData) => {
      ServerTime.syncServerTime(timeData);
    });

    this.#socketIO.on('scene', async (data) => {
      await this.#sceneEventHandler(data);
    });

    this.#socketIO.on('update_paddle', async (data) => {
      await this.#updatePaddleEventHandler(data);
    });

    this.#socketIO.on('prepare_ball_for_match', async (data) => {
      await this.#prepareBallForMatchEventHandler(data);
    });

    this.#socketIO.on('update_ball', async (data) => {
      await this.#updateBallEventHandler(data);
    });

    this.#socketIO.on('player_won_match', async (data) => {
      await this.#playerWonMatchEventHandler(data);
    });

    this.#socketIO.on('player_scored_a_point', async (data) => {
      await this.#playerScoredAPointEventHandler(data);
    });

    this.#socketIO.on('game_over', async (data) => {
      await this.#gameOverEventHandler(data);
    });

    this.#socketIO.connect();
  }

  requestTimeSync(currentTime) {
    this.emit('request_time_sync', currentTime);
  }

  async #connectErrorHandler(jsonString, URI) {
    let error;
    try {
      error = JSON.parse(jsonString.message);
    } catch {
      ToastNotifications.addErrorNotification('Server connection error');
      this.disconnect(false);
      this.#reconnectAttempts++;
      await sleep(2000);
      await this.init(URI);
      return;
    }
    if (error['status_code'] === 0 || error['status_code'] === 1) {
      ToastNotifications.addErrorNotification(error['message']);
      getRouter().redirect('/');
      return;
    } else {
      console.error('Connection error:', error['message']);
      ToastNotifications.addErrorNotification(`Connection error: ${error['message']}`);
      this.disconnect(false);
      this.#reconnectAttempts++;
      await sleep(2000);
      await this.init(URI);
    }
  }

  async #sceneEventHandler(data) {
    while (!ServerTime.isTimeSynced) {
      await sleep(5);
    }
    const scene = new Scene();
    await scene.init(
        this.#engine,
        data['scene'],
        data['player_location'],
    );
    this.#engine.scene = scene;
    this.#engine.scene.updateCamera();
    this.#engine.displayGameScene();
    this.#gameHasStarted = data['game_has_started'];
    if (this.#gameHasStarted) {
      this.#engine.startListeningForKeyHooks();
    } else {
      this.emit('player_is_ready', {});
      this.#engine.component.addWaitingForOpponent();
      this.#engine.scene.updateCamera(true);
    }
  }

  async #updatePaddleEventHandler(data) {
    while (!(this.#engine.scene instanceof Scene)) {
      await sleep(50);
    }
    console.log('update_paddle received');

    const paddle = new PlayerLocation(data['player_location'])
        .getPlayerFromScene(this.#engine.scene).paddle;
    paddle.setDirection(data['direction']);
    paddle.setPosition(data['position']);
  }

  async #prepareBallForMatchEventHandler(data) {
    while (!(this.#engine.scene instanceof Scene)) {
      await sleep(50);
    }
    console.log('prepare_ball_for_match received');

    const ballStartTime = ServerTime.fixServerTime(data['ball_start_time']);
    if (!this.#gameHasStarted) {
      this.#gameHasStarted = true;
      this.#engine.startListeningForKeyHooks();
      this.#engine.component.removeWaitingForOpponent();
      this.#engine.component.startCountdown(ballStartTime / 1000.);
    }

    const match = this.#engine.scene
        .getMatchFromLocation(data['match_location']);
    match.prepare_ball_for_match(ballStartTime, data['ball_movement']);
  }

  async #updateBallEventHandler(data) {
    while (!(this.#engine.scene instanceof Scene)) {
      await sleep(50);
    }
    console.log('update_ball received');

    const match = this.#engine.scene
        .getMatchFromLocation(data['match_location']);
    const movement = data['movement'];
    match.setBallMovement(movement);
    match.setBallPosition(data['position']);

    const paddle = movement['x'] < 0. ?
        match.players[0].paddle :
        match.players[1].paddle;
    const timeAtUpdate = ServerTime.fixServerTime(data['time_at_update']);
    const now = Number(Date.now());
    const timeDelta = (now - timeAtUpdate + ServerTime.latency) / 1000.;
    if (timeDelta > 0.) {
      new CollisionHandler(paddle, this.#engine.scene.boardSize)
          .updateBallPositionAndMovement(timeDelta, match);
    }
  }

  async #playerWonMatchEventHandler(data) {
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
  }

  async #playerScoredAPointEventHandler(data) {
    while (!(this.#engine.scene instanceof Scene)) {
      await sleep(50);
    }

    const playerLocation = new PlayerLocation(data['player_location']);
    const match = playerLocation.getPlayerMatchFromScene(this.#engine.scene);
    match.players[playerLocation.playerIndex].addPoint();
  }

  async #gameOverEventHandler(data) {
    while (!(this.#engine.scene instanceof Scene)) {
      await sleep(50);
    }
    console.log('game_over received');

    const winnerIndex = data['winner_index'];
    this.#engine.scene.matches[0].players[winnerIndex].addPoint();
    this.#engine.scene.matches[0].ball.removeBall();

    const currentPlayerLocation = this.#engine.scene.currentPlayerLocation;
    if (currentPlayerLocation.isLooser) {
      this.#handleGameOverPlayerHasNotReachedTheFinal();
      return;
    }

    const finalMatch = currentPlayerLocation.getPlayerMatchFromScene(
        this.#engine.scene);
    const winnerScore = finalMatch.players[winnerIndex].score;
    const looserScore = finalMatch.players[1 - winnerIndex].score;

    if (currentPlayerLocation.playerIndex === winnerIndex) {
      if (this.#engine.scene.loosers.length !== 0) {
        this.#handleGameOverPlayerWonTournamentFinal(winnerScore,
            looserScore);
        return;
      }
      this.#handleGameOverPlayerWon1v1(winnerScore, looserScore);
      return;
    }

    if (this.#engine.scene.loosers.length !== 0) {
      this.#handleGameOverPlayerLostTournamentFinal(winnerScore,
          looserScore);
      return;
    }
    this.#handleGameOverPlayerLost1v1(winnerScore, looserScore);
  }

  #handleGameOverPlayerHasNotReachedTheFinal() {
    this.#engine.component.addEndGameCard('eliminated', 0, 0);
  }

  #handleGameOverPlayerWonTournamentFinal(winnerScore, looserScore) {
    this.#engine.component.addEndGameCard('win', winnerScore, looserScore);
  }

  #handleGameOverPlayerWon1v1(winnerScore, looserScore) {
    this.#engine.component.addEndGameCard('win', winnerScore, looserScore);
  }

  #handleGameOverPlayerLostTournamentFinal(winnerScore, looserScore) {
    this.#engine.component.addEndGameCard('loose', winnerScore, looserScore);
  }

  #handleGameOverPlayerLost1v1(winnerScore, looserScore) {
    this.#engine.component.addEndGameCard('loose', winnerScore, looserScore);
  }

  disconnect(stopReconnect = true) {
    try {
      if (stopReconnect) {
        this.#reconnectAttempts = -1;
      }
      this.#socketIO.disconnect();
    } catch (error) {}
  }

  emit(event, data) {
    try {
      this.#socketIO.emit(event, data);
    } catch (error) {}
  }
}
