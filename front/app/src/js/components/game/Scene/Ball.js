import * as THREE from 'three';
import {jsonToVector3} from '../jsonToVector3';
import {CollisionHandler} from '@components/game/Scene/CollisionHandler.js';

export class Ball {
  #threeJSGroup = new THREE.Group();
  #movement;
  #acceleration;
  #radius;

  constructor(ballJson) {
    this.#radius = ballJson['radius'];
    this.#addBallToGroup();
    this.#addLightToGroup();

    const position = ballJson['position'];
    this.#threeJSGroup.position.set(position['x'],
        position['y'],
        position['z']);

    this.#acceleration = ballJson['acceleration'];

    this.#movement = jsonToVector3(ballJson['movement']);
  }

  prepareForMatch(ballMovementJson) {
    this.#threeJSGroup.position.set(0., 0., this.#threeJSGroup.position.z);
    this.#movement.set(ballMovementJson['x'],
        ballMovementJson['y'],
        ballMovementJson['z']);
  }

  updateFrame(timeDelta, boardSize, match) {
    if (this.#movement.x === 0. || timeDelta === 0.) {
      return;
    }

    let collisionHandler;
    if (this.#movement.x < 0.) {
      collisionHandler = new CollisionHandler(match.players[0].paddle,
          boardSize);
    } else {
      collisionHandler = new CollisionHandler(match.players[1].paddle,
          boardSize);
    }
    collisionHandler.updateBallPositionAndMovement(
        this, timeDelta, match, this.#radius,
    );
  }

  #addBallToGroup() {
    const ball = new THREE.Mesh(
        new THREE.IcosahedronGeometry(this.#radius, 16, 8),
        new THREE.MeshPhysicalMaterial({
          roughness: 0.5,
          metalness: 1,
          color: 0xffffff,
        }),
    );
    ball.position.set(0., 0., 0.);
    ball.castShadow = false;
    ball.receiveShadow = false;
    this.#threeJSGroup.add(ball);
  }

  #addLightToGroup() {
    const light = new THREE.PointLight(0xFFFFFF, 10.0, 10.);
    light.position.set(0., 0., 0.);
    light.castShadow = true;
    this.#threeJSGroup.add(light);
  }

  get threeJSGroup() {
    return this.#threeJSGroup;
  }

  get acceleration() {
    return this.#acceleration;
  }

  getPosition() {
    return this.#threeJSGroup.position;
  }

  setPosition(positionJson) {
    this.#threeJSGroup.position.set(positionJson['x'],
        positionJson['y'],
        positionJson['z']);
  }

  setMovement(movementJson) {
    this.#movement.set(movementJson['x'],
        movementJson['y'],
        movementJson['z']);
  }

  get movement() {
    return this.#movement;
  }

  setMovementX(x) {
    this.#movement.x = x;
  }

  setMovementY(y) {
    this.#movement.y = y;
  }
}
