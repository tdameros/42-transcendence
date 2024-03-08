import {Scene} from '@components/game/Scene/Scene.js';

import {_ThreeJS} from './_ThreeJS';
import {_KeyHookHandler} from './_KeyHookHandler';
import {LoadingScreenScene} from '../Scene/LoadingScreenScene';
import {_GameSocketIO} from './_GameSocketIO.js';
import * as THREE from 'three';
import TWEEN from '@tweenjs/tween.js';

export class Engine {
  #threeJS;
  #keyHookHandler;
  #socket;
  #scene;
  #component;

  constructor(component) {
    this.#component = component;
    this.#threeJS = new _ThreeJS(this);
    this.#keyHookHandler = new _KeyHookHandler(this);
    this.#scene = new LoadingScreenScene();
    this.#socket = null;
  }

  async connectToServer(URI) {
    this.#socket = new _GameSocketIO(this);
    await this.#socket.init(URI);
  }

  disconnectFromServer() {
    try {
      this.#socket.disconnect();
      return true;
    } catch (error) {
      return false;
    }
  }

  renderFrame() {
    this.#threeJS.renderFrame(this.#scene.threeJSScene);
  }

  emit(event, data) {
    if (this.#socket === null) {
      console.log('Error: Socket is null: Failed to send event(', event, '): ',
          data);
      return;
    }

    this.#socket.emit(event, data);
  }

  get scene() {
    return this.#scene;
  }

  set scene(newScene) {
    this.#scene = newScene;
  }

  setAnimationLoop(loopFunction) {
    this.#threeJS.setAnimationLoop(loopFunction);
  }

  stopAnimationLoop() {
    this.#threeJS.stopAnimationLoop();
  }

  displayLoadingScene() {
    const clock = new THREE.Clock();

    this.setAnimationLoop(() => {
      const delta = clock.getDelta();
      this.scene.updateFrame(delta);

      TWEEN.update();
      this.threeJS.updateControls();
      this.renderFrame();
    });
  }

  displayGameScene() {
    const clock = new THREE.Clock();
    let currentTime = Number(Date.now());
    let requestTimeSyncTime = currentTime;

    this.setAnimationLoop(() => {
      if (currentTime >= requestTimeSyncTime) {
        this.socket.requestTimeSync(currentTime);
        // Wait 2 sec before next time sync
        requestTimeSyncTime = currentTime + 2000;
      }
      const delta = clock.getDelta();
      this.scene.updateFrame(currentTime, delta);

      TWEEN.update();
      this.threeJS.updateControls();
      this.renderFrame();

      currentTime = Number(Date.now());
    });
  }

  get component() {
    return this.#component;
  }

  set socket(socket) {
    this.#socket = socket;
  }

  get socket() {
    return this.#socket;
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
