import {io} from 'socket.io-client';

import {Component} from '@components';
import {userManagementClient} from '@utils/api';
import {getRouter} from '@js/Router';
import {ErrorPage} from '@utils/ErrorPage.js';
import {ToastNotifications} from '@components/notifications';

export class MultiplayerButton extends Component {
  static multiplayerURL = `https://${window.location.hostname}:6004/`;

  constructor() {
    super();
    this.queueTime = 0;
  }

  render() {
    return (`
      <div class="d-flex flex-row align-items-center">
        <button type="button" id="matchmaking" class="btn btn-primary btn-lg">Find match</button>
        <div id="cancel"></div>
        <div id="timer" class="ms-2 text-muted"></div>
      </div>
    `);
  }

  postRender() {
    this.matchmakingButton = document.querySelector('#matchmaking');
    super.addComponentEventListener(
        this.matchmakingButton, 'click', this.#matchmakingHandler,
    );
    this.timer = document.querySelector('#timer');
    this.cancel = document.querySelector('#cancel');
  }

  disconnectedCallback() {
    if (this.sio) {
      try {
        this.sio.disconnect();
      } catch (error) {
        ;
      }
    }
    super.removeAllComponentEventListeners();
  }

  async #matchmakingHandler() {
    this.#startMatchmakingLoader();
    await this.#socketHandler();
  }

  async #socketHandler() {
    let accessToken;
    try {
      accessToken = await userManagementClient.getValidAccessToken();
      if (accessToken === null) {
        getRouter().redirect('/signin/');
        return;
      }
    } catch (error) {
      ErrorPage.loadNetworkError();
      return;
    }
    this.sio = io(MultiplayerButton.multiplayerURL, {
      auth: {
        token: accessToken,
      },
    });

    this.sio.on('connect', () => {
      this.#startQueue();
    });

    this.sio.on('connect_error', (error) => {
      ToastNotifications.addErrorNotification(
          'Server connection error: ' + error.message,
      );
      this.#cancelQueue();
    });

    this.sio.on('match', (data) => {
      const json = JSON.parse(data);
      const port = json['port'];
      getRouter().navigate(`/game/${port}/`);
    });

    this.sio.on('disconnect', () => {
      this.#cancelQueue();
    });

    this.sio.on('error', (message) => {
      console.error(message);
      ToastNotifications.addErrorNotification(message.error);
      this.#cancelQueue();
    });
  }

  #startQueue() {
    this.#startQueueTimer();
    this.#addCancelButton();
    this.#hideMatchmakingButton();
  }

  #hideMatchmakingButton() {
    this.matchmakingButton.style.display = 'none';
    this.#stopMatchmakingLoader();
  }

  #addCancelButton() {
    this.cancel.innerHTML = `
      <button type="button" id="cancel-button" class="btn btn-danger btn-lg">Cancel</button>
    `;
    const cancelButton = document.querySelector('#cancel-button');
    super.addComponentEventListener(
        cancelButton, 'click', this.#cancelQueue,
    );
  }

  #cancelQueue() {
    this.#stopMatchmakingLoader();
    this.#stopQueueTimer();
    this.cancel.innerHTML = '';
    this.sio.disconnect();
  }

  #startQueueTimer() {
    if (this.queueTime === 0) {
      this.timer.innerHTML = `<h2 class="m-0">${this.#getDisplayTimer(this.queueTime)}</h2>`;
    }
    this.queueTimerInterval = setInterval(() => {
      this.queueTime += 1;
      this.timer.innerHTML = `<h2 class="m-0">${this.#getDisplayTimer(this.queueTime)}</h2>`;
    }, 1000);
  }

  #stopQueueTimer() {
    clearInterval(this.queueTimerInterval);
    this.queueTime = 0;
    this.timer.innerHTML = '';
    this.matchmakingButton.style.display = 'block';
  }

  #getDisplayTimer(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    const minutesStr = minutes < 10 ? '0' + minutes : minutes;
    const secondsStr = remainingSeconds < 10 ?
        '0' + remainingSeconds : remainingSeconds;
    return minutesStr + ':' + secondsStr;
  }

  #startMatchmakingLoader() {
    this.matchmakingButton.disabled = true;
    this.matchmakingButton.innerHTML = `
      <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
      Find match
    `;
  }

  #stopMatchmakingLoader() {
    this.matchmakingButton.disabled = false;
    this.matchmakingButton.innerHTML = 'Find match';
  }

  style() {
    return (`
      <style>

      </style>
    `);
  }
}
