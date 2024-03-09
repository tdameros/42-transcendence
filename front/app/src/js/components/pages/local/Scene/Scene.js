import * as THREE from 'three';
import TWEEN from '@tweenjs/tween.js';


import {Match} from './Match';
import {PaddleBoundingBox} from './PaddleBoundingBox.js';
import {SceneSky} from './SceneSky.js';

export class Scene {
  #engine;
  #threeJSScene = new THREE.Scene();
  #match = new Match();
  #paddleBoundingBox;
  #matchHalfWidth = 20.;
  #matchHalfHeight = 13.75;
  #cameraPadding = 10.;
  #sky;
  #boardSize;
  #animationHeight = 20;

  constructor() {}

  async init(engine) {
    this.#engine = engine;

    await this.#match.init(engine);
    this.#threeJSScene.add(this.#match.threeJSGroup);

    this.#sky = new SceneSky();
    this.#threeJSScene.add(this.#sky.sky);
    const light = new THREE.AmbientLight(0xffffff, 0.2);
    this.#threeJSScene.add(light);

    const player = this.#match.players[0];
    this.#boardSize = player.board.size;
    this.#paddleBoundingBox = new PaddleBoundingBox(
        this.#boardSize.y, player.paddle.size.y,
    );

    this.#engine.threeJS.controls.target.set(30, 25, 0);
  }

  setLightTheme() {
    this.#sky.setLightTheme();
  }

  setDarkTheme() {
    this.#sky.setDarkTheme();
  }

  updateFrame(currentTime, timeDelta) {
    this.#match.updateFrame(
        timeDelta,
        currentTime,
        this.#paddleBoundingBox,
        this.#boardSize,
    );
  }

  setPlayerPaddleDirection(direction, index) {
    this.#match.players[index].paddle.setDirection(direction);
  }

  updateCamera(animation = false) {
    const matchPosition = this.#match.threeJSGroup.position;
    const xHeight = (this.#matchHalfWidth + this.#cameraPadding * .5) /
      Math.tan(this.#engine.threeJS.getCameraHorizontalFOVRadian() * .5);
    const yHeight = (this.#matchHalfHeight + this.#cameraPadding * .5) /
      Math.tan(this.#engine.threeJS.getCameraVerticalFOVRadian() * .5);
    const cameraHeight = Math.max(xHeight, yHeight) -
        animation * this.#animationHeight;

    const cameraPosition = new THREE.Vector3(
        matchPosition.x,
        matchPosition.y,
        cameraHeight,
    );
    const cameraLookAt = matchPosition.clone();
    this.#engine.updateCamera(cameraPosition, cameraLookAt);

    if (animation) {
      const newCameraPosition = new THREE.Vector3(
          matchPosition.x,
          matchPosition.y,
          cameraHeight + this.#animationHeight,
      );

      new TWEEN.Tween(cameraPosition)
          .to(newCameraPosition, 3000)
          .easing(TWEEN.Easing.Quadratic.InOut)
          .onUpdate(() => {
            this.#engine.updateCamera(cameraPosition, cameraLookAt);
          })
          .start();
    }
  }

  get match() {
    return this.#match;
  }

  get threeJSScene() {
    return this.#threeJSScene;
  }

  get boardSize() {
    return this.#boardSize;
  }
}
