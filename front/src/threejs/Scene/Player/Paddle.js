import * as THREE from "three";
import {jsonToVector3} from "../../jsonToVector3";
import {Segment2} from "../Segment2";

export class Paddle {
    #threeJSGroup = new THREE.Group();
    #moveSpeed;
    #movement;

    #topCollisionSegment;
    #frontCollisionSegment;
    #bottomCollisionSegment;

    #playerPosition;
    #paddleSize;
    #paddleIsOnTheRight;

    constructor(paddleJson, playerPosition) {
        this.#moveSpeed = paddleJson['move_speed'];
        this.#movement = jsonToVector3(paddleJson['movement']);

        const position = jsonToVector3(paddleJson['position']);
        this.#threeJSGroup.position.set(position.x,
                                        position.y,
                                        position.z);

        this.#paddleSize = jsonToVector3(paddleJson['size']);
        if (this.#threeJSGroup.position.x < 0.) {
            this.#paddleIsOnTheRight = false;
            const color = new THREE.Color(0x00ff00);
            this.#addPaddleToGroup(color);
            this.#addLightToGroup(color);
        } else {
            this.#paddleIsOnTheRight = true;
            const color = new THREE.Color(0xff0000);
            this.#addPaddleToGroup(color);
            this.#addLightToGroup(color);
        }

        this.#playerPosition = playerPosition;

        this.#setCollisionSegments();
    }

    updateFrame(timeDelta, paddleBoundingBox) {
        const movement = new THREE.Vector3().copy(this.#movement)
                                            .multiplyScalar(timeDelta);
        this.#threeJSGroup.position.add(movement);

        if (this.#threeJSGroup.position.y < paddleBoundingBox.y_min) {
            this.#threeJSGroup.position.y = paddleBoundingBox.y_min;
        } else if (this.#threeJSGroup.position.y > paddleBoundingBox.y_max) {
            this.#threeJSGroup.position.y = paddleBoundingBox.y_max;
        }

        this.#setCollisionSegments();
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

        this.#setCollisionSegments();
    }

    getPosition() {
        return this.#threeJSGroup.position;
    }

    get threeJSGroup() {
        return this.#threeJSGroup;
    }

    #addPaddleToGroup(color) {
        const geometry = new THREE.BoxGeometry(this.#paddleSize.x,
                                               this.#paddleSize.y,
                                               this.#paddleSize.z)
        const player = new THREE.Mesh(geometry,
                                      new THREE.MeshStandardMaterial({color: color,
                                                                      emissive: color}));
        player.position.set(0., 0., 0.);
        player.castShadow = true;
        player.receiveShadow = false;
        this.#threeJSGroup.add(player);
    }

    #addLightToGroup(color) {
        const light = new THREE.RectAreaLight(color, 100., 1., 5.);

        const xDirectionToLookAt = 999999999999999.;
        if (this.#paddleIsOnTheRight) {
            light.position.set(-(this.#paddleSize.x * 0.5), 0., 0.);
            light.lookAt(-xDirectionToLookAt, 0., 0.);
        } else {
            light.position.set(this.#paddleSize.x * 0.5, 0., 0.);
            light.lookAt(xDirectionToLookAt, 0., 0.);
        }
        this.#threeJSGroup.add(light);
    }

    #setCollisionSegments() {
        const x_left = this.#playerPosition.x + this.#threeJSGroup.position.x
            - this.#paddleSize.x * 0.5;
        const x_right = this.#playerPosition.x + this.#threeJSGroup.position.x
            + this.#paddleSize.x * 0.5;

        const y_top = this.#playerPosition.y + this.#threeJSGroup.position.y
            + this.#paddleSize.y * 0.5;
        const y_bottom = this.#playerPosition.y + this.#threeJSGroup.position.y
            - this.#paddleSize.y * 0.5;

        const topLeft = new THREE.Vector2(x_left, y_top);
        const topRight = new THREE.Vector2(x_right, y_top);
        const bottomRight = new THREE.Vector2(x_right, y_bottom);
        const bottomLeft = new THREE.Vector2(x_left, y_bottom);

        this.#topCollisionSegment = new Segment2(topLeft, topRight);
        this.#bottomCollisionSegment = new Segment2(bottomLeft, bottomRight);
        if (this.#paddleIsOnTheRight) {
            this.#frontCollisionSegment = new Segment2(topLeft, bottomLeft);
        } else {
            this.#frontCollisionSegment = new Segment2(topRight, bottomRight);
        }
    }

    get topCollisionSegment() {
        return this.#topCollisionSegment;
    }

    get frontCollisionSegment() {
        return this.#frontCollisionSegment;
    }

    get bottomCollisionSegment() {
        return this.#bottomCollisionSegment;
    }
}
