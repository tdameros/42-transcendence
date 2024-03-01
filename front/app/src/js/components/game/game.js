import {Component} from '@components';
import WebGL from 'three/addons/capabilities/WebGL.js';

import {Engine} from './Engine/Engine.js';
import * as THREE from 'three';
import {Theme} from '@js/Theme.js';
import TWEEN from '@tweenjs/tween.js';
export class Game extends Component {
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
    this.start_game(`https://localhost:${this.getAttribute('port')}`);
    super.addComponentEventListener(document, Theme.event, this.themeEvent);
  }

  start_game(URI) {
    if (!WebGL.isWebGLAvailable()) {
      document.querySelector('#container')
          .appendChild(WebGL.getWebGLErrorMessage());
      return;
    }

    this.engine = new Engine();

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
