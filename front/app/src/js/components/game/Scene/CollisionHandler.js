import {Segment2} from '@components/game/Scene/Segment2.js';


class _APhysicalObject {
  constructor() {
    this.intersection = null;
    this.t = null;
  }

  intersect(_travel, _currentClosestPhysicalObjectHit, _ballRadius) {
    throw new Error('Not implemented');
  }

  handleCollision(_travel, _ball, _collisionHandler, _match) {
    throw new Error('Not implemented');
  }
}


class _Wall extends _APhysicalObject {
  constructor(isTop, boardSize) {
    super();
    this.isTop = isTop;
    if (this.isTop) {
      this.y = boardSize.y * 0.5;
    } else {
      this.y = boardSize.y * -0.5;
    }
  }

  intersect(travel, currentClosestPhysicalObjectHit, ballRadius) {
    if (this.isTop) {
      const travelTop = travel.end.y + ballRadius;
      if (travelTop < this.y) {
        return currentClosestPhysicalObjectHit;
      }
      this.intersection = travel.vector.clone()
          .divideScalar(travel.vector.y)
          .multiplyScalar(this.y - travel.begin.y - ballRadius)
          .add(travel.begin);
    } else {
      const travelBottom = travel.end.y - ballRadius;
      if (travelBottom > this.y) {
        return currentClosestPhysicalObjectHit;
      }
      this.intersection = travel.vector.clone()
          .divideScalar(travel.vector.y)
          .multiplyScalar(this.y - travel.begin.y + ballRadius)
          .add(travel.begin);
    }

    this.t = (this.intersection.x - travel.begin.x) / travel.vector.x;

    if (currentClosestPhysicalObjectHit === null) {
      return this;
    }
    if (this.t < currentClosestPhysicalObjectHit.t) {
      return this;
    }
    return currentClosestPhysicalObjectHit;
  }

  handleCollision(travel, ball, collisionHandler, _match) {
    ball.setMovementY(ball.movement.y * -ball.acceleration);
    const newTravelVector = travel.vector.multiplyScalar(1 - this.t);
    newTravelVector.y *= -ball.acceleration;
    return new Segment2(
        this.intersection,
        this.intersection.clone().add(newTravelVector),
        newTravelVector,
    );
  }
}


class _Goal extends _APhysicalObject {
  constructor(isRight, boardSize) {
    super();
    this.isRight = isRight;
    if (this.isRight) {
      this.x = boardSize.x;
    } else {
      this.x = -boardSize.x;
    }
  }

  intersect(travel, currentClosestPhysicalObjectHit, ballRadius) {
    if (this.isRight) {
      const travelRight = travel.end.x + ballRadius;
      if (travelRight < this.x) {
        return currentClosestPhysicalObjectHit;
      }
      this.intersection = travel.vector.clone()
          .divideScalar(travel.vector.x)
          .multiplyScalar(this.x - travel.begin.x - ballRadius)
          .add(travel.begin);
    } else {
      const travelLeft = travel.end.x - ballRadius;
      if (travelLeft > this.x) {
        return currentClosestPhysicalObjectHit;
      }
      this.intersection = travel.vector.clone()
          .divideScalar(travel.vector.x)
          .multiplyScalar(this.x - travel.begin.x + ballRadius)
          .add(travel.begin);
    }

    this.t = (this.intersection.x - travel.begin.x) / travel.vector.x;

    if (currentClosestPhysicalObjectHit === null) {
      return this;
    }
    if (this.t < currentClosestPhysicalObjectHit.t) {
      return this;
    }
    return currentClosestPhysicalObjectHit;
  }

  handleCollision(_travel, _ball, _collisionHandler, _match) {
    // match.playerMarkedPoint(1 - this.isRight);
    // TODO uncomment in single player mode
    return null;
  }
}


class _PhysicalPaddle extends _APhysicalObject {
  #paddleWasAlreadyHit;
  #closestSideHit;

  constructor(paddle) {
    super();
    this.top = paddle.topCollisionSegment;
    this.front = paddle.frontCollisionSegment;
    this.bottom = paddle.bottomCollisionSegment;

    // Used to prevent the ball from getting stuck in the paddle
    this.#paddleWasAlreadyHit = false;

    this.#closestSideHit = null;
  }

  intersect(travel, currentClosestPhysicalObjectHit, ballRadius) {
    if (this.#paddleWasAlreadyHit) {
      return currentClosestPhysicalObjectHit;
    }
    this.#calculateClosestSideHit(travel, ballRadius);
    if (this.#closestSideHit === null) {
      return currentClosestPhysicalObjectHit;
    }
    if (currentClosestPhysicalObjectHit === null) {
      return this;
    }
    if (this.t < currentClosestPhysicalObjectHit.t) {
      return this;
    }
    return currentClosestPhysicalObjectHit;
  }

  #calculateClosestSideHit(travel, ballRadius) {
    this.#closestSideHit = null;
    this.#intersectTop(travel, ballRadius);
    this.#intersectFront(travel, ballRadius);
    this.#intersectBottom(travel, ballRadius);
  }

  #intersectTop(travel, ballRadius) {
    if (travel.vector.y > 0) {
      return;
    }
    const {intersection, t} = _PhysicalPaddle.#circleSegmentIntersection(
        travel, this.top, ballRadius,
    );
    if (intersection === null) {
      return;
    }
    if (this.t === null || this.t > t) {
      this.#closestSideHit = 'top';
      this.t = t;
      this.intersection = intersection;
    }
  }

  #intersectFront(travel, ballRadius) {
    const {intersection, t} = _PhysicalPaddle.#circleSegmentIntersection(
        travel, this.front, ballRadius,
    );
    if (intersection === null) {
      return;
    }
    if (this.t === null || this.t > t) {
      this.#closestSideHit = 'front';
      this.t = t;
      this.intersection = intersection;
    }
  }

  #intersectBottom(travel, ballRadius) {
    if (travel.vector.y < 0) {
      return;
    }
    const {intersection, t} = _PhysicalPaddle.#circleSegmentIntersection(
        travel, this.bottom, ballRadius,
    );
    if (intersection === null) {
      return;
    }
    if (this.t === null || this.t > t) {
      this.#closestSideHit = 'bottom';
      this.t = t;
      this.intersection = intersection;
    }
  }

  static #circleSegmentIntersection(travel, segment, ballRadius) {
    // This is not a perfect solution to calculate the intersection between a
    // moving circle and a segment, but it is good enough for our use case
    const radiusHelper = travel.vector.clone()
        .normalize()
        .multiplyScalar(ballRadius);
    const travelHelper = new Segment2(travel.begin,
        travel.end.clone().add(radiusHelper));
    let {intersection, t} = travelHelper.intersect(segment);
    if (intersection === null) {
      return {intersection: null, t: null};
    }
    intersection.sub(radiusHelper);
    t = (intersection.x - travel.begin.x) / travel.vector.x;
    return {intersection: intersection, t: t};
  }

  handleCollision(travel, ball, collisionHandler, _match) {
    this.#paddleWasAlreadyHit = true;
    const newTravelVector = travel.vector.multiplyScalar(1. - this.t);
    if (this.#closestSideHit === 'front') {
      ball.setMovementX(ball.movement.x * -ball.acceleration);
      newTravelVector.x *= -ball.acceleration;
    } else {
      ball.setMovementY(ball.movement.y * -ball.acceleration);
      newTravelVector.y *= -ball.acceleration;
    }
    return new Segment2(this.intersection,
        this.intersection.clone().add(newTravelVector),
        newTravelVector);
  }
}


export class CollisionHandler {
  constructor(paddle, boardSize) {
    this.TOP_WALL = new _Wall(true, boardSize);
    this.BOTTOM_WALL = new _Wall(false, boardSize);

    this.RIGHT_GOAL = new _Goal(true, boardSize);
    this.LEFT_GOAL = new _Goal(false, boardSize);

    this.physicalPaddle = new _PhysicalPaddle(paddle);
  }

  updateBallPositionAndMovement(timeDelta, match) {
    const ball = match.ball;
    let travel = new Segment2(
        ball.getPosition(),
        ball.getPosition().clone()
            .add(ball.movement.clone().multiplyScalar(timeDelta)),
    );
    while (travel !== null) {
      const closestObjectHit = this._getClosestObjectHit(
          travel, this.physicalPaddle, ball.radius,
      );
      if (closestObjectHit === null) {
        ball.setPosition(travel.end);
        return;
      }
      travel = closestObjectHit.handleCollision(
          travel, ball, this, match,
      );
    }
  }

  _getClosestObjectHit(travel, physicalPaddle, ballRadius) {
    let closestObjectHit = this.TOP_WALL.intersect(travel, null, ballRadius);
    closestObjectHit = this.BOTTOM_WALL.intersect(
        travel, closestObjectHit, ballRadius,
    );
    closestObjectHit = this.LEFT_GOAL.intersect(
        travel, closestObjectHit, ballRadius,
    );
    closestObjectHit = this.RIGHT_GOAL.intersect(
        travel, closestObjectHit, ballRadius,
    );
    return physicalPaddle.intersect(travel, closestObjectHit, ballRadius);
  }
}
