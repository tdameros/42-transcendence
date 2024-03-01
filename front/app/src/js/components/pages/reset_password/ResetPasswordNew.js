import {Component} from '@components';
import {InputValidator} from '@utils/InputValidator.js';
import {BootstrapUtils} from '@utils/BootstrapUtils.js';
import {userManagementClient} from '@utils/api';
import {ErrorPage} from '@utils/ErrorPage.js';
import {NavbarUtils} from '@utils/NavbarUtils.js';

export class ResetPasswordNew extends Component {
  constructor() {
    super();
    this.passwordHiden = true;
    this.confirmPasswordHiden = true;
    this.startConfirmPassword = false;
    this.InputValidPassword = false;
    this.InputValidConfirmPassword = false;
  }

  render() {
    return (`
      <div id="reset-password"
           class="d-flex justify-content-center align-items-center rounded-3">
          <div class="reset-password-card card m-3">
              <div class="card-body m-2">
                  <h2 class="card-title text-center m-5">Reset password</h2>
                  <p class="text-center">Enter a new password</p>
                  <form id="form">
                      <div class="d-flex justify-content-center mb-4">
                          <i class="bi bi-key-fill"
                             style="font-size: 5rem;"></i>
                      </div>
                      <div class="form-group mb-4">
                          <div class="input-group has-validation">
                              <input type="password" class="form-control"
                                     id="password"
                                     placeholder="Password">
                              <span id="password-eye"
                                    class="input-group-text eye-box">
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
                                    class="input-group-text eye-box">
                                  <i class="bi bi-eye-fill"></i>
                              </span>
                              <div id="confirm-password-feedback" class="invalid-feedback">
                                  Passwords do not match.
                              </div>
                          </div>
                      </div>
                      <alert-component id="alert-form" alert-display="false"></alert-component>
                      <div class="row d-flex justify-content-center">
                          <button id="confirm-btn" type="submit" class="btn btn-primary" disabled>Change password</button>
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
      .active {
          font-family: 'JetBrains Mono', monospace;
      }
      
      #reset-password {
          height: calc(100vh - ${NavbarUtils.height}px);
      }
      
      .reset-password-card {
          width: 550px;
      }
      </style>
    `);
  }

  postRender() {
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
    this.confirmBtn = this.querySelector('#confirm-btn');
    this.alertForm = this.querySelector('#alert-form');
    this.form = this.querySelector('#form');
    super.addComponentEventListener(this.form, 'submit', (event) => {
      event.preventDefault();
      this.#confirmBtnHandler();
    });
  }

  #successRender() {
    return (`
      <div id="reset-password"
           class="d-flex justify-content-center align-items-center rounded-3">
          <div class="reset-password-card card m-3">
              <div class="card-body m-2">
                  <h2 class="card-title
                      text-center m-5">Password changed</h2>
                  <div class="alert alert-success text-center" role="alert">
                      Your password has been changed!
                  </div>
                  <div class="row d-flex justify-content-center">
                      <button onclick="window.router.navigate('/signin/')" class="btn btn-primary">Sign in</button>
                  </div>
              </div>
          </div>
      </div>
    `);
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
    this.confirmBtn.disabled = !(this.InputValidPassword &&
      this.InputValidConfirmPassword);
  }

  async #confirmBtnHandler() {
    this.#startLoadButton();
    try {
      const {response, body} = await userManagementClient.changePassword(
          this.email, this.code, this.password.value);
      if (response.ok) {
        this.innerHTML = this.#successRender() + this.style();
      } else {
        this.#resetLoadButton();
        this.alertForm.setAttribute('alert-message', body.errors[0]);
        this.alertForm.setAttribute('alert-display', 'true');
      }
    } catch (error) {
      ErrorPage.loadNetworkError();
    }
  }

  #startLoadButton() {
    this.confirmBtn.innerHTML = `
      <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
      <span class="sr-only">Loading...</span>
    `;
    this.confirmBtn.disabled = true;
  }

  #resetLoadButton() {
    this.confirmBtn.innerHTML = 'Change password';
    this.confirmBtn.disabled = false;
  }
}
