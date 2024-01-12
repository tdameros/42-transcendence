import * as THREE from "three";
import {Scene} from "./Scene";
import {jsonToVector3} from "./Engine/jsonToVector3";

export class Player {
    constructor(player, direction) {
        this._playerObject = player;
        this._direction = direction;
    }

    updatePosition(time_ratio) {
        const movement = this._direction * time_ratio;
        this._playerObject.position.y += movement;
    }

    updateDirection(y) {
        this._direction = y;
    }

    getPosition() {
        return this._playerObject.position;
    }

    setPosition(position) {
        this._playerObject.position.set(position['x'],
                                        position['y'],
                                        position['z']);
    }
}