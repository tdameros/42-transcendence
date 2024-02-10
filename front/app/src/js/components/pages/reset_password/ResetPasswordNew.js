import {Component} from '@components';
import {InputValidator} from '@utils/InputValidator.js';
import {BootstrapUtils} from '@utils/BootstrapUtils.js';

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
                  </form>
                  <div class="row d-flex justify-content-center">
                      <button id="confirm-btn" type="submit" class="btn btn-primary" disabled>Change password</button>
                  </div>
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
          height: 100vh;
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
    super.addComponentEventListener(this.confirmBtn, 'click',
        this.#confirmBtnHandler);
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

  #confirmBtnHandler() {
    console.log('confirmBtnHandler');
  }
}
