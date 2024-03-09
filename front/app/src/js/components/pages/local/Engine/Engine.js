import {Scene} from '@components/pages/local/Scene/Scene.js';

import {_ThreeJS} from './_ThreeJS';
import {_KeyHookHandler} from './_KeyHookHandler';
import * as THREE from 'three';
import TWEEN from '@tweenjs/tween.js';

export class Engine {
  #threeJS;
  #keyHookHandler;
  #scene;
  #component;

  constructor(component) {
    this.#component = component;
    this.#threeJS = new _ThreeJS(this);
    this.#keyHookHandler = new _KeyHookHandler(this);
    this.#scene = new Scene();
  }

  async startGame() {
    await this.#scene.init(this);
    this.scene.updateCamera();
    this.startListeningForKeyHooks();
    this.displayGameScene();
    this.component.startCountdown(this.#scene.match.ballStartTime / 1000.);
  }

  cleanUp() {
    this.clearScene(this.#scene.threeJSScene);
    this.#threeJS.clearRenderer();
  }

  renderFrame() {
    this.#threeJS.renderFrame(this.#scene.threeJSScene);
  }

  get scene() {
    return this.#scene;
  }

  set scene(newScene) {
    this.clearScene(this.#scene.threeJSScene);
    this.#scene = newScene;
  }

  clearScene(scene) {
    while (scene.children.length > 0) {
      this.clearScene(scene.children[0]);
      scene.remove(scene.children[0]);
    }
    if (scene.geometry) {
      scene.geometry.dispose();
    }
    if (scene.material) {
      scene.material.dispose();
    }
  }

  setAnimationLoop(loopFunction) {
    this.#threeJS.setAnimationLoop(loopFunction);
  }

  stopAnimationLoop() {
    this.#threeJS.stopAnimationLoop();
  }

  displayGameScene() {
    const clock = new THREE.Clock();

    this.setAnimationLoop(() => {
      const currentTime = Number(Date.now());
      const delta = clock.getDelta();
      this.scene.updateFrame(currentTime, delta);

      TWEEN.update();
      this.threeJS.updateControls();
      this.renderFrame();
    });
  }

  get component() {
    return this.#component;
  }

  get threeJS() {
    return this.#threeJS;
  }

  updateCamera(cameraPosition, cameraLookAt) {
    this.#threeJS.controls.target.set(
        cameraLookAt.x,
        cameraLookAt.y,
        cameraLookAt.z,
    );
    this.#threeJS.setCameraPosition(cameraPosition);
    this.#threeJS.setCameraLookAt(cameraLookAt);
  }

  resizeHandler() {
    if (this.#scene instanceof Scene) {
      this.#scene.updateCamera();
    }
  }

  startListeningForKeyHooks() {
    this.#keyHookHandler.startListeningForKeyHooks();
  }
}
