import {Component} from '../../Component.js';
import {ErrorPage} from '../../../utils/ErrorPage.js';
import {TournamentBracket} from './TournamentBracket.js';
import {Modal} from 'bootstrap';

export class TournamentDetails extends Component {
  constructor() {
    super();
  }

  render() {
    return (`
      <div class="card mb-3 mt-3 overflow-auto">
          <div class="card-header">
              ${this.#generatePlaceholderHeader()}
          </div>
          <alert-component id="alert-modal" alert-display="false"></alert-component>
          <div class="card-body">
              ${this.#generatePlaceholderBody()}
          </div>
      
          <div class="modal fade" id="join-modal" aria-hidden="true"
               aria-labelledby="exampleModalToggleLabel" tabindex="-1">
              <div class="modal-dialog modal-dialog-centered">
                  <div class="modal-content">
                      <div class="modal-header">
                          <h1 class="modal-title fs-5" id="join-modal-title">Modal
                              1</h1>
                          <button type="button" class="btn-close"
                                  data-bs-dismiss="modal" aria-label="Close"></button>
                      </div>
                      <form>
                      <div class="modal-body d-flex flex-column justify-content-center">
                          <input type="text" class="form-control mb-2" id="nickname"
                                 placeholder="nickname" required>
                          <input type="password" class="form-control mb-2"
                                 id="password" placeholder="password" required>
                          <alert-component id="join-alert-modal"
                                           alert-display="false"></alert-component>
                      </div>
                      <div class="modal-footer">
                          <button id="join-modal-btn" type="submit" class="btn btn-primary">Join
                          </button>
                      </div>
                      </form>
                  </div>
              </div>
          </div>
      </div>
    `);
  }

  style() {
    return (`
      <style>

      </style>
    `);
  }

  postRender() {
    this.body = this.querySelector('.card-body');
    this.header = this.querySelector('.card-header');
    this.modalAlert = this.querySelector('#alert-modal');
    this.joinModalAlert = this.querySelector('#join-alert-modal');
    const joinModal = this.querySelector('#join-modal');
    this.joinModal = new Modal(joinModal);
    this.joinModalTitle = this.querySelector('#join-modal-title');
    this.joinModalBtn = this.querySelector('#join-modal-btn');
    this.joinModalNickname = this.querySelector('#nickname');
    this.modalPassword = this.querySelector('#password');
    super.addComponentEventListener(this.joinModalBtn, 'click',
        this.#modalJoinBtnHandler);
    super.addComponentEventListener(joinModal, 'hidden.bs.modal', () => {
      this.modalAlert.setAttribute('alert-display', 'false');
      this.modalAlert.setAttribute('alert-message', '');
      this.joinModalNickname.value = '';
      this.modalPassword.value = '';
    });
    this.alertModal = this.querySelector('#alert-modal');
    const navbarHeight = document.body.style.paddingTop;
    const cardHeight = this.querySelector('.card').offsetHeight;
    this.body.style.maxHeight = `calc(100vh - ${navbarHeight} - ${cardHeight}px)`;
  }

  loadNoTournament() {
    this.header.innerHTML = 'No tournament selected';
    this.body.innerHTML = `
      <div class="alert alert-warning" role="alert">
        Please select a tournament
      </div>
    `;
  }

  async loadTournamentDetails(tournamentId) {
    this.#loadPlaceholder();
    try {
      const {response, body} = await window.ApiClient.getTournament(
          tournamentId,
      );
      if (response.ok) {
        this.userId = window.ApiClient.userId;
        this.tournamentId = tournamentId;
        this.tournament = body;
        await this.#loadContent();
      } else {
        window.router.redirect('/signin/');
      }
    } catch (error) {
      ErrorPage.loadNetworkError();
    }
  }

  #loadPlaceholder() {
    this.header.innerHTML = this.#generatePlaceholderHeader();
    this.body.innerHTML = this.#generatePlaceholderBody();
  }

  #generatePlaceholderHeader() {
    return (`
      <div class="placeholder-glow">
        <span class="placeholder bg-body-secondary col-4 placeholder-lg"></span>
      </div>
    `);
  }

  #generatePlaceholderBody() {
    return (`
      <div class="d-flex justify-content-center">
        <div class="spinner-border" role="status">
          <span class="sr-only"></span>
        </div>
      </div>
    `);
  }

  async #loadContent() {
    this.header.innerHTML = this.#generateHeader(this.tournament, this.userId);
    if (this.tournament['status'] === 'Created') {
      this.body.innerHTML = this.#generatePlayersList(
          this.tournament['players'], this.userId,
      );
    } else {
      await this.#loadBracket();
    }
    this.joinBtn = this.querySelector('#join-btn');
    this.startBtn = this.querySelector('#start-btn');
    this.deleteBtn = this.querySelector('#delete-btn');
    if (this.joinBtn) {
      super.addComponentEventListener(
          this.joinBtn, 'click', this.#joinBtnHandler,
      );
    }
    if (this.deleteBtn) {
      super.addComponentEventListener(
          this.deleteBtn, 'click', this.#deleteBtnHandler,
      );
    }
    if (this.startBtn) {
      super.addComponentEventListener(
          this.startBtn, 'click', this.#startBtnHandler,
      );
    }
  }

  #generateHeader(tournament, userId) {
    if (tournament['admin'] === localStorage.getItem('username')) {
      return (`
        ${tournament['name']} 
        ${this.#canJoin(tournament, userId) ? `<button id="join-btn" type="button" class="btn btn-success btn-sm">Join</button>` : ''}
        ${tournament['status'] === 'Created' ? `<button id="start-btn" type="button" class="btn btn-primary btn-sm">Start</button>` : ''}
        ${tournament['status'] === 'Created' ? `<button id="delete-btn" type="button" class="btn btn-danger btn-sm">Delete</button>` : ''}
      `);
    }
    return (`
        ${tournament['name']} 
        ${this.#canJoin(tournament, userId) ? `<button id="join-btn" type="button" class="btn btn-success btn-sm">Join</button>` : ''}
    `);
  }

  #canJoin(tournament, userId) {
    if (tournament['status'] !== 'Created') {
      return false;
    }
    for (const player of tournament['players']) {
      if (player['user-id'] === userId) {
        return false;
      }
    }
    return true;
  }

  #generatePlayersList(players) {
    if (players.length === 0) {
      return (`
        <div class="alert alert-warning" role="alert">
          No players registered yet
        </div>
      `);
    }
    return (`
      <ul class="list-group list-group-flush">
        ${this.#generatePlayerListItems(players)}
      </ul>
    `);
  }

  #generatePlayerListItems(players) {
    return players.map((player) => {
      return (`
        <li class="list-group-item">${player['nickname']}</li>
      `);
    }).join('');
  }

  async #loadBracket() {
    try {
      const {response, body} = await window.ApiClient.getTournamentMatches(
          this.tournamentId,
      );
      if (response.ok) {
        const bracket = new TournamentBracket(
            body.matches, this.tournament['nb-players'],
        );
        this.body.innerHTML = '';
        this.body.appendChild(bracket);
      } else {
        window.router.redirect('/signin/');
      }
    } catch (error) {
      ErrorPage.loadNetworkError();
    }
  }

  async #startBtnHandler() {
    if (await this.#generateMatches()) {
      await this.#startTournament();
    }
  }

  async #generateMatches() {
    try {
      const {response, body} = await window.ApiClient.generateMatches(
          this.tournamentId,
      );
      if (response.ok) {
        await this.loadTournamentDetails(this.tournamentId);
        return true;
      } else {
        this.alertModal.setAttribute('alert-message', body['errors'][0]);
        this.alertModal.setAttribute('alert-display', 'true');
        return false;
      }
    } catch (error) {
      ErrorPage.loadNetworkError();
    }
  }

  async #startTournament() {
    try {
      const {response, body} = await window.ApiClient.startTournament(
          this.tournamentId,
      );
      if (response.ok) {
        await this.loadTournamentDetails(this.tournamentId);
      } else {
        this.alertModal.setAttribute('alert-message', body['errors'][0]);
        this.alertModal.setAttribute('alert-display', 'true');
      }
    } catch (error) {
      ErrorPage.loadNetworkError();
    }
  }

  async #deleteBtnHandler() {
    try {
      const {response, body} = await window.ApiClient.deleteTournament(
          this.tournamentId,
      );
      if (response.ok) {
        window.router.navigate('/tournaments/');
      } else {
        this.alertModal.setAttribute('alert-message', body['errors'][0]);
        this.alertModal.setAttribute('alert-display', 'true');
      }
    } catch (error) {
      ErrorPage.loadNetworkError();
    }
  }

  async #joinBtnHandler() {
    this.joinModalTitle.textContent = this.tournament['name'];
    if (this.tournament['is-private']) {
      this.querySelector('#password').classList.remove('d-none');
    } else {
      this.querySelector('#password').classList.add('d-none');
    }
    this.joinModal.show();
  }

  async #modalJoinBtnHandler(event) {
    event.preventDefault();
    const nickname = this.joinModalNickname.value;
    const password = this.modalPassword.value;
    try {
      const {response, body} = await window.ApiClient.joinTournament(
          this.tournamentId, nickname, password,
      );
      if (response.ok) {
        this.joinModal.hide();
        await this.loadTournamentDetails(this.tournamentId);
      } else {
        this.joinModalAlert.setAttribute('alert-message', body['errors'][0]);
        this.joinModalAlert.setAttribute('alert-display', 'true');
      }
    } catch (error) {
      ErrorPage.loadNetworkError();
    }
  }
}

