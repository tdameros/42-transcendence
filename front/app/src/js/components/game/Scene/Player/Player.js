import * as THREE from 'three';
import {_Board} from './_Board';
import {Paddle} from './Paddle';
import {jsonToVector3} from '@components/game/jsonToVector3.js';
import {ServerTime} from '@components/game/ServerTime.js';

export class Player {
  #threeJSGroup = new THREE.Group();
  #board;
  #paddle;
  #originalPosition;
  #destination;
  #isAnimating;
  #animationStartTime;
  #animationEndTime;
  #isChangingSide;

  #isCurrentPlayer = false;

  constructor() {}

  async init(playerJson, index, pointsToWinMatch) {
    this.#originalPosition = jsonToVector3(playerJson['position']);
    this.#threeJSGroup.position.set(this.#originalPosition.x,
        this.#originalPosition.y,
        this.#originalPosition.z);
    this.#destination = jsonToVector3(playerJson['destination']);
    this.#isAnimating = playerJson['is_animating'];
    this.#animationStartTime = ServerTime.fixServerTime(
        playerJson['animation_start_time']);
    this.#animationEndTime = ServerTime.fixServerTime(
        playerJson['animation_end_time']);
    this.#isChangingSide = playerJson['is_changing_side'];

    this.#paddle = new Paddle(playerJson['paddle'],
        this.#threeJSGroup.position);

    this.#threeJSGroup.add(this.#paddle.threeJSGroup);
    this.#board = new _Board();
    if (this.#isAnimating && this.#isChangingSide) {
      await this.#board.init(playerJson['board'], 1 - index, pointsToWinMatch);
      this.#board.startAnimation();
    } else {
      await this.#board.init(playerJson['board'], index, pointsToWinMatch);
    }
    if (this.#isAnimating) {
      this.#paddle.startAnimation();
    }
    this.#threeJSGroup.add(this.#board.threeJSBoard);
  }

  async initLooser(playerJson, pointsToWinMatch) {
    const position = playerJson['position'];
    this.#threeJSGroup.position.set(position['x'],
        position['y'],
        position['z']);

    this.#paddle = new Paddle(playerJson['paddle'],
        this.#threeJSGroup.position);

    this.#threeJSGroup.add(this.#paddle.threeJSGroup);
    this.#board = new _Board();
    await this.#board.init(
        playerJson['board'], playerJson['index_when_lost_match'],
        pointsToWinMatch,
    );
    this.#threeJSGroup.add(this.#board.threeJSBoard);
  }

  updateFrame(timeDelta, currentTime, paddleBoundingBox) {
    if (this.#isAnimating) {
      this.#animate(currentTime);
      if (this.#isAnimating) {
        return;
      }
    }

    this.#paddle.updateFrame(timeDelta, paddleBoundingBox);
    this.#board.updateFrame();
  }

  #animate(currentTime) {
    const t = Math.min(
        (currentTime - this.#animationStartTime) /
            (this.#animationEndTime - this.#animationStartTime),
        1.,
    );

    if (t >= 1.) {
      this.#isAnimating = false;
    }

    this.#animateMovement(t);
    this.#paddle.animate(t, this.#isChangingSide);
    if (this.#isChangingSide) {
      this.#animateRotation(t);
      this.#board.animate(t);
    }
  }

  #animateMovement(t) {
    if (t >= 1.) {
      this.#threeJSGroup.position.set(
          this.#destination.x, this.#destination.y, this.#destination.z);
      return;
    }
    const upMovement = this.#destination.y - this.#originalPosition.y;
    const sideMovement = this.#destination.x - this.#originalPosition.x;
    const portionOfUpMovement = upMovement /
        (upMovement + Math.abs(sideMovement));
    const portionOfSideMovement = 1. - portionOfUpMovement;
    if (t < portionOfUpMovement) {
      this.#threeJSGroup.position.x = this.#originalPosition.x;
      this.#threeJSGroup.position.y = this.#originalPosition.y +
          upMovement * (t / portionOfUpMovement);
    } else {
      this.#threeJSGroup.position.y = this.#destination.y;
      this.#threeJSGroup.position.x = this.#originalPosition.x +
          sideMovement * ((t - portionOfUpMovement) / portionOfSideMovement);
    }
  }

  #animateRotation(t) {
    if (t >= 1.) {
      this.#threeJSGroup.rotation.y = 0;
      this.#threeJSGroup.rotation.x = 0;
      return;
    }
    this.#threeJSGroup.rotation.y = Math.PI * t;
    this.#threeJSGroup.rotation.x = Math.PI * t;
  }

  startAnimation(isChangingSide,
      animationStartTime,
      animationEndTime,
      finishedMatch,
      newMatch) {
    this.#isChangingSide = isChangingSide;
    this.#destination = this.#threeJSGroup.position.clone();
    if (this.#isChangingSide) {
      this.#destination.x *= -1.;
    }
    this.#originalPosition = this.#threeJSGroup.position.clone()
        .add(finishedMatch.getPosition()) // make position global
        .sub(newMatch.getPosition()); // make position local to new match
    this.#isAnimating = true;
    this.#animationStartTime = animationStartTime;
    this.#animationEndTime = animationEndTime;

    this.#board.startAnimation();
    this.#paddle.startAnimation();
  }

  addPoint() {
    this.#board.addPoint();
  }

  resetPoints() {
    this.#board.resetPoints();
  }

  get score() {
    return this.#board.score;
  }

  get threeJSGroup() {
    return this.#threeJSGroup;
  }

  get paddle() {
    return this.#paddle;
  }

  set destination(destination) {
    this.#destination = destination;
  }

  set isCurrentPlayer(isCurrentPlayer) {
    this.#isCurrentPlayer = isCurrentPlayer;
  }

  get isCurrentPlayer() {
    return this.#isCurrentPlayer;
  }

  get isAnimating() {
    return this.#isAnimating;
  }

  getPosition() {
    return this.#threeJSGroup.position;
  }
}
