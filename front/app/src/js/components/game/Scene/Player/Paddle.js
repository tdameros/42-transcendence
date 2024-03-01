import * as THREE from 'three';
import {jsonToVector3} from '../../jsonToVector3';
import {Segment2} from '../Segment2';

export class Paddle {
  #threeJSGroup = new THREE.Group();
  #moveSpeed;
  #movement;

  #paddleObject;
  #light;

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
    this.#paddleIsOnTheRight = this.#threeJSGroup.position.x > 0.;
    const color = this.#getColor();
    this.#addPaddleToGroup(color);
    this.#addLightToGroup(color);

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
        positionJson['z']);

    this.#setCollisionSegments();
  }

  getPosition() {
    return this.#threeJSGroup.position;
  }

  get threeJSGroup() {
    return this.#threeJSGroup;
  }

  #getColor() {
    if (this.#paddleIsOnTheRight) {
      return new THREE.Color(0xff1111);
    } else {
      return new THREE.Color(0x11ff11);
    }
  }

  #addPaddleToGroup(color) {
    this.#paddleObject = new THREE.Mesh(
        new THREE.BoxGeometry(this.#paddleSize.x,
            this.#paddleSize.y,
            this.#paddleSize.z),
        new THREE.MeshStandardMaterial({color: color}));
    this.#paddleObject.position.set(0., 0., 0.25);
    this.#paddleObject.castShadow = true;
    this.#paddleObject.receiveShadow = false;
    this.#threeJSGroup.add(this.#paddleObject);
  }

  #addLightToGroup(color) {
    this.#light = new THREE.RectAreaLight(color, 10., 1., 5.);

    const xDirectionToLookAt = 1.;
    if (this.#paddleIsOnTheRight) {
      this.#light.position.set(-(this.#paddleSize.x * 0.5), 0., -0.25);
      this.#light.lookAt(-xDirectionToLookAt, 0., 0.);
    } else {
      this.#light.position.set(this.#paddleSize.x * 0.5, 0., -0.25);
      this.#light.lookAt(xDirectionToLookAt, 0., 0.);
    }
    this.#threeJSGroup.add(this.#light);
  }

  #setCollisionSegments() {
    const xLeft = this.#playerPosition.x + this.#threeJSGroup.position.x -
            this.#paddleSize.x * 0.5;
    const xRight = this.#playerPosition.x + this.#threeJSGroup.position.x +
            this.#paddleSize.x * 0.5;

    const yTop = this.#playerPosition.y + this.#threeJSGroup.position.y +
            this.#paddleSize.y * 0.5;
    const yBottom = this.#playerPosition.y + this.#threeJSGroup.position.y -
            this.#paddleSize.y * 0.5;

    const topLeft = new THREE.Vector2(xLeft, yTop);
    const topRight = new THREE.Vector2(xRight, yTop);
    const bottomRight = new THREE.Vector2(xRight, yBottom);
    const bottomLeft = new THREE.Vector2(xLeft, yBottom);

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

  changeSide() {
    this.#threeJSGroup.position.set(this.#threeJSGroup.position.x * -1.,
        this.#threeJSGroup.position.y,
        this.#threeJSGroup.position.z);
    this.#paddleIsOnTheRight = !this.#paddleIsOnTheRight;
    this.#threeJSGroup.remove(this.#paddleObject);
    this.#threeJSGroup.remove(this.#light);
    const color = this.#getColor();
    this.#addPaddleToGroup(color);
    this.#addLightToGroup(color);
    this.#setCollisionSegments();
  }
}
