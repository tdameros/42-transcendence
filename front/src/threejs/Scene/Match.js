import * as THREE from "three";

import {jsonToVector3} from "../jsonToVector3";
import {Player} from "./Player/Player";
import {Ball} from "./Ball";

export class Match {
    #threeJSGroup = new THREE.Group();
    #players = [];
    #ball;

    constructor(matchJson) {
        const playersJson = matchJson['players'];
        this.#players.push(new Player(playersJson[0]));
        this.#players.push(new Player(playersJson[1]));

        this.#ball = new Ball(matchJson['ball']);

        const position = matchJson['position'];
        this.#threeJSGroup.position.set(position['x'],
                                        position['y'],
                                        position['z']);
        this.#threeJSGroup.add(this.#players[0].threeJSGroup);
        this.#threeJSGroup.add(this.#players[1].threeJSGroup);
        this.#threeJSGroup.add(this.#ball.threeJSGroup);
    }

    updateFrame(timeDelta) {
        this.#ball.updateFrame(timeDelta);
        this.#players[0].updateFrame(timeDelta);
        this.#players[1].updateFrame(timeDelta);
    }

    get threeJSGroup() {
        return this.#threeJSGroup;
    }

    get players() {
        return this.#players;
    }
}