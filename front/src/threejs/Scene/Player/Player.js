import * as THREE from "three";
import {_Board} from "./_Board";
import {_Paddle} from "./_Paddle";

export class Player {
    #threeJSGroup = new THREE.Group();
    #moveSpeed;
    #board;
    #paddle;


    constructor(playerJson) {
        this.#moveSpeed = playerJson['move_speed'];
        this.#board = new _Board(playerJson['board']);
        this.#paddle = new _Paddle(playerJson['paddle']);

        this.#threeJSGroup.add(this.#board.threeJSBoard);
        this.#threeJSGroup.add(this.#paddle.threeJSGroup);

        const position = playerJson['position'];
        this.#threeJSGroup.position.set(position['x'],
                                        position['y'],
                                        position['z']);
    }

    updateFrame(timeDelta) {
        this.#paddle.updateFrame(timeDelta);
        this.#board.updateFrame(timeDelta);
    }

    get threeJSGroup() {
        return this.#threeJSGroup;
    }

    setPaddleDirection(direction) {
        this.#paddle.setDirection(direction);
    }

    setPaddlePosition(positionJson) {
        this.#paddle.setPosition(positionJson);
    }

    getPaddlePosition() {
        return this.#paddle.getPosition();
    }
}