import * as THREE from 'three';
import {_Board} from './_Board';
import {Paddle} from './Paddle';

export class Player {
  #threeJSGroup = new THREE.Group();
  #moveSpeed;
  #board;
  #paddle;


  constructor(playerJson) {
    const position = playerJson['position'];
    this.#threeJSGroup.position.set(position['x'],
        position['y'],
        position['z']);

    this.#moveSpeed = playerJson['move_speed'];
    this.#board = new _Board(playerJson['board']);
    this.#paddle = new Paddle(playerJson['paddle'],
        this.#threeJSGroup.position);

    this.#threeJSGroup.add(this.#board.threeJSBoard);
    this.#threeJSGroup.add(this.#paddle.threeJSGroup);
  }

  updateFrame(timeDelta, paddleBoundingBox) {
    this.#paddle.updateFrame(timeDelta, paddleBoundingBox);
    this.#board.updateFrame(timeDelta);
  }

  get threeJSGroup() {
    return this.#threeJSGroup;
  }

  get paddle() {
    return this.#paddle;
  }
}
