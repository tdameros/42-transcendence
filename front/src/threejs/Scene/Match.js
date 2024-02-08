import * as THREE from 'three';

import {Player} from './Player/Player';
import {Ball} from './Ball';
import {BallBoundingBox, PaddleBoundingBox} from './boundingBoxes';

export class Match {
  #threeJSGroup = new THREE.Group();
  #players = [];
  #ball;
  #ballBoundingBox;
  #paddleBoundingBox;
  #ballIsWaiting;
  #ballStartTime;

  constructor(matchJson) {
    this.#ball = new Ball(matchJson['ball']);
    this.#ballIsWaiting = matchJson['ball_is_waiting'];
    this.#ballStartTime = matchJson['ball_start_time'];

    const playersJson = matchJson['players'];
    this.#players.push(new Player(playersJson[0]));
    this.#players.push(new Player(playersJson[1]));

    const position = matchJson['position'];
    this.#threeJSGroup.position.set(position['x'],
        position['y'],
        position['z']);
    this.#threeJSGroup.add(this.#players[0].threeJSGroup);
    this.#threeJSGroup.add(this.#players[1].threeJSGroup);
    this.#threeJSGroup.add(this.#ball.threeJSGroup);

    this.#ballBoundingBox = new BallBoundingBox(playersJson[0],
        matchJson['ball']['radius']);
    this.#paddleBoundingBox = new PaddleBoundingBox(playersJson[0]);
  }

  updateFrame(timeDelta, currentTime) {
    this.#players[0].updateFrame(timeDelta, this.#paddleBoundingBox);
    this.#players[1].updateFrame(timeDelta, this.#paddleBoundingBox);

    if (this.#ballIsWaiting && currentTime >= this.#ballStartTime) {
      this.#ballIsWaiting = false;
    }
    if (this.#ballIsWaiting === false) {
      this.#ball.updateFrame(timeDelta,
          this.#ballBoundingBox,
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

  get threeJSGroup() {
    return this.#threeJSGroup;
  }

  get players() {
    return this.#players;
  }
}
