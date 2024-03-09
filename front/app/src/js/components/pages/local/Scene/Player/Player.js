import * as THREE from 'three';
import {_Board} from './_Board';
import {Paddle} from './Paddle';

export class Player {
  #threeJSGroup = new THREE.Group();
  #board;
  #paddle;


  constructor() {
  }

  async init(index, pointsToWinMatch) {
    if (index === 0) {
      this.#threeJSGroup.position.set(-10., 0., 0.);
    } else {
      this.#threeJSGroup.position.set(10., 0., 0.);
    }


    this.#paddle = new Paddle(index, this.#threeJSGroup.position);
    this.#threeJSGroup.add(this.#paddle.threeJSGroup);
    this.#board = new _Board();
    await this.#board.init(index, pointsToWinMatch);
    this.#threeJSGroup.add(this.#board.threeJSBoard);
  }

  updateFrame(timeDelta, paddleBoundingBox) {
    this.#paddle.updateFrame(timeDelta, paddleBoundingBox);
    this.#board.updateFrame();
  }

  addPoint() {
    this.#board.addPoint();
  }

  resetPoints() {
    this.#board.resetPoints();
  }

  get score() {
    return this.#board.score;
  }

  get threeJSGroup() {
    return this.#threeJSGroup;
  }

  get paddle() {
    return this.#paddle;
  }

  get board() {
    return this.#board;
  }

  getPosition() {
    return this.#threeJSGroup.position;
  }

  changeSide() {
    this.#threeJSGroup.position.set(this.#threeJSGroup.position.x * -1.,
        this.#threeJSGroup.position.y,
        this.#threeJSGroup.position.z);
    this.#paddle.changeSide();
    this.#board.changeSide();
  }
}
