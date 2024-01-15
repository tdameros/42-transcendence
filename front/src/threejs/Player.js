import * as THREE from "three";
import {Scene} from "./Scene";
import {jsonToVector3} from "./Engine/jsonToVector3";

export class Player {
    #playerObject;
    #direction;

    constructor(player, direction) {
        this.#playerObject = player;
        this.#direction = direction;
    }

    updatePosition(time_ratio) {
        const movement = this.#direction * time_ratio;
        this.#playerObject.position.y += movement;
    }

    updateDirection(y) {
        this.#direction = y;
    }

    get position() {
        return this.#playerObject.position;
    }

    set position(position) {
        this.#playerObject.position.set(position.x,
                                        position.y,
                                        position.z);
    }
}