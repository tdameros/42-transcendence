import * as THREE from "three";
import {jsonToVector3} from "../jsonToVector3";

export class Ball {
    #threeJSGroup = new THREE.Group();
    #movement;

    constructor(ballJson) {
        this.#addBallToGroup(ballJson['radius']);
        this.#addLightToGroup();

        const position = ballJson['position'];
        this.#threeJSGroup.position.set(position['x'],
                                        position['y'],
                                        position['z']);

        this.#movement = jsonToVector3(ballJson['movement']);
    }

    updateFrame(timeDelta) {
        const movement = new THREE.Vector3().copy(this.#movement)
                                                     .multiplyScalar(timeDelta);
        this.#threeJSGroup.position.add(movement);
    }

    #addBallToGroup(radius) {
        let ball = new THREE.Mesh(new THREE.SphereGeometry(radius, 10, 10),
                                  new THREE.MeshStandardMaterial({color: 0xFFFFFF,
                                                                  emissive: 0xFFFFFF}));
        ball.position.set(0., 0., 0.);
        ball.castShadow = false;
        ball.receiveShadow = false;
        this.#threeJSGroup.add(ball);
    }

    #addLightToGroup() {
        let light = new THREE.PointLight(0xFFFFFF, 500.0, 25.);
        light.position.set(0., 0., 0.);
        light.castShadow = true;
        this.#threeJSGroup.add(light);
    }

    get threeJSGroup() {
        return this.#threeJSGroup;
    }
}