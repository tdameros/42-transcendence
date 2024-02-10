import {Component} from '@components';
import {InputValidator} from '@utils/InputValidator.js';
import {BootstrapUtils} from '@utils/BootstrapUtils.js';

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
                  <form>
                      <div class="d-flex justify-content-center mb-4">
                          <i class="bi bi-envelope-at-fill"
                             style="font-size: 5rem;"></i>
                      </div>
                      <div class="form-group mb-4">
                          <input type="email" class="form-control" id="email"
                                 placeholder="Email">
                          <div id="email-feedback" class="invalid-feedback">
                              Please enter a valid email.
                          </div>
                      </div>
                  </form>
                  <div class="row d-flex justify-content-center">
                      <button id="sendEmailBtn" type="submit" class="btn btn-primary" disabled>Send email</button>
                  </div>
              </div>
          </div>
      </div>
    `);
  }
  style() {
    return (`
      <style>
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
    this.email = this.querySelector('#email');
    this.emailFeedback = this.querySelector('#email-feedback');
    super.addComponentEventListener(this.email, 'input',
        this.#emailHandler);
    this.sendEmailBtn = this.querySelector('#sendEmailBtn');
    super.addComponentEventListener(this.sendEmailBtn, 'click',
        this.#sendEmail);
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
    const newComponent = document.createElement(
        'reset-password-code-component',
    );
    this.innerHTML = '';
    this.appendChild(newComponent);
  }
}
