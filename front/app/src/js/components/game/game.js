import WebGL from 'three/addons/capabilities/WebGL.js';

import {Component} from '@components';
import {ToastNotifications} from '@components/notifications';
import {userManagementClient} from '@utils/api';
import {getRouter} from '@js/Router.js';
import {Theme} from '@js/Theme.js';

import {Engine} from './Engine/Engine.js';

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
      width : 300px;
      height: 200px;
    }
    
    #game-display {
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

  addWaitingForOpponent() {
    this.addGameDisplay();
    this.gameDisplay.innerHTML = `
      <h2 class="text-center">Waiting for opponent</h2>
      <div class="spinner-border text-primary" role="status">
      <span class="visually-hidden">Loading...</span>
    `;
    this.enableGameBlur();
  }

  removeWaitingForOpponent() {
    this.removeGameDisplay();
    this.disableGameBlur();
  }

  startCountdown(startDateInSeconds) {
    const currentDateInSeconds = Date.now() / 1000;
    const secondsLeft = Math.round(
        (startDateInSeconds - currentDateInSeconds),
    );
    this.displayCountdown(secondsLeft);
  }

  displayCountdown(secondsLeft) {
    this.enableGameBlur();
    this.addGameDisplay();
    this.gameDisplay.innerHTML = `
        <h1 class="text-center fs-1 m-0">${secondsLeft}</h1>
    `;
    const countDownInterval = setInterval(() => {
      secondsLeft -= 1;
      if (secondsLeft <= 0) {
        clearInterval(countDownInterval);
        this.removeGameDisplay();
        this.disableGameBlur();
        return;
      }
      this.gameDisplay.innerHTML = `
        <h1 class="text-center fs-1 m-0">${secondsLeft}</h1>
      `;
    }, 1000);
  }

  addEndGameCard(status, playerScore, opponentScore) {
    this.enableGameBlur();
    this.addGameDisplay();
    this.gameDisplay.innerHTML = `
      <div id="end-game-card" class="card">
        <div class="card-header text-center">
            ${this.renderEndGameCardTitle(status)}
         </div>
         <div class="card-body d-flex justify-content-center align-items-center">
            ${this.renderCardBody(status, playerScore, opponentScore)}
        </div>
      </div>
    `;
    const spectateButton = this.querySelector('#spectate-button');
    if (spectateButton) {
      super.addComponentEventListener(
          spectateButton, 'click', this.#spectateButtonHandler,
      );
    }
  }

  #spectateButtonHandler() {
    this.disableGameBlur();
    this.removeGameDisplay();
  }

  renderCardBody(status, playerScore, opponentScore) {
    if (status === 'eliminated') {
      return (`
        <btn class="btn btn-primary ms-2 me-2" onclick="window.router.navigate('/')">Go home</btn>
        <btn class="btn btn-secondary ms-2 me-2" id="spectate-button">Spectate</btn>
      `);
    } else {
      return (`
        <div class="d-flex flex-column justify-content-center align-items-center">
          <h5 class="m-0 text-muted ">Game result</h5>
          <h3 class="card-text">${playerScore} - ${opponentScore}</h3>
          <btn class="btn btn-primary " onclick="window.router.navigate('/')">Go home</btn>
        </div>
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

  enableGameBlur() {
    const canvas = this.querySelector('canvas');
    if (canvas) {
      canvas.style.filter = 'blur(5px)';
    }
  }

  disableGameBlur() {
    const canvas = this.querySelector('canvas');
    if (canvas) {
      canvas.style.filter = 'blur(0px)';
    }
  }

  addGameDisplay() {
    if (this.gameDisplay) {
      this.removeGameDisplay();
    }
    this.gameDisplay = document.createElement('div');
    this.gameDisplay.id = 'game-display';
    this.gameDisplay.classList.add(
        'd-flex', 'flex-column', 'justify-content-center', 'align-items-center',
    );
    this.container.appendChild(this.gameDisplay);
  }

  removeGameDisplay() {
    if (this.gameDisplay) {
      this.gameDisplay.remove();
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

    this.engine.displayLoadingScene();
    this.engine.connectToServer(URI)
        .catch((error) => {
          console.error('Error connecting to server:', error);
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
