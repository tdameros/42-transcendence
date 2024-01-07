import * as THREE from "three";
import {Scene} from "./Scene";

export class Player {
    constructor(player, light, direction, _ballToLookAt) {
        this._player = player;
        this._light = light;
        this._direction = direction;
    }

    updatePosition(time_ratio) {
        const movement = this._direction * time_ratio;
        this._player.position.y += movement;
        this._light.position.y += movement;
    }

    updateDirection(y) {
        this._direction = y;
    }
}