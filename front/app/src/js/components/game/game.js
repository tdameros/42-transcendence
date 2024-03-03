import WebGL from 'three/addons/capabilities/WebGL.js';
import * as THREE from 'three';

import {Component} from '@components';
import {ToastNotifications} from '@components/notifications';
import {userManagementClient} from '@utils/api';

import {Engine} from './Engine/Engine.js';
import {Theme} from '@js/Theme.js';
import TWEEN from '@tweenjs/tween.js';

export class Game extends Component {
  static gameURL = `https://${window.location.hostname}`;

  constructor() {
    super();
  }
  render() {
    if (!userManagementClient.isAuth()) {
      getRouter().redirect('/signin/');
      return false;
    }
    return (`
      <navbar-component></navbar-component>
      <div id="container"></div>
    `);
  }

  postRender() {
    this.engine = null;
    const port = this.getAttribute('port');
    if (!port) {
      console.error('Port attribute is not set');
      return;
    }
    this.start_game(this.getGameURL(port));
  }

  disconnectedCallback() {
    if (this.engine) {
      this.engine.disconnectFromServer();
    }
    super.removeAllComponentEventListeners();
  }

  start_game(URI) {
    if (!WebGL.isWebGLAvailable()) {
      console.error(WebGL.getWebGLErrorMessage());
      ToastNotifications.addErrorNotification(
          'WebGL is not available on this device',
      );
      return;
    }
    this.engine = new Engine(this);

    this.displayScene(this.engine);
    this.engine.connectToServer(URI)
        .catch((error) => {
          console.error('Error connecting to server:', error);
        });
  }

  displayScene(engine) {
    const clock = new THREE.Clock();

    engine.setAnimationLoop(() => {
      const delta = clock.getDelta();
      engine.scene.updateFrame(delta);

      TWEEN.update();
      engine.threeJS.updateControls();
      engine.renderFrame();
    });
  }

  getGameURL(port) {
    return `${Game.gameURL}:${port}/`;
  }

  themeEvent(event) {
    if (Theme.get() === 'light') {
      this.engine.scene.setLightTheme();
    } else {
      this.engine.scene.setDarkTheme();
    }
  }

  style() {
    return (`
      <style>

      </style>
    `);
  }
}
