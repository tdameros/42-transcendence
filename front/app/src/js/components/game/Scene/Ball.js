import * as THREE from 'three';
import {jsonToVector3} from '../jsonToVector3';
import {Segment2} from './Segment2';

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

  updateFrame(timeDelta, matchBoundingBox, leftPaddle, rightPaddle) {
    if (this.#movement.x === 0.) return;

    const previousPosition = new THREE.Vector2(this.#threeJSGroup.position.x,
        this.#threeJSGroup.position.y);

    const radiusCompensator = this.#movement.clone()
        .normalize()
        .multiplyScalar(this.#radius / 2.);
    this.#threeJSGroup.position.add(this.#movement.clone()
        .multiplyScalar(timeDelta)
        .add(radiusCompensator));

    const travel = new Segment2(previousPosition,
        this.#threeJSGroup.position);

    if (this.#handleCollisions(travel,
        matchBoundingBox,
            this.#movement.x < 0. ? leftPaddle : rightPaddle,
            timeDelta)) {
      this.#threeJSGroup.position.sub(radiusCompensator);
    }
  }

  #handleCollisions(travel, matchBoundingBox, paddle, timeDelta) {
    if (this.#handlePaddleCollision(travel, paddle, timeDelta)) {
      return true;
    }

    if (this.#handleMatchPoint(matchBoundingBox)) {
      return false;
    }

    this.#handleBoardCollision(matchBoundingBox);
    return true;
  }

  #handlePaddleCollision(travel, paddle, timeDelta) {
    const {point: topIntersection,
      t: topT} = travel.intersect(paddle.topCollisionSegment);
    const {point: frontIntersection,
      t: frontT} = travel.intersect(paddle.frontCollisionSegment);
    const {point: bottomIntersection,
      t: bottomT} = travel.intersect(paddle.bottomCollisionSegment);

    const {
      closestIntersection,
      closestT,
      axeToChange,
      yDirection,
    } = this.#getClosestIntersection(topIntersection, topT,
        frontIntersection, frontT,
        bottomIntersection, bottomT);

    if (closestIntersection === null) return false;

    this.#threeJSGroup.position.set(closestIntersection.x,
        closestIntersection.y,
        this.#threeJSGroup.position.z);

    if (axeToChange === 'x') {
      this.#movement.x = -this.#movement.x * this.#acceleration;
    } else if ((yDirection === '+' && this.#movement.y < 0.) ||
                (yDirection === '-' && this.#movement.y > 0.)) {
      this.#movement.y = -this.#movement.y * this.#acceleration;
    }
    this.#threeJSGroup.position
        .add(this.#movement.clone()
            .multiplyScalar(timeDelta * (1. - closestT)));
    return true;
  }

  #handleMatchPoint(matchBoundingBox) {
    if (this.#threeJSGroup.position.x <= matchBoundingBox.x_min) {
      this.#threeJSGroup.position.x = matchBoundingBox.x_min;
      this.#movement.set(0., 0., 0.);
      return true;
    } else if (this.#threeJSGroup.position.x >= matchBoundingBox.x_max) {
      this.#threeJSGroup.position.x = matchBoundingBox.x_max;
      this.#movement.set(0., 0., 0.);
      return true;
    } // TODO This should mark a point
    return false;
  }

  #handleBoardCollision(matchBoundingBox) {
    if (this.#threeJSGroup.position.y < matchBoundingBox.y_min) {
      const oppositeMovement =
          (matchBoundingBox.y_min - this.#threeJSGroup.position.y) *
                this.#acceleration;
      this.#threeJSGroup.position.y = matchBoundingBox.y_min + oppositeMovement;

      this.#movement.y = -this.#movement.y * this.#acceleration;
    } else if (this.#threeJSGroup.position.y > matchBoundingBox.y_max) {
      const oppositeMovement =
          (matchBoundingBox.y_max - this.#threeJSGroup.position.y) *
                this.#acceleration;
      this.#threeJSGroup.position.y = matchBoundingBox.y_max + oppositeMovement;

      this.#movement.y = -this.#movement.y * this.#acceleration;
    }
  }

  #getClosestIntersection(topIntersection, topT,
      frontIntersection, frontT,
      bottomIntersection, bottomT) {
    let closestIntersection = null;
    let closestT = Number.MAX_VALUE;
    let axeToChange = null;
    let yDirection = null;

    if (topIntersection !== null) {
      closestIntersection = topIntersection;
      closestT = topT;
      axeToChange = 'y';
      yDirection = '+';
    }
    if (frontIntersection !== null) {
      if (frontT < closestT) {
        closestIntersection = frontIntersection;
        closestT = frontT;
        axeToChange = 'x';
      }
    }
    if (bottomIntersection !== null) {
      if (bottomT < closestT) {
        return {closestIntersection: bottomIntersection,
          closestT: closestT,
          axeToChange: 'y',
          yDirection: '-'};
      }
    }
    return {closestIntersection: closestIntersection,
      closestT: closestT,
      axeToChange: axeToChange,
      yDirection: yDirection};
  }

  #addBallToGroup() {
    const ball = new THREE.Mesh(new THREE.SphereGeometry(this.#radius, 10, 10),
        new THREE.MeshStandardMaterial({color: 0xFFFFFF,
          emissive: 0xFFFFFF}));
    ball.position.set(0., 0., 0.);
    ball.castShadow = false;
    ball.receiveShadow = false;
    this.#threeJSGroup.add(ball);
  }

  #addLightToGroup() {
    const light = new THREE.PointLight(0xFFFFFF, 75.0, 40.);
    light.position.set(0., 0., 0.);
    light.castShadow = true;
    this.#threeJSGroup.add(light);
  }

  get threeJSGroup() {
    return this.#threeJSGroup;
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
}
