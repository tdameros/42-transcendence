import * as THREE from 'three';

export class Ball {
    #ball;
    #light;
    #direction;

    constructor(ball, light, jsonDirection) {
        this.#ball = ball;
        this.#light = light;
        this.#direction = new THREE.Vector3(jsonDirection['x'],
                                            jsonDirection['y'],
                                            jsonDirection['z']);
    }

    updatePosition(time_ratio) {
        const movement = new THREE.Vector3().copy(this.#direction)
                                            .multiplyScalar(time_ratio);
        this.#ball.position.add(movement);
        this.#light.position.add(movement);
    }

    updateDirection(jsonDirection) {
        this.#direction = new THREE.Vector3(jsonDirection['x'],
                                            jsonDirection['y'],
                                            jsonDirection['z']);
    }
}