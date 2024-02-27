import {Component} from '@components';
import {InputValidator} from '@utils/InputValidator.js';
import {BootstrapUtils} from '@utils/BootstrapUtils.js';
import {ErrorPage} from '@utils/ErrorPage.js';
import {userManagementClient} from '@utils/api';
import {getRouter} from '@js/Router.js';
import {Cookies} from '@js/Cookies.js';
import {JWT} from '@utils/JWT.js';

export class SignUp extends Component {
  constructor() {
    super();
    this.passwordHiden = true;
    this.confirmPasswordHiden = true;
    this.startConfirmPassword = false;

    this.InputValidUsername = false;
    this.InputValidEmail = false;
    this.InputValidPassword = false;
    this.InputValidConfirmPassword = false;

    this.error = false;
    this.errorMessage = '';
  }

  render() {
    if (userManagementClient.isAuth()) {
      getRouter().redirect('/');
      return false;
    }
    const {render} = this.#OAuthReturn();
    if (!render) {
      return false;
    }
    return (`
      <navbar-component disable-padding-top="true"></navbar-component>
      <div id="login"
           class="d-flex justify-content-center align-items-center rounded-3">
          <div class="login-card card m-3">
              <div class="card-body m-2">
                  <h2 class="card-title text-center m-5 dynamic-hover">Sign up</h2>
                  <form id="signup-form">
                      <div class="form-group mb-4">
                          <div class="input-group has-validation">
                              <span class="input-group-text"
                                    id="inputGroupPrepend">@</span>
                              <input type="text" class="form-control" id="username"
                                     placeholder="Username">
                              <div id="username-feedback" class="invalid-feedback">
                                  Invalid username.
                              </div>
                          </div>
                      </div>
                      <div class="form-group mb-4">
                          <input type="email" class="form-control" id="email"
                                 placeholder="Email">
                          <div id="email-feedback" class="invalid-feedback">
                              Please enter a valid email.
                          </div>
                      </div>
                      <div class="form-group mb-4">
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
                      <div class="form-group mb-4">
                          <div class="input-group has-validation">
                              <input type="password" class="form-control"
                                     id="confirm-password"
                                     placeholder="Confirm Password">
                              <span id="confirm-password-eye"
                                    class="input-group-text dynamic-hover">
                                  <i class="bi bi-eye-fill"></i>
                              </span>
                              <div id="confirm-password-feedback" class="invalid-feedback">
                                  Passwords do not match.
                              </div>
                          </div>
                      </div>
                  <alert-component id="alert-form" alert-display="false">
                  </alert-component>
                  <div class="d-flex mb-3">
                      <a id="have-account">Already have an account?</a>
                  </div>
                  <div class="row d-flex justify-content-center">
                      <button id="signupBtn" type="submit" class="btn btn-primary" disabled>Sign up</button>
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
      
      #have-account {
          font-size: 13px;
          color: var(--bs-primary);
      }
      </style>
    `);
  }


  postRender() {
    this.username = this.querySelector('#username');
    this.usernameFeedback = this.querySelector('#username-feedback');
    super.addComponentEventListener(this.username, 'input',
        this.#usernameHandler);

    this.email = this.querySelector('#email');
    this.emailFeedback = this.querySelector('#email-feedback');
    super.addComponentEventListener(this.email, 'input',
        this.#emailHandler);

    this.password = this.querySelector('#password');
    this.passwordEyeIcon = this.querySelector('#password-eye');
    this.passwordFeeback = this.querySelector('#password-feedback');
    super.addComponentEventListener(this.password, 'input',
        this.#passwordHandler);
    super.addComponentEventListener(this.passwordEyeIcon, 'click',
        this.#togglePasswordVisibility);

    this.confirmPassword = this.querySelector('#confirm-password');
    this.confirmPasswordEyeIcon = this.querySelector(
        '#confirm-password-eye');
    this.confirmPasswordFeedback = this.querySelector(
        '#confirm-password-feedback');
    super.addComponentEventListener(this.confirmPassword, 'input',
        this.#confirmPasswordHandler);
    super.addComponentEventListener(this.confirmPasswordEyeIcon, 'click',
        this.#toggleConfirmPasswordVisibility);

    this.haveAccount = this.querySelector('#have-account');
    super.addComponentEventListener(this.haveAccount, 'click', () =>
      getRouter().navigate('/signin/'),
    );
    this.alertForm = this.querySelector('#alert-form');
    this.signupBtn = this.querySelector('#signupBtn');
    super.addComponentEventListener(this.signupBtn, 'click', (event) => {
      event.preventDefault();
      this.#signupHandler();
    });
    this.signupForm = this.querySelector('#signup-form');
    super.addComponentEventListener(this.signupForm, 'submit', (event) => {
      event.preventDefault();
      this.#signupHandler();
    });
    if (this.error) {
      this.alertForm.setAttribute('alert-message', this.errorMessage);
      this.alertForm.setAttribute('alert-display', 'true');
      this.error = false;
    }
  }

  reRender() {
    this.innerHTML = this.render() + this.style();
    this.postRender();
  }

  #renderLoader() {
    return (`
      <navbar-component disable-padding-top="true"></navbar-component>
      <div class="d-flex justify-content-center align-items-center" style="height: 100vh">
          <div class="spinner-border" role="status">
              <span class="visually-hidden">Loading...</span>
          </div>
      </div>
    `);
  }


  async #usernameHandler() {
    clearTimeout(this.usernameTimeout);
    const {validity, missingRequirements} =
      InputValidator.isValidUsername(this.username.value);
    if (validity) {
      this.usernameTimeout = setTimeout(() => {
        this.#usernameExist();
      }, 500);
    } else {
      this.#setUsernameInputValidity(false, missingRequirements[0]);
    }
  }

  async #usernameExist() {
    try {
      const {response, body} = await userManagementClient.usernameExist(
          this.username.value,
      );
      if (response.ok && body.is_taken) {
        this.#setUsernameInputValidity(false, 'Username already taken.');
      } else {
        this.#setUsernameInputValidity(true);
      }
    } catch (error) {
      this.#setUsernameInputValidity(true);
    }
  }

  #setUsernameInputValidity(validity, message='') {
    if (validity) {
      BootstrapUtils.setValidInput(this.username);
      this.InputValidUsername = true;
    } else {
      BootstrapUtils.setInvalidInput(this.username);
      this.usernameFeedback.innerHTML = message;
      this.InputValidUsername = false;
    }
    this.#formHandler();
  }

  #emailHandler() {
    clearTimeout(this.emailTimeout);
    const {validity, missingRequirements} =
      InputValidator.isValidEmail(this.email.value);
    if (validity) {
      this.emailTimeout = setTimeout(() => {
        this.#emailExist();
      }, 500);
    } else {
      this.#setEmailInputValidity(false, missingRequirements[0]);
    }
  }

  async #emailExist() {
    try {
      const {response, body} = await userManagementClient.emailExist(
          this.email.value,
      );
      if (response.ok && body.is_taken) {
        this.#setEmailInputValidity(false, 'Email already taken.');
      } else {
        this.#setEmailInputValidity(true);
      }
    } catch (error) {
      this.#setEmailInputValidity(true);
    }
  }

  #setEmailInputValidity(validity, message='') {
    if (validity) {
      BootstrapUtils.setValidInput(this.email);
      this.InputValidEmail = true;
    } else {
      BootstrapUtils.setInvalidInput(this.email);
      this.emailFeedback.innerHTML = message;
      this.InputValidEmail = false;
    }
    this.#formHandler();
  }

  #passwordHandler() {
    const {validity, missingRequirements} =
      InputValidator.isValidSecurePassword(this.password.value);
    if (validity) {
      this.#setInputPasswordValidity(true);
      if (this.startConfirmPassword) {
        if (this.confirmPassword.value === this.password.value) {
          this.#setInputConfirmPasswordValidity(true);
        } else {
          this.#setInputConfirmPasswordValidity(false,
              'Passwords do not match.');
        }
      }
    } else {
      this.#setInputPasswordValidity(false, missingRequirements[0]);
      if (this.startConfirmPassword) {
        this.#setInputConfirmPasswordValidity(false);
      }
    }
  }

  #confirmPasswordHandler() {
    if (!this.startConfirmPassword) {
      this.startConfirmPassword = true;
    }
    this.#passwordHandler();
  }

  #setInputPasswordValidity(validity, message='') {
    if (validity) {
      BootstrapUtils.setValidInput(this.password);
      this.InputValidPassword = true;
    } else {
      BootstrapUtils.setInvalidInput(this.password);
      this.passwordFeeback.innerHTML = message;
      this.InputValidPassword = false;
    }
    this.#formHandler();
  }

  #setInputConfirmPasswordValidity(validity, message='') {
    if (validity) {
      BootstrapUtils.setValidInput(this.confirmPassword);
      this.InputValidConfirmPassword = true;
    } else {
      BootstrapUtils.setInvalidInput(this.confirmPassword);
      this.confirmPasswordFeedback.innerHTML = message;
      this.InputValidConfirmPassword = false;
    }
    this.#formHandler();
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

  #toggleConfirmPasswordVisibility() {
    if (this.confirmPasswordHiden) {
      this.confirmPassword.setAttribute('type', 'text');
    } else {
      this.confirmPassword.setAttribute('type', 'password');
    }
    this.confirmPasswordEyeIcon.children[0].classList.toggle('bi-eye-fill');
    this.confirmPasswordEyeIcon.children[0].classList.toggle(
        'bi-eye-slash-fill');
    this.confirmPasswordHiden = !this.confirmPasswordHiden;
  }

  #formHandler() {
    if (this.InputValidUsername && this.InputValidEmail &&
      this.InputValidPassword && this.InputValidConfirmPassword) {
      this.signupBtn.disabled = false;
    } else {
      this.signupBtn.disabled = true;
    }
  }

  async #signupHandler() {
    this.#startLoadButton();
    try {
      const {response, body} = await userManagementClient.signUp(
          this.username.value, this.email.value, this.password.value);
      if (response.ok) {
        this.#loadEmailVerification();
      } else {
        this.#resetLoadButton();
        this.alertForm.setAttribute('alert-message', body.errors[0]);
        this.alertForm.setAttribute('alert-display', 'true');
      }
    } catch (error) {
      ErrorPage.loadNetworkError();
    }
  }

  #OAuthReturn() {
    if (!this.#isOAuthError()) {
      return {render: true};
    }
    const refreshToken = Cookies.get('refresh_token');
    Cookies.remove('refresh_token');
    if (new JWT(refreshToken).isValid()) {
      this.#loadAndCache(refreshToken);
      return {render: false};
    }
    return {render: true};
  }

  #isOAuthError() {
    const params = new URLSearchParams(window.location.search);
    if (params.has('error')) {
      this.error = true;
      this.errorMessage = params.get('error');
      return false;
    }
    return true;
  }

  async #loadAndCache(refreshToken) {
    this.innerHTML = this.#renderLoader();
    userManagementClient.refreshToken = refreshToken;
    if (!await userManagementClient.restoreCache()) {
      userManagementClient.logout();
      this.error = true;
      this.errorMessage = 'Error, failed to store cache';
      this.reRender();
    } else {
      getRouter().navigate('/');
    }
  }

  #startLoadButton() {
    this.signupBtn.innerHTML = `
      <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
      <span class="sr-only">Loading...</span>
    `;
    this.signupBtn.disabled = true;
  }

  #resetLoadButton() {
    this.signupBtn.innerHTML = 'Sign up';
    this.signupBtn.disabled = false;
  }

  #loadEmailVerification() {
    const cardBody = this.querySelector('.card-body');
    cardBody.innerHTML = this.#renderEmailVerification();
  }

  #renderEmailVerification() {
    return (`
      <h2 class="card-title text-center m-5 dynamic-hover">Activate your account</h2>
      <p class="text-center">Please verify your email address to continue</p> 
      <div class="d-flex justify-content-center mb-4">
        <i class="bi bi-envelope-arrow-up" style="font-size: 7rem;"></i>
      </div>
    `);
  }
}
