import * as THREE from 'three';
import {
  CollisionHandler} from '@components/pages/local/Scene/CollisionHandler.js';

export class Ball {
  #threeJSGroup = new THREE.Group();
  #movement = new THREE.Vector3(0., 0., 0.);
  #acceleration = 1.1;
  #radius = 1.;
  #mesh;
  #light;

  constructor() {
    this.#addBallToGroup();
    this.#addLightToGroup();
    this.#threeJSGroup.position.set(0., 0., 1.);
  }

  prepareForMatch() {
    this.#threeJSGroup.position.set(0., 0., this.#threeJSGroup.position.z);
    this.randomizeMovement();
  }

  updateFrame(timeDelta, boardSize, match) {
    if (this.#movement.x === 0. || timeDelta === 0.) {
      return;
    }

    const collisionHandler = this.#movement.x < 0. ?
        new CollisionHandler(match.players[0].paddle, boardSize) :
        new CollisionHandler(match.players[1].paddle, boardSize);
    collisionHandler.updateBallPositionAndMovement(timeDelta, match);
  }

  #addBallToGroup() {
    this.#mesh = new THREE.Mesh(
        new THREE.IcosahedronGeometry(this.#radius, 16, 8),
        new THREE.MeshPhysicalMaterial({
          roughness: 0.5,
          metalness: 1,
          color: 0xffffff,
        }),
    );
    this.#mesh.position.set(0., 0., 0.);
    this.#mesh.castShadow = false;
    this.#mesh.receiveShadow = false;
    this.#threeJSGroup.add(this.#mesh);
  }

  removeBall() {
    this.#threeJSGroup.remove(this.#mesh);
    this.#threeJSGroup.remove(this.#light);
  }

  #addLightToGroup() {
    this.#light = new THREE.PointLight(0xFFFFFF, 10.0, 10.);
    this.#light.position.set(0., 0., 0.);
    this.#light.castShadow = true;
    this.#threeJSGroup.add(this.#light);
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

  set movement(movement) {
    this.#movement.set(movement.x, movement.y, 0.);
  }

  get movement() {
    return this.#movement;
  }

  randomizeMovement() {
    this.#movement.x = Math.random() < 0.5 ? -1. : 1.;
    this.#movement.y = Math.random() < 0.5 ? -.5 : .5;
    this.#movement.normalize().multiplyScalar(15.);
  }

  setMovementX(x) {
    this.#movement.x = x;
  }

  setMovementY(y) {
    this.#movement.y = y;
  }

  get radius() {
    return this.#radius;
  }
}
