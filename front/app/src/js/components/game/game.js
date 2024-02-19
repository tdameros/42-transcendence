import {Component} from '@components';
import WebGL from 'three/addons/capabilities/WebGL.js';

import {Engine} from './Engine/Engine.js';
import * as THREE from 'three';

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
  }

  start_game(URI) {
    if (!WebGL.isWebGLAvailable()) {
      document.querySelector('#container')
          .appendChild(WebGL.getWebGLErrorMessage());
      return;
    }

    const engine = new Engine();

    this.displayScene(engine);
    engine.connectToServer(URI);
  }

  displayScene(engine) {
    const clock = new THREE.Clock();

    engine.setAnimationLoop(() => {
      const delta = clock.getDelta();
      engine.scene.updateFrame(delta);

      engine.renderFrame();
    });
  }

  style() {
    return (`
      <style>

      </style>
    `);
  }
}
