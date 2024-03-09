import * as THREE from 'three';

import {Player} from './Player/Player';
import {Ball} from './Ball';

export class Match {
  #engine;

  #threeJSGroup = new THREE.Group();
  #players = [null, null];
  #ball;
  #ballIsWaiting;
  #ballStartTime;
  #pointsToWinMatch = 5;
  #matchIsOver = false;
  #points = [0, 0];

  constructor() {}

  async init(engine) {
    this.#engine = engine;

    this.#ball = new Ball();
    this.prepare_ball_for_match();
    this.#threeJSGroup.add(this.#ball.threeJSGroup);

    this.#threeJSGroup.position.set(30., 23.75, 0.);

    for (let i = 0; i < 2; i++) {
      this.#players[i] = new Player();
      this.#players[i].init(i, this.#pointsToWinMatch);
      this.#threeJSGroup.add(this.#players[i].threeJSGroup);
    }
  }

  updateFrame(timeDelta, currentTime, paddleBoundingBox, boardSize) {
    this.#players[0].updateFrame(timeDelta, paddleBoundingBox);
    this.#players[1].updateFrame(timeDelta, paddleBoundingBox);

    if (!this.#matchIsOver) {
      if (this.#ballIsWaiting && currentTime >= this.#ballStartTime) {
        this.#ballIsWaiting = false;
      }
      if (this.#ballIsWaiting === false) {
        this.#ball.updateFrame(timeDelta, boardSize, this);
      }
    }
  }

  prepare_ball_for_match() {
    this.#ballIsWaiting = true;
    this.#ballStartTime = Number(Date.now()) + 3000.;
    this.#ball.prepareForMatch();
  }

  playerMarkedPoint(playerIndex) {
    this.#points[playerIndex]++;
    this.#players[playerIndex].addPoint();
    if (this.#points[playerIndex] >= this.#pointsToWinMatch) {
      this.#matchIsOver = true;
      this.ball.removeBall();
      this.#engine.component.addEndGameCard(this.#points[0], this.#points[1]);
      return;
    }
    this.prepare_ball_for_match();
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

  get threeJSGroup() {
    return this.#threeJSGroup;
  }

  get players() {
    return this.#players;
  }

  get ball() {
    return this.#ball;
  }

  get ballStartTime() {
    return this.#ballStartTime;
  }
}
