import {Scene} from '@components/game/Scene/Scene.js';

import {_ThreeJS} from './_ThreeJS';
import {_KeyHookHandler} from './_KeyHookHandler';
import {LoadingScreenScene} from '../Scene/LoadingScreenScene';
import {_GameSocketIO} from './_GameSocketIO.js';

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

  get component() {
    return this.#component;
  }

  set socket(socket) {
    this.#socket = socket;
  }

  get threeJS() {
    return this.#threeJS;
  }

  updateCamera(cameraPosition, cameraLookAt) {
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
