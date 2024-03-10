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

  #rightColor = 0xff1111;
  #leftColor = 0x11ff11;

  #startingPosition;
  #positionChange;
  #startingColor;
  #endingColor;

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

  animate(t, isChangingSide) {
    if (t >= 1.) {
      if (isChangingSide) {
        this.changeSide();
      }
      return;
    }
    if (isChangingSide) {
      const color = this.#mergeColor(t);
      this.#paddleObject.material.color = color;
      this.#light.color = color;
    }

    this.#threeJSGroup.position.set(this.#threeJSGroup.position.x,
        this.#startingPosition + this.#positionChange * t,
        this.#threeJSGroup.position.z,
    );
  }

  #mergeColor(t) {
    const red = (this.#startingColor >> 16) * (1. - t) +
        (this.#endingColor >> 16) * t;
    const green = ((this.#startingColor & 0xff00) >> 8) * (1. - t) +
        ((this.#endingColor & 0xff00) >> 8) * t;
    const blue = (this.#startingColor & 0xff) * (1. - t) +
        (this.#endingColor & 0xff) * t;
    return new THREE.Color((red << 16) | (green << 8) | blue);
  }

  startAnimation() {
    this.#startingPosition = this.#threeJSGroup.position.y;
    this.#positionChange = -this.#startingPosition;
    if (this.#paddleIsOnTheRight) {
      this.#startingColor = this.#rightColor;
      this.#endingColor = this.#leftColor;
    } else {
      this.#startingColor = this.#leftColor;
      this.#endingColor = this.#rightColor;
    }
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

  setYPosition(y) {
    this.#threeJSGroup.position.y = y;
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
      return new THREE.Color(this.#rightColor);
    } else {
      return new THREE.Color(this.#leftColor);
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
    this.#light = new THREE.PointLight(color, 20., 10.);
    this.#light.position.z += this.#paddleSize.z * 2;
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
      this.#frontCollisionSegment = new Segment2(bottomLeft, topLeft);
    } else {
      this.#frontCollisionSegment = new Segment2(bottomRight, topRight);
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

  get paddleIsOnTheRight() {
    return this.#paddleIsOnTheRight;
  }

  changeSide() {
    this.#threeJSGroup.position.set(this.#threeJSGroup.position.x * -1.,
        0.,
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
