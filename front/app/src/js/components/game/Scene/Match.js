import * as THREE from 'three';

import {Player} from './Player/Player';
import {Ball} from './Ball';

export class Match {
  #threeJSGroup = new THREE.Group();
  #players = [null, null];
  #ball;
  #ballIsWaiting;
  #ballStartTime;

  constructor(matchJson) {
    this.#ball = new Ball(matchJson['ball']);
    this.#ballIsWaiting = matchJson['ball_is_waiting'];
    this.#ballStartTime = matchJson['ball_start_time'];

    const position = matchJson['position'];
    this.#threeJSGroup.position.set(position['x'],
        position['y'],
        position['z']);

    const playersJson = matchJson['players'];
    this.#addPlayer(playersJson[0], 0);
    this.#addPlayer(playersJson[1], 1);

    this.#threeJSGroup.add(this.#ball.threeJSGroup);
  }

  updateFrame(timeDelta, currentTime, paddleBoundingBox, ballBoundingBox) {
    if (this.#players[0] !== null) {
      this.#players[0].updateFrame(timeDelta, paddleBoundingBox);
    }
    if (this.#players[1] !== null) {
      this.#players[1].updateFrame(timeDelta, paddleBoundingBox);
    }

    if (this.#ballStartTime === null ||
        this.#players[0] === null || this.#players[1] === null) {
      return;
    }

    if (this.#ballIsWaiting && currentTime >= this.#ballStartTime) {
      this.#ballIsWaiting = false;
    }
    if (this.#ballIsWaiting === false) {
      this.#ball.updateFrame(timeDelta,
          ballBoundingBox,
          this.#players[0].paddle,
          this.#players[1].paddle);
    }
  }

  prepare_ball_for_match(ballStartTime, ballMovementJson) {
    this.#ballIsWaiting = true;
    this.#ballStartTime = ballStartTime * 1000;
    this.#ball.prepareForMatch(ballMovementJson);
  }

  setBallMovement(movementJson) {
    this.#ball.setMovement(movementJson);
  }

  setBallPosition(positionJson) {
    this.#ball.setPosition(positionJson);
  }

  getPosition() {
    return this.#threeJSGroup.position;
  }

  #addPlayer(playerJson, index) {
    if (playerJson !== null) {
      this.#players[index] = new Player(playerJson);
      this.#threeJSGroup.add(this.#players[index].threeJSGroup);
    }
  }

  addPlayer(player, index) {
    this.#players[index] = player;
    this.#threeJSGroup.add(this.#players[index].threeJSGroup);
  }

  popPlayer(index) {
    const player = this.#players[index];
    if (player === null) {
      return null;
    }
    this.#threeJSGroup.remove(player.threeJSGroup);
    this.#players[index] = null;
    return player;
  }

  get threeJSGroup() {
    return this.#threeJSGroup;
  }

  get players() {
    return this.#players;
  }
}
