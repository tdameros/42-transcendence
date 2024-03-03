import * as THREE from 'three';
import {_Board} from './_Board';
import {Paddle} from './Paddle';

export class Player {
  #threeJSGroup = new THREE.Group();
  #moveSpeed;
  #board;
  #paddle;


  constructor() {
  }

  async init(playerJson, index) {
    const position = playerJson['position'];
    this.#threeJSGroup.position.set(position['x'],
        position['y'],
        position['z']);

    this.#moveSpeed = playerJson['move_speed'];
    this.#paddle = new Paddle(playerJson['paddle'],
        this.#threeJSGroup.position);

    this.#threeJSGroup.add(this.#paddle.threeJSGroup);
    this.#board = new _Board();
    await this.#board.init(playerJson['board'], index, 3);
    this.#threeJSGroup.add(this.#board.threeJSBoard);
  }

  updateFrame(timeDelta, paddleBoundingBox) {
    this.#paddle.updateFrame(timeDelta, paddleBoundingBox);
    this.#board.updateFrame(timeDelta);
  }

  addPoint() {
    this.#board.addPoint();
  }

  resetPoints() {
    this.#board.resetPoints();
  }
  get threeJSGroup() {
    return this.#threeJSGroup;
  }

  get paddle() {
    return this.#paddle;
  }

  getPosition() {
    return this.#threeJSGroup.position;
  }

  changeSide() {
    this.#threeJSGroup.position.set(this.#threeJSGroup.position.x * -1.,
        this.#threeJSGroup.position.y,
        this.#threeJSGroup.position.z);
    this.#paddle.changeSide();
  }
}
