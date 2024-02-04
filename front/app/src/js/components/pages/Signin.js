import {Component} from '../Component.js';
import {ErrorPage} from '../../utils/ErrorPage.js';

export class Signin extends Component {
  constructor() {
    super();
    this.isValidEmailInput = false;
    this.isValidPasswordInput = false;
  }

  render() {
    if (window.ApiClient.isAuth()) {
      window.router.redirect('/');
      return false;
    }
    return (`
      <navbar-component disable-padding-top="true"></navbar-component>
      <div id="login"
           class="d-flex justify-content-center align-items-center rounded-3">
          <div class="login-card card m-3">
              <div class="card-body m-2">
                  <h2 class="card-title text-center m-5">Sign in</h2>
                  <form id="signin-form">
                      <div class="form-group mb-4">
                          <input type="text" class="form-control" id="email"
                                 placeholder="Username">
                          <div id="email-feedback" class="invalid-feedback">
                              Please enter a valid email.
                          </div>
                      </div>
                      
                      <div class="form-group mb-4">
                          <div class="input-group">
                              <input type="password" class="form-control"
                                     id="password"
                                     placeholder="Password">
                              <span id="password-eye"
                                    class="input-group-text dynamic-hover">
                                  <i class="bi bi-eye-fill"></i>
                              </span>
                          </div>
                      </div>
                      <alert-component id="alert-form" alert-dispaly="false">
                      </alert-component>
                      <div class="d-flex justify-content-between mb-3">
                          <a id="dont-have-account">Don't have an account?</a>
                          <a id="forgot-password">Forgot pasword?</a>
                      </div>
                      <div class="row d-flex justify-content-center">
                          <button id="signin-btn" class="btn btn-primary" disabled>Sign in
                          </button>
                      </div>
                  </form>
                  <hr class="my-4">
                  <div class="row">
                    <github-button-component class="p-0"></github-button-component>
                    <intra-button-component class="p-0"></intra-button-component>
                  </div>
              </div>
          </div>
      </div>
    `);
  }

  style() {
    return (`
      <style>
      #login {
          height: 100vh;
      }
      
      .login-card {
          width: 550px;
      }
      
      #forgot-password, #dont-have-account {
          font-size: 13px;
          color: rgb(13, 110, 253);
      }
      </style>
    `);
  }

  postRender() {
    this.forgotPassword = this.querySelector('#forgot-password');
    super.addComponentEventListener(this.forgotPassword, 'click', () => {
      window.router.navigate('/reset-password/');
    });
    this.donthaveAccount = this.querySelector('#dont-have-account');
    super.addComponentEventListener(this.donthaveAccount, 'click', () => {
      window.router.navigate('/signup/');
    });
    this.signinBtn = this.querySelector('#signin-btn');
    super.addComponentEventListener(this.signinBtn, 'click', (event) => {
      event.preventDefault();
      this.#signin();
    });
    this.signinForm = this.querySelector('#signin-form');
    super.addComponentEventListener(this.signinForm, 'submit', (event) => {
      event.preventDefault();
      this.#signin();
    });
    this.email = this.querySelector('#email');
    super.addComponentEventListener(this.email, 'input',
        this.#emailHandler);
    this.password = this.querySelector('#password');
    this.passwordEyeIcon = this.querySelector('#password-eye');
    super.addComponentEventListener(this.password, 'input',
        this.#passwordHandler);
    super.addComponentEventListener(this.passwordEyeIcon, 'click',
        this.#togglePasswordVisibility);

    this.alertForm = this.querySelector('#alert-form');
  }

  #emailHandler() {
    this.isValidEmailInput = this.email.value.length > 0;
    this.#formHandler();
  }

  #passwordHandler() {
    this.isValidPasswordInput = this.password.value.length > 0;
    this.#formHandler();
  }

  #formHandler() {
    this.signinBtn.disabled = !(this.isValidEmailInput &&
      this.isValidPasswordInput);
  }

  async #signin() {
    try {
      const {response, body} = await window.ApiClient.signIn(this.email.value,
          this.password.value);
      if (response.ok) {
        window.ApiClient.refreshToken = body.refresh_token;
        await window.ApiClient.restoreCache();
        window.router.navigate('/');
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
