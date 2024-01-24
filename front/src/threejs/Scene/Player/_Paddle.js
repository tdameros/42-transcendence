import * as THREE from "three";
import {jsonToVector3} from "../../jsonToVector3";

export class _Paddle {
    #threeJSGroup = new THREE.Group();
    #moveSpeed;
    #movement;

    constructor(paddleJson) {
        this.#moveSpeed = paddleJson['move_speed'];
        this.#movement = jsonToVector3(paddleJson['movement']);

        const position = paddleJson['position'];
        this.#threeJSGroup.position.set(position['x'],
                                        position['y'],
                                        position['z']);

        const paddleSize = jsonToVector3(paddleJson['size']);
        if (this.#threeJSGroup.position.x < 0.) {
            const color = new THREE.Color(0x00ff00);
            this.#addPaddleToGroup(color, paddleSize);
            this.#addLightToGroup(color, false, paddleSize.x);
        } else {
            const color = new THREE.Color(0xff0000);
            this.#addPaddleToGroup(color, paddleSize);
            this.#addLightToGroup(color, true, paddleSize.x);
        }
    }

    updateFrame(timeDelta) {
        const movement = new THREE.Vector3().copy(this.#movement)
            .multiplyScalar(timeDelta);
        this.#threeJSGroup.position.add(movement);
    }

    setDirection(direction) {
        if (direction === 'up') {
            this.#movement.y = this.#moveSpeed;
        } else if (direction === 'down') {
            this.#movement.y = -this.#moveSpeed;
        } else {
            this.#movement.y = 0.;
        }
    }

    setPosition(positionJson) {
        this.#threeJSGroup.position.set(positionJson['x'],
                                        positionJson['y'],
                                        positionJson['z'])
    }

    getPosition() {
        return this.#threeJSGroup.position;
    }

    get threeJSGroup() {
        return this.#threeJSGroup;
    }

    #addPaddleToGroup(color, size) {
        const player = new THREE.Mesh(new THREE.BoxGeometry(size.x, size.y, size.z),
                                      new THREE.MeshStandardMaterial({color: color,
                                                                      emissive: color}));
        player.position.set(0., 0., 0.);
        player.castShadow = true;
        player.receiveShadow = false;
        this.#threeJSGroup.add(player);
    }

    #addLightToGroup(color, isPaddleOnTheRight, paddleWidth) {
        const light = new THREE.RectAreaLight(color, 100., 1., 5.);

        const xDirectionToLookAt = 999999999999999.;
        if (isPaddleOnTheRight) {
            light.position.set(-(paddleWidth / 2.), 0., 0.);
            light.lookAt(-xDirectionToLookAt, 0., 0.);
        } else {
            light.position.set(paddleWidth / 2., 0., 0.);
            light.lookAt(xDirectionToLookAt, 0., 0.);
        }
        this.#threeJSGroup.add(light);
    }
}
