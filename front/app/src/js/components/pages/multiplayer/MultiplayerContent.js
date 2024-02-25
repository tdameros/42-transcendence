import {Component} from '@components';
import {io} from 'socket.io-client';
import {userManagementClient} from '@utils/api';
import {getRouter} from '@js/Router';

export class MultiplayerContent extends Component {
  constructor() {
    super();
  }
  render() {
    return (`
      <div class="d-flex flex-row align-items-center">
        <button type="button" id="matchmaking" class="btn btn-primary btn-lg">Find match</button>
        <div id="cancel"></div>
        <div id="timer" class="ms-2"></div>
      </div>
    `);
  }

  postRender() {
    this.matchmakingButton = document.querySelector('#matchmaking');
    super.addComponentEventListener(
        this.matchmakingButton, 'click', this.#socketHandler,
    );
    this.timer = document.querySelector('#timer');
    this.cancel = document.querySelector('#cancel');
  }

  async #socketHandler() {
    const accessToken = await userManagementClient.getValidAccessToken();
    console.log(accessToken);
    this.sio = io('https://localhost:6004', {
      auth: {
        token: accessToken,
      },
    });

    this.sio.on('connect', () => {
      console.log('connected');
      this.#startQueue();
    });

    this.sio.on('connect_error', (err) => {
      console.log(err.message);
    });

    this.sio.on('match', (data) => {
      const json = JSON.parse(data);
      console.log(json);
      const port = json['port'];
      getRouter().navigate(`/game/${port}/`);
    });

    this.sio.on('disconnect', () => {
      console.log('disconnected');
      this.#stopQueueTimer();
    });

    this.sio.on('error', (err) => {
      console.log(err);
    });
  }

  #startQueue() {
    this.#startQueueTimer();
    this.#addCancelButton();
    this.#hideMatchmakingButton();
  }

  #hideMatchmakingButton() {
    this.matchmakingButton.style.display = 'none';
  }

  #addCancelButton() {
    this.cancel.innerHTML = `
      <button type="button" id="cancel-button" class="btn btn-danger btn-lg">Cancel</button>
    `;
    const cancelButton = document.querySelector('#cancel-button');

    this.addComponentEventListener(cancelButton, 'click', () => {
      this.#stopQueueTimer();
      this.cancel.innerHTML = '';
      this.sio.disconnect();
    });
  }

  #startQueueTimer() {
    let time = 0;
    this.queueTimerInterval = setInterval(() => {
      time += 1;
      this.timer.innerHTML = `<h2 class="m-0">${this.#getDisplayTimer(time)}</h2>`;
    }, 1000);
  }

  #stopQueueTimer() {
    clearInterval(this.queueTimerInterval);
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


  style() {
    return (`
      <style>

      </style>
    `);
  }
}
