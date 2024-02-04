import {Component} from '../Component.js';
import {ErrorPage} from '../../utils/ErrorPage.js';

export class TournamentsCreate extends Component {
  constructor() {
    super();
    this.passwordHiden = true;
  }

  render() {
    if (!window.ApiClient.isAuth()) {
      window.router.redirect('/signin/');
      return false;
    }
    return (`
      <navbar-component disable-padding-top="true"></navbar-component>
      <div id="tournament"
           class="d-flex justify-content-center align-items-center rounded-3">
          <div class="tournament-card card m-3">
              <div class="card-body m-2">
                  <h2 class="card-title text-center m-5 dynamic-hover">New tournament</h2>
                  <form id="tournament-form">
                      <div class="form-group mb-4">
                          <div class="input-group has-validation">
                              <input type="text" class="form-control" id="name"
                                     placeholder="Name">
                              <div id="name-feedback" class="invalid-feedback">
                                  Invalid username.
                              </div>
                          </div>
                      </div>
                      <div class="form-group mb-4">
                        <label for="max-players" class="form-label">Max players: 8</label>
                        <input type="range" value=8 class="form-range" id="max-players" min="3" max="16">
                        </div>
                      <div class="form-group mb-4">
                      <div class="form-check form-switch">
                        <input class="form-check-input" type="checkbox" id="private-switch">
                        <label class="form-check-label" for="private-switch">Private</label>
                       </div>
                      <div id="password-box" class="form-group mt-3 d-none">
                          <div class="input-group has-validation">
                              <input type="password" class="form-control"
                                     id="password"
                                     placeholder="Password">
                              <span id="password-eye"
                                    class="input-group-text dynamic-hover">
                                  <i class="bi bi-eye-fill"></i>
                              </span>
                              <div id="password-feedback" class="invalid-feedback">
                                  Invalid password.
                              </div>
                          </div>
                      </div>
                      </div>
                  <alert-component id="alert-form" alert-display="false">
                  </alert-component>
                  <div class="row d-flex justify-content-center">
                      <button id="createBtn" type="submit" class="btn btn-primary">Create</button>
                  </div>
                  </form>
              </div>
          </div>
      </div>
    `);
  }
  style() {
    return (`
      <style>
      #tournament {
          height: 100vh;
      }
      
      .tournament-card {
          width: 550px;
      }
      
      #have-account {
          font-size: 13px;
          color: var(--bs-primary);
      }
      </style>
    `);
  }


  postRender() {
    this.maxPlayersRange = this.querySelector('#max-players');
    super.addComponentEventListener(
        this.maxPlayersRange, 'input', this.#maxPlayersRangeHandler,
    );
    this.privateSwitch = this.querySelector('#private-switch');
    super.addComponentEventListener(
        this.privateSwitch, 'change', this.#privateSwitchHandler,
    );
    this.createBtn = this.querySelector('#createBtn');
    super.addComponentEventListener(
        this.createBtn, 'click', this.#createBtnHandler,
    );
    this.alertForm = this.querySelector('#alert-form');
    this.password = this.querySelector('#password');
    this.passwordEyeIcon = this.querySelector('#password-eye');
    super.addComponentEventListener(
        this.passwordEyeIcon, 'click', this.#togglePasswordVisibility,
    );
  }

  #maxPlayersRangeHandler() {
    const maxPlayers = this.maxPlayersRange.value;
    this.querySelector('label[for="max-players"]').innerHTML = `Max players: ${maxPlayers}`;
  }

  #privateSwitchHandler() {
    const passwordBox = this.querySelector('#password-box');
    if (this.privateSwitch.checked) {
      passwordBox.classList.remove('d-none');
    } else {
      passwordBox.classList.add('d-none');
    }
  }

  async #createBtnHandler(event) {
    event.preventDefault();
    const name = this.querySelector('#name').value;
    const maxPlayers = parseInt(this.maxPlayersRange.value);
    const isPrivate = this.privateSwitch.checked;
    const password = this.password.value;
    try {
      const {response, body} = await window.ApiClient.createTournament(
          name, maxPlayers, isPrivate, password,
      );
      if (response.ok) {
        window.router.navigate(`/tournaments/`);
      } else {
        this.alertForm.setAttribute('alert-message', body.errors[0]);
        this.alertForm.setAttribute('alert-display', 'true');
      }
    } catch (error) {
      ErrorPage.loadNetworkError();
    }
  }

  #togglePasswordVisibility() {
    if (this.passwordHiden) {
      this.password.setAttribute('type', 'text');
    } else {
      this.password.setAttribute('type', 'password');
    }
    this.passwordEyeIcon.children[0].classList.toggle('bi-eye-fill');
    this.passwordEyeIcon.children[0].classList.toggle('bi-eye-slash-fill');
    this.passwordHiden = !this.passwordHiden;
  }
}
