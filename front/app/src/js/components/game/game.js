import WebGL from 'three/addons/capabilities/WebGL.js';
import * as THREE from 'three';

import {Component} from '@components';
import {ToastNotifications} from '@components/notifications';

import {Engine} from './Engine/Engine.js';

export class Game extends Component {
  static gameURL = `https://${window.location.hostname}`;

  constructor() {
    super();
  }
  render() {
    return (`
      <navbar-component></navbar-component>
      <div id="container"></div>
    `);
  }

  postRender() {
    const port = this.getAttribute('port');
    if (!port) {
      console.error('Port attribute is not set');
      return;
    }
    this.start_game(this.getGameURL(port));
  }

  start_game(URI) {
    if (!WebGL.isWebGLAvailable()) {
      console.error(WebGL.getWebGLErrorMessage());
      ToastNotifications.addErrorNotification(
          'WebGL is not available on this device',
      );
      return;
    }
    const engine = new Engine(this);

    this.displayScene(engine);
    engine.connectToServer(URI)
        .catch((error) => {
          console.error('Error connecting to server:', error);
        });
  }

  displayScene(engine) {
    const clock = new THREE.Clock();

    engine.setAnimationLoop(() => {
      const delta = clock.getDelta();
      engine.scene.updateFrame(delta);

      engine.renderFrame();
    });
  }

  getGameURL(port) {
    return `${Game.gameURL}:${port}/`;
  }

  style() {
    return (`
      <style>

      </style>
    `);
  }
}
