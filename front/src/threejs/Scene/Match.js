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

  constructor(matchJson) {
    this.#ball = new Ball(matchJson['ball']);

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

  updateFrame(timeDelta) {
    this.#players[0].updateFrame(timeDelta, this.#paddleBoundingBox);
    this.#players[1].updateFrame(timeDelta, this.#paddleBoundingBox);
    this.#ball.updateFrame(timeDelta,
        this.#ballBoundingBox,
        this.#players[0].paddle,
        this.#players[1].paddle);
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
