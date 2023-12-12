import * as THREE from "three";
import {Scene} from "./Scene";

export class Player {
    constructor(player, light, jsonDirection, _ballToLookAt) {
        this._player = player;
        this._light = light;
        this._direction = Scene.jsonToVector3(jsonDirection);
    }

    updatePosition(time_ratio) {
        const movement = new THREE.Vector3().copy(this._direction).multiplyScalar(time_ratio);
        this._player.position.add(movement);
        this._light.position.add(movement);
    }

    updateDirection(jsonDirection) {
        this._direction = Scene.jsonToVector3(jsonDirection);
    }
}