import {Component} from '@components';
import {Keys} from '@utils/Keys.js';
import {userManagementClient} from '@utils/api';
import {ErrorPage} from '@utils/ErrorPage.js';
import {getRouter} from '../../../Router.js';

export class Settings2FA extends Component {
  constructor() {
    super();
  }

  render() {
    this.qrCode = this.getAttribute('qr-code');
    return (`
      <div id="settings-two-fa"
           class="d-flex justify-content-center align-items-center rounded-3">
          <div class="settings-two-fa-card card m-3">
              <div class="card-body m-2">
                  <h2 class="card-title text-center m-5">Enable two-factor authentication</h2>
                  <p class="text-center">Scan QR-Code and enter the 6-digit code received by your mobile application</p>
                  <form id="form">
                      <div class="d-flex justify-content-center mb-4">
                        <img src="${this.qrCode}" class="img-fluid" alt="QR code" style="height: 250px; width: 250px">
                      </div>
                      <div class="form-group row mb-4">
                          <input class="code-input form-control text-center col" type="tel" name="pincode-1" maxlength="1"
                                 pattern="[\\d]*" tabindex="1" placeholder="·"
                                 autocomplete="off">
                          <input class="code-input form-control text-center col" type="tel" name="pincode-2" maxlength="1"
                                 pattern="[\\d]*" tabindex="2" placeholder="·"
                                 autocomplete="off">
                          <input class="code-input form-control text-center col" type="tel" name="pincode-3" maxlength="1"
                                 pattern="[\\d]*" tabindex="3" placeholder="·"
                                 autocomplete="off">
                          <input class="code-input form-control text-center col" type="tel" name="pincode-4" maxlength="1"
                                 pattern="[\\d]*" tabindex="4" placeholder="·"
                                 autocomplete="off">
                          <input class="code-input form-control text-center col" type="tel" name="pincode-5" maxlength="1"
                                 pattern="[\\d]*" tabindex="5" placeholder="·"
                                 autocomplete="off">
                          <input class="code-input form-control text-center col" type="tel" name="pincode-6" maxlength="1"
                                 pattern="[\\d]*" tabindex="6" placeholder="·"
                                 autocomplete="off">
                      </div>
                      <alert-component id="alert-form" alert-display="false"></alert-component>
                      <div class="row d-flex justify-content-center">
                          <button id="sendCodeBtn" type="submit" class="btn btn-primary" disabled>Send code</button>
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
      .code-input {
      margin: 0 0.2rem;
      }
      
      #settings-two-fa {
          height: 100vh;
      }
      
      .settings-two-fa-card {
          width: 550px;
      }
      </style>
    `);
  }

  postRender() {
    this.inputs = this.querySelectorAll('input');
    for (const input of this.inputs) {
      super.addComponentEventListener(input, 'keydown',
          this.#handleInputChange);
      super.addComponentEventListener(input, 'paste',
          this.#handlePaste);
    }
    this.sendCodeBtn = this.querySelector('#sendCodeBtn');
    super.addComponentEventListener(this.sendCodeBtn, 'click', this.#sendCode);
    this.alertForm = this.querySelector('#alert-form');
  }

  #handleInputChange(event) {
    if (!Keys.isPasteShortcut(event)) {
      event.preventDefault();
    }
    if (!Keys.isDigitKey(event) && !Keys.isDeleteKey(event)) {
      event.target.value = '';
      return;
    }
    if (Keys.isDeleteKey(event)) {
      event.target.value = '';
      this.#focusPreviousInput(event.target);
      return;
    }
    event.target.value = Keys.getDigitValue(event);
    this.#formHandler();
    this.#focusNextInput(event.target);
  }

  #handlePaste(event) {
    event.preventDefault();
    const clipboardData = event.clipboardData || window.clipboardData;
    const pastedText = clipboardData.getData('text').replace(/\D/g, '');
    let currentInput = event.target;
    for (let i = 0; i < pastedText.length && currentInput !== null; i++) {
      currentInput.value = pastedText[i];
      this.#formHandler();
      currentInput = this.#focusNextInput(currentInput);
    }
  }
  #formHandler() {
    for (const input of this.inputs) {
      if (!input.value) {
        this.sendCodeBtn.disabled = true;
        return;
      }
    }
    this.sendCodeBtn.disabled = false;
    this.#sendCode();
  }

  async #sendCode() {
    this.#startLoadButton();
    this.code = Array.from(this.inputs).map((input) => input.value).join('');
    try {
      const {response, body} =
          await userManagementClient.verify2FA(
              this.code,
          );
      if (response.ok) {
        getRouter().redirect('/settings/');
      } else {
        this.#resetLoadButton();
        this.alertForm.setAttribute('alert-message', body.errors[0]);
        this.alertForm.setAttribute('alert-display', 'true');
      }
    } catch (error) {
      ErrorPage.loadNetworkError();
    }
  }

  #focusPreviousInput(input) {
    const previousInput = input.previousElementSibling;
    if (previousInput) {
      previousInput.focus();
      return previousInput;
    }
    return null;
  }

  #focusNextInput(input) {
    const nextInput = input.nextElementSibling;
    if (nextInput) {
      nextInput.focus();
      return nextInput;
    }
    return null;
  }

  #startLoadButton() {
    this.sendCodeBtn.innerHTML = `
      <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
      <span class="sr-only">Loading...</span>
    `;
    this.sendCodeBtn.disabled = true;
  }

  #resetLoadButton() {
    this.sendCodeBtn.innerHTML = 'Send code';
    this.sendCodeBtn.disabled = false;
  }
}
