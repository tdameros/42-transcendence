import {Component} from '@components';
import {InputValidator} from '@utils/InputValidator.js';
import {BootstrapUtils} from '@utils/BootstrapUtils.js';
import {userManagementClient} from '@utils/api';
import {ErrorPage} from '@utils/ErrorPage.js';
import {ResetPasswordCode} from './ResetPasswordCode.js';
import {NavbarUtils} from '@utils/NavbarUtils.js';

export class ResetPasswordEmail extends Component {
  constructor() {
    super();
  }
  render() {
    return (`
      <div id="reset-password"
           class="d-flex justify-content-center align-items-center rounded-3">
          <div class="reset-password-card card m-3">
              <div class="card-body m-2">
                  <h2 class="card-title text-center m-5">Reset password</h2>
                  <form id="reset-password-form">
                      <div class="d-flex justify-content-center mb-4">
                          <i class="bi bi-envelope-at-fill"
                             style="font-size: 5rem;"></i>
                      </div>
                      <div class="form-group mb-4">
                          <input type="email" class="form-control" id="email"
                                 placeholder="Email" autocomplete="email">
                          <div id="email-feedback" class="invalid-feedback">
                              Please enter a valid email.
                          </div>
                      </div>
                  <alert-component id="alert-form" alert-display="false"></alert-component>
                  <div class="row d-flex justify-content-center">
                      <button id="sendEmailBtn" type="submit" class="btn btn-primary" disabled>Send email</button>
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
    this.email = this.querySelector('#email');
    this.emailFeedback = this.querySelector('#email-feedback');
    super.addComponentEventListener(this.email, 'input',
        this.#emailHandler);
    this.sendEmailBtn = this.querySelector('#sendEmailBtn');
    this.form = this.querySelector('#reset-password-form');
    super.addComponentEventListener(this.form, 'submit', (event) => {
      event.preventDefault();
      this.#sendEmail();
    });
    this.alertForm = this.querySelector('#alert-form');
  }

  #emailHandler() {
    const {validity, missingRequirements} =
      InputValidator.isValidEmail(this.email.value);
    if (validity) {
      BootstrapUtils.setValidInput(this.email);
      this.InputValidEmail = true;
      this.sendEmailBtn.disabled = false;
    } else {
      BootstrapUtils.setInvalidInput(this.email);
      this.emailFeedback.innerHTML = missingRequirements[0];
      this.InputValidEmail = false;
      this.sendEmailBtn.disabled = true;
    }
  }

  async #sendEmail() {
    this.#startLoadButton();
    try {
      const {response, body} = await userManagementClient.sendResetPasswordCode(
          this.email.value,
      );
      if (response.ok) {
        this.#loadCodeComponent();
      } else {
        this.#resetLoadButton();
        this.alertForm.setAttribute('alert-message', body.errors[0]);
        this.alertForm.setAttribute('alert-display', 'true');
      }
    } catch (error) {
      ErrorPage.loadNetworkError();
    }
  }

  #loadCodeComponent() {
    const codeComponent = new ResetPasswordCode();
    codeComponent.email = this.email.value;
    this.innerHTML = '';
    this.appendChild(codeComponent);
  }

  #startLoadButton() {
    this.sendEmailBtn.innerHTML = `
      <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
      <span class="sr-only">Loading...</span>
    `;
    this.sendEmailBtn.disabled = true;
  }

  #resetLoadButton() {
    this.sendEmailBtn.innerHTML = 'Send email';
    this.sendEmailBtn.disabled = false;
  }
}
