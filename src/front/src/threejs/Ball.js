import * as THREE from "three";

export class Ball {
    constructor(ball, light, jsonDirection) {
        this._ball = ball;
        this._light = light;
        this._direction = new THREE.Vector3(jsonDirection["x"],
            jsonDirection["y"],
            jsonDirection["z"]);
    }

    updatePosition(time_ratio) {
        const movement = new THREE.Vector3().copy(this._direction).multiplyScalar(time_ratio);
        this._ball.position.add(movement);
        this._light.position.add(movement);
    }

    updateDirection(jsonDirection) {
        this._direction = new THREE.Vector3(jsonDirection["x"],
            jsonDirection["y"],
            jsonDirection["z"]);
    }
}