import WebGL from 'three/addons/capabilities/WebGL.js';

import {Component} from '@components';
import {userManagementClient} from '@utils/api';
import {getRouter} from '@js/Router.js';
import {Theme} from '@js/Theme.js';

import {Engine} from './Engine/Engine.js';
import {ToastNotifications} from '@components/notifications/index.js';

export class Local extends Component {
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
    this.addComponentEventListener(document, Theme.event, this.themeEvent);
    this.start_game();
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

  addEndGameCard(playerScore, opponentScore) {
    this.enableGameBlur();
    this.addGameDisplay();
    this.gameDisplay.innerHTML = `
      <div id="end-game-card" class="card">
        <div class="card-header text-center">
          <h1 class="card-title text-success">Game over</h1>
        </div>
        <div class="card-body d-flex justify-content-center align-items-center">
          <div class="d-flex flex-column justify-content-center align-items-center">
            <h5 class="m-0 text-muted ">Game result</h5>
            <h3 class="card-text">${playerScore} - ${opponentScore}</h3>
            <btn class="btn btn-primary " onclick="window.router.navigate('/')">Go home</btn>
          </div>
        </div>
      </div>
    `;
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
      this.engine.cleanUp();
    }
    try {
      this.engine.stopAnimationLoop();
    } catch (error) {}
    super.removeAllComponentEventListeners();
  }

  start_game() {
    if (!WebGL.isWebGLAvailable()) {
      console.error(WebGL.getWebGLErrorMessage());
      ToastNotifications.addErrorNotification(
          'WebGL is not available on this device',
      );
      return;
    }
    this.engine = new Engine(this);
    this.engine.startGame();
  }

  themeEvent(event) {
    if (Theme.get() === 'light') {
      this.engine.scene.setLightTheme();
    } else {
      this.engine.scene.setDarkTheme();
    }
  }
}
