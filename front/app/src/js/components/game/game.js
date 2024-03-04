import WebGL from 'three/addons/capabilities/WebGL.js';
import * as THREE from 'three';

import {Component} from '@components';
import {ToastNotifications} from '@components/notifications';
import {userManagementClient} from '@utils/api';
import {getRouter} from '@js/Router.js';

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
      <div id="container" class="m-2 position-relative">
        <div id="end-game-card" class="card d-none">
        </div>
      </div>
    `);
  }

  style() {
    return (`
      <style>
      @keyframes card-animation {
          from {
              opacity: 0;
              transform: translateY(-40px) translate(-50%, -50%);
          }
          to {
              opacity: 1;
              transform: translateY(0) translate(-50%, -50%);
          }
      }
      
    #end-game-card {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      z-index: 1000;
      width : 300px;
      height: 200px;
      animation: card-animation 1.0s ease-in-out;
    }
      </style>
    `);
  }

  postRender() {
    this.container = this.querySelector('#container');
    this.engine = null;
    const port = this.getAttribute('port');
    if (!port) {
      console.error('Port attribute is not set');
      return;
    }
    this.addComponentEventListener(document, Theme.event, this.themeEvent);
    this.start_game(this.getGameURL(port));
  }

  loadEndGameCard(status, playerScore, opponentScore) {
    this.endGameCard = this.querySelector('#end-game-card');
    this.endGameCard.innerHTML = `
     <div class="card-header text-center">
        ${this.renderEndGameCardTitle(status)}
     </div>
     <div class="card-body d-flex flex-column justify-content-center align-items-center">
        ${this.renderCardBody(status, playerScore, opponentScore)}
    </div>`;
    this.endGameCard.classList.remove('d-none');
    const canvas = this.querySelector('canvas');
    if (canvas) {
      canvas.style.filter = 'blur(5px)';
    }
    const spectateButton = this.querySelector('#spectate-button');
    if (spectateButton) {
      super.addComponentEventListener(
          spectateButton, 'click', this.#spectateButtonHandler,
      );
    }
  }

  #spectateButtonHandler() {
    const canvas = this.querySelector('canvas');
    if (canvas) {
      canvas.style.filter = 'blur(0px)';
    }
    this.endGameCard.classList.add('d-none');
  }

  renderCardBody(status, playerScore, opponentScore) {
    if (status === 'eliminated') {
      return (`
        <btn class="btn btn-primary " onclick="window.router.navigate('/')">Go home</btn>
        <btn class="btn btn-secondary me-3" id="spectate-button">Spectate</btn>
      `);
    } else {
      return (`
        <h5 class="m-0 text-muted ">Game result</h5>
        <h3 class="card-text">${playerScore} - ${opponentScore}</h3>
        <btn class="btn btn-primary " onclick="window.router.navigate('/')">Go home</btn>
      `);
    }
  }

  renderEndGameCardTitle(status) {
    if (status === 'win') {
      return (`
        <h1 class="card-title text-success">Win</h1>
      `);
    } else if (status === 'loose') {
      return (`
        <h1 class="card-title text-danger">Loose</h1>
      `);
    } else {
      return (`
        <h1 class="card-title text-danger">Eliminated</h1>
      `);
    }
  }

  disconnectedCallback() {
    if (this.engine) {
      this.engine.disconnectFromServer();
    }
    try {
      this.engine.stopAnimationLoop();
    } catch (error) {}
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
}
