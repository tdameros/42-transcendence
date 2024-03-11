import {Component} from '@components';
import {InputValidator} from '@utils/InputValidator.js';
import {BootstrapUtils} from '@utils/BootstrapUtils.js';
import {ErrorPage} from '@utils/ErrorPage.js';
import {userManagementClient} from '@utils/api';
import {getRouter} from '@js/Router.js';
import {Modal} from 'bootstrap';
import {NavbarUtils} from '@utils/NavbarUtils.js';

export class SettingsContent extends Component {
  constructor() {
    super();
    this.passwordHiden = true;
    this.confirmPasswordHiden = true;
    this.startConfirmPassword = false;

    this.inputValidUsername = false;
    this.inputValidEmail = false;
    this.inputValidPassword = false;
    this.inputValidConfirmPassword = false;

    this.hasChangeAvatar = false;
    this.base64Avatar = null;

    this.error = false;
    this.errorMessage = '';
  }

  render() {
    return (this.renderPlaceholder());
  }

  renderWithDefaultSettings() {
    const username = userManagementClient.username;
    return (`
      <div id="settings"
           class="d-flex justify-content-center align-items-center rounded-3">
          <div class="settings-card card m-3">
              <div class="card-body m-2">
                  <h2 class="card-title text-center m-5">Settings</h2>
                  <form id="settings-form">
                      <div class="form-group mb-4 d-flex justify-content-center position-relative">
                          <div class="position-relative">
                              <img id="avatar" src="${userManagementClient.getURLAvatar(username)}"
                                   class="rounded-circle object-fit-cover" style="width: 125px; height: 125px;">
                              <button id="trash-icon" type="button"
                                      class="btn btn-danger btn-sm position-absolute bottom-0 end-0">
                                  <i class="bi bi-trash-fill"></i>
                              </button>
                          </div>
                      </div>
                      <div class="form-group mb-4">
                          <div class="input-group has-validation">
                                    <span class="input-group-text"
                                          id="inputGroupPrepend">@</span>
                              <input type="text" class="form-control" id="username"
                                     placeholder="New username" value="${this.defaultUsername}"
                                     autocomplete="username">
                              <div id="username-feedback" class="invalid-feedback">
                                  Invalid username.
                              </div>
                          </div>
                      </div>
                      <div class="form-group mb-4">
                          <input type="email" class="form-control" id="email"
                                 placeholder="New email" value="${this.defaultEmail}"
                                 autocomplete="email">
                          <div id="email-feedback" class="invalid-feedback">
                              Please enter a valid email.
                          </div>
                      </div>
                      <div class="form-group mb-4">
                          <div class="input-group has-validation">
                              <input type="password" class="form-control"
                                     id="password"
                                     placeholder="New password">
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
                                     placeholder="Confirm new password">
                              <span id="confirm-password-eye"
                                    class="input-group-text dynamic-hover">
                                        <i class="bi bi-eye-fill"></i>
                                    </span>
                              <div id="confirm-password-feedback" class="invalid-feedback">
                                  Passwords do not match.
                              </div>
                          </div>
                      </div>
                      <div class="form-group mb-4">
                          <div class="form-check form-switch">
                              <input class="form-check-input" type="checkbox" id="two-fa-switch" ${this.defaultHas2FA ?
                              'checked': ''}>
                              <label class="form-check-label" for="two-fa-switch">Two-factor authentication</label>
                          </div>
                      </div>
                      <alert-component id="alert-form" alert-display="false">
                      </alert-component>
                      <div class="d-flex flex-row mb-2">
                          <button id="export-button" type="button" class="btn btn-success">Export data</button>
                          <button id="delete-button" type="button" class="btn btn-danger ms-2">Delete account</button>
                      </div>
                      <div class="d-flex">
                          <button id="save-button" type="submit" class="btn btn-primary mb-2" disabled>Save changes</button>
                      </div>
                  </form>
              </div>
          </div>
      </div>
      <div class="modal fade" id="confirm-delete-modal" aria-hidden="true" tabindex="-1">
          <div class="modal-dialog modal-dialog-centered">
              <div class="modal-content">
                  <div class="modal-header">
                      <h1 class="modal-title fs-5 text-danger">Confirm Account Deletion</h1>
                      <button type="button" class="btn-close"
                              data-bs-dismiss="modal" aria-label="Close"></button>
                  </div>
                  <form>
                      <div class="modal-body d-flex flex-column justify-content-center">
                          <p>Are you sure you want to delete your account? This action cannot be undone, and all your data will
                              be anonymized.</p>
                          <alert-component id="alert-delete"
                                           alert-display="false"></alert-component>
                      </div>
                      <div class="modal-footer">
                          <button id="cancel-button" type="button" class="btn btn-secondary" data-dismiss="modal">Cancel
                          </button>
                          <button id="delete-account-btn" type="button" class="btn btn-danger">Delete</button>
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
      #settings {
          height: calc(100vh - ${NavbarUtils.height}px);
      }
      
      .settings-card {
          width: 550px;
      }
      
      #avatar {
        transition: transform 0.3s ease;
      }

      #avatar:hover {
        transform: scale(1.1); 
        cursor: pointer;
      }
    
      .hide-placeholder-text {
        color: var(--bs-secondary-bg);
        background-color: var(--bs-secondary-bg)!important;
      }
      </style>
    `);
  }

  renderPlaceholder() {
    const placeholderClass = 'placeholder placeholder-lg' +
      'bg-body-secondary rounded hide-placeholder-text';
    return (`
      <div id="settings"
           class="d-flex justify-content-center align-items-center rounded-3">
          <div class="settings-card card m-3">
              <div class="card-body m-2 placeholder-glow">
                  <h2 class="card-title text-center m-5 dynamic-hover">Settings</h2>
                  <form id="settings-form">
                  <div class="form-group mb-4 d-flex justify-content-center position-relative">
                    <div class="position-relative">
                      <img id="avatar" src="/img/default_avatar.png" class="${placeholderClass} rounded-circle object-fit-cover" style="width: 125px; height: 125px;">
                    </div>
                  </div>
                      <div class="form-group mb-4">
                          <span class="${placeholderClass} col-12 form-control">_</span>
                      </div>
                      <div class="form-group mb-4">
                          <span class="${placeholderClass} col-12 form-control">_</span>
                      </div>
                      <div class="form-group mb-4">
                          <span class="${placeholderClass} col-12 form-control">_</span>
                      </div>
                      <div class="form-group mb-4">
                          <span class="${placeholderClass} col-12 form-control">_</span>
                      </div>
                  <alert-component id="alert-form" alert-display="false">
                  </alert-component>
                  <div class="d-flex flex-row mb-2">
                      <button class="btn ${placeholderClass}">Export data</button>
                      <button class="btn ms-2 ${placeholderClass}">Delete account</button>
                  </div>
                  <div class="d-flex">
                      <button id="save-button" type="submit" class="btn mb-2 ${placeholderClass}">Save changes</button>
                  </div>
                  </form>
              </div>
          </div>
      </div>
    `);
  }


  async postRender() {
    if (!await this.loadDefaultSettings()) {
      return;
    }
    this.avatar = this.querySelector('#avatar');
    super.addComponentEventListener(this.avatar, 'click', this.#avatarHandler);

    this.trashIcon = this.querySelector('#trash-icon');
    super.addComponentEventListener(
        this.trashIcon, 'click', this.#trashAvatarHandler,
    );

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

    this.alertForm = this.querySelector('#alert-form');
    this.alertDelete = this.querySelector('#alert-delete');

    this.saveButton = this.querySelector('#save-button');
    super.addComponentEventListener(this.saveButton, 'click', (event) => {
      event.preventDefault();
      this.#saveHandler();
    });
    this.settingsForm = this.querySelector('#settings-form');
    super.addComponentEventListener(this.settingsForm, 'submit', (event) => {
      event.preventDefault();
      this.#saveHandler();
    });

    if (this.error) {
      this.alertForm.setAttribute('alert-message', this.errorMessage);
      this.alertForm.setAttribute('alert-type', 'error');
      this.alertForm.setAttribute('alert-display', 'true');
      this.error = false;
    }

    this.twoFASwitch = this.querySelector('#two-fa-switch');
    super.addComponentEventListener(this.twoFASwitch, 'change', (event) => {
      this.#formHandler();
    });

    const deleteModal = document.getElementById('confirm-delete-modal');
    this.deleteModal = new Modal(deleteModal);
    super.addComponentEventListener(deleteModal, 'hidden.bs.modal', () => {
      this.alertDelete.setAttribute('alert-message', '');
      this.alertForm.setAttribute('alert-type', 'error');
      this.alertDelete.setAttribute('alert-display', 'false');
    });

    this.exportButton = this.querySelector('#export-button');
    super.addComponentEventListener(
        this.exportButton, 'click', this.#exportHandler,
    );

    this.deleteButton = this.querySelector('#delete-button');
    super.addComponentEventListener(
        this.deleteButton, 'click', this.#deleteHandler,
    );

    this.deleteAccountButton = this.querySelector('#delete-account-btn');
    super.addComponentEventListener(
        this.deleteAccountButton, 'click', this.#deleteAccountHandler,
    );

    this.cancelButton = this.querySelector('#cancel-button');
    super.addComponentEventListener(
        this.cancelButton, 'click', this.#cancelHandler,
    );
  }

  async loadDefaultSettings() {
    try {
      const {response, body} = await userManagementClient.getMe();
      if (response.ok) {
        this.defaultUsername = body['username'];
        this.defaultEmail = body['email'];
        this.defaultHas2FA = body['2fa'];
        this.innerHTML = this.renderWithDefaultSettings() + this.style();
        return true;
      } else {
        getRouter().navigate('/signin/');
      }
    } catch (error) {
      ErrorPage.loadNetworkError();
    }
    return false;
  }

  async #avatarHandler() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/jpeg, image/png';
    input.onchange = (event) => {
      const file = event.target.files[0];
      try {
        if (!file.type.match('image/jpeg') && !file.type.match('image/png')) {
          this.alertForm.setAttribute(
              'alert-message',
              'Invalid file format. Please select a JPEG or PNG image.',
          );
          this.alertForm.setAttribute('alert-type', 'error');
          this.alertForm.setAttribute('alert-display', 'true');
          return;
        }
      } catch (error) {
        this.alertForm.setAttribute(
            'alert-message',
            'Invalid file format. Please select a JPEG or PNG image.',
        );
        this.alertForm.setAttribute('alert-type', 'error');
        this.alertForm.setAttribute('alert-display', 'true');
        return;
      }
      const reader = new FileReader();
      reader.onload = async (event) => {
        this.base64Avatar = event.target.result;
        const sizeInMB = file.size / (1024 * 1024);
        if (sizeInMB > 1) {
          this.alertForm.setAttribute('alert-message', 'File too large.');
          this.alertForm.setAttribute('alert-type', 'error');
          this.alertForm.setAttribute('alert-display', 'true');
          return;
        }
        this.hasChangeAvatar = true;
        this.#formHandler();
        this.avatar.src = event.target.result;
      };
      reader.readAsDataURL(file);
    };
    input.click();
  }

  async #trashAvatarHandler(event) {
    event.preventDefault();
    this.hasChangeAvatar = true;
    this.base64Avatar = null;
    this.avatar.src = '/img/default_avatar.png';
    this.#formHandler();
  }

  async #usernameHandler() {
    clearTimeout(this.usernameTimeout);
    if (this.username.value === this.defaultUsername) {
      this.#setUsernameInputValidity(null);
      return;
    }
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
    if (validity === null) {
      BootstrapUtils.setDefaultInputValidity(this.username);
      this.inputValidUsername = false;
    } else if (validity) {
      BootstrapUtils.setValidInput(this.username);
      this.inputValidUsername = true;
    } else {
      BootstrapUtils.setInvalidInput(this.username);
      this.usernameFeedback.innerHTML = message;
      this.inputValidUsername = false;
    }
    this.#formHandler();
  }

  #emailHandler() {
    clearTimeout(this.emailTimeout);
    if (this.email.value === this.defaultEmail) {
      this.#setEmailInputValidity(null);
      return;
    }
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
    if (validity === null) {
      BootstrapUtils.setDefaultInputValidity(this.email);
      this.inputValidEmail = false;
    } else if (validity) {
      BootstrapUtils.setValidInput(this.email);
      this.inputValidEmail = true;
    } else {
      BootstrapUtils.setInvalidInput(this.email);
      this.emailFeedback.innerHTML = message;
      this.inputValidEmail = false;
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
      this.inputValidPassword = true;
    } else {
      BootstrapUtils.setInvalidInput(this.password);
      this.passwordFeeback.innerHTML = message;
      this.inputValidPassword = false;
    }
    this.#formHandler();
  }

  #setInputConfirmPasswordValidity(validity, message='') {
    if (validity) {
      BootstrapUtils.setValidInput(this.confirmPassword);
      this.inputValidConfirmPassword = true;
    } else {
      BootstrapUtils.setInvalidInput(this.confirmPassword);
      this.confirmPasswordFeedback.innerHTML = message;
      this.inputValidConfirmPassword = false;
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
    if (this.hasChangeAvatar || this.inputValidUsername ||
        this.inputValidEmail ||
        this.defaultHas2FA !== this.twoFASwitch.checked ||
        (this.inputValidPassword && this.inputValidConfirmPassword)) {
      this.saveButton.disabled = false;
    } else {
      this.saveButton.disabled = true;
    }
  }

  async #saveHandler() {
    this.#startLoadButton();
    if (this.hasChangeAvatar) {
      if (!await this.#changeAvatar()) {
        this.#resetLoadButton();
        return;
      }
    }
    if (this.inputValidUsername || this.inputValidEmail ||
        (this.inputValidPassword && this.inputValidConfirmPassword)) {
      const result = await this.#updateInfo();
      if (result === false) {
        this.#resetLoadButton();
        return;
      }
    }
    if (this.defaultHas2FA !== this.twoFASwitch.checked) {
      const result = await this.#update2FA();
      if (result === false) {
        this.#resetLoadButton();
        return;
      }
    }
    window.location.reload();
  }


  async #changeAvatar() {
    if (this.base64Avatar === null) {
      return await this.#deleteAvatar();
    }
    return await this.#updateAvatar();
  }

  async #deleteAvatar() {
    try {
      const {response, body} = await userManagementClient.deleteAvatar(
          userManagementClient.username,
      );
      if (!response.ok) {
        this.alertForm.setAttribute('alert-message', body.errors[0]);
        this.alertForm.setAttribute('alert-type', 'error');
        this.alertForm.setAttribute('alert-display', 'true');
        return false;
      }
      return true;
    } catch (error) {
      ErrorPage.loadNetworkError();
      return false;
    }
  }

  async #updateAvatar() {
    try {
      const {response, body} = await userManagementClient.changeAvatar(
          this.base64Avatar, userManagementClient.username,
      );
      if (!response.ok) {
        this.alertForm.setAttribute('alert-message', body.errors[0]);
        this.alertForm.setAttribute('alert-type', 'error');
        this.alertForm.setAttribute('alert-display', 'true');
        return false;
      }
      return true;
    } catch (error) {
      ErrorPage.loadNetworkError();
      return false;
    }
  }

  async #updateInfo() {
    const newUsername = this.inputValidUsername ? this.username.value: null;
    const newEmail = this.inputValidEmail ? this.email.value: null;
    const newPassword =
      this.inputValidPassword && this.inputValidConfirmPassword ?
      this.password.value: null;
    try {
      const {response, body} = await userManagementClient.updateInfo(
          newUsername, newEmail, newPassword);
      if (response.ok) {
        if (this.inputValidUsername) {
          userManagementClient.username = newUsername;
        }
        return true;
      } else {
        this.alertForm.setAttribute('alert-message', body.errors[0]);
        this.alertForm.setAttribute('alert-type', 'error');
        this.alertForm.setAttribute('alert-display', 'true');
        return false;
      }
    } catch (error) {
      ErrorPage.loadNetworkError();
      return null;
    }
  }

  async #update2FA() {
    if (this.twoFASwitch.checked) {
      return await this.#enable2FA();
    } else {
      return await this.#disable2FA();
    }
  }

  async #enable2FA() {
    try {
      const {response} = await userManagementClient.enable2FA();
      if (response.ok) {
        const result = await response.blob();
        const url = window.URL.createObjectURL(result);
        const settings2FA = document.createElement('settings-2fa-component');
        settings2FA.setAttribute('qr-code', url);
        this.innerHTML = settings2FA.outerHTML;
        return false;
      } else {
        getRouter().navigate('/signin/');
        return false;
      }
    } catch (error) {
      ErrorPage.loadNetworkError();
      return false;
    }
  }

  async #disable2FA() {
    try {
      const {response, body} = await userManagementClient.disable2FA();
      if (response.ok) {
        return true;
      }
      this.alertForm.setAttribute('alert-message', body.errors[0]);
      this.alertForm.setAttribute('alert-type', 'error');
      this.alertForm.setAttribute('alert-display', 'true');
      return false;
    } catch (error) {
      ErrorPage.loadNetworkError();
      return false;
    }
  }

  async #exportHandler(event) {
    event.preventDefault();
    this.exportButton.innerHTML = `
      <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
      <span class="sr-only">Export data</span>
    `;
    this.exportButton.disabled = true;
    try {
      const {response, body} = await userManagementClient.sendUserInfos();
      if (response.ok) {
        this.alertForm.setAttribute(
            'alert-message', 'Data sent to your email.',
        );
        this.alertForm.setAttribute('alert-type', 'success');
        this.alertForm.setAttribute('alert-display', 'true');
      } else {
        this.alertForm.setAttribute('alert-message', body.errors[0]);
        this.alertForm.setAttribute('alert-type', 'error');
        this.alertForm.setAttribute('alert-display', 'true');
      }
      this.exportButton.innerHTML = 'Export data';
      this.exportButton.disabled = false;
    } catch (error) {
      ErrorPage.loadNetworkError();
    }
  }

  async #deleteHandler(event) {
    event.preventDefault();
    this.deleteModal.show();
  }

  async #cancelHandler(event) {
    event.preventDefault();
    this.deleteModal.hide();
  }

  async #deleteAccountHandler(event) {
    event.preventDefault();
    this.deleteAccountButton.innerHTML = `
      <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
      <span class="sr-only">Delete</span>
    `;
    this.deleteAccountButton.disabled = true;
    try {
      const {response, body} = await userManagementClient.deleteAccount();
      if (response.ok) {
        userManagementClient.logout();
        this.deleteModal.hide();
        getRouter().navigate('/signin/');
        return;
      } else {
        this.alertDelete.setAttribute('alert-message', body.errors[0]);
        this.alertForm.setAttribute('alert-type', 'error');
        this.alertDelete.setAttribute('alert-display', 'true');
      }
      this.deleteAccountButton.innerHTML = 'Delete';
      this.deleteAccountButton.disabled = false;
    } catch (error) {
      ErrorPage.loadNetworkError();
    }
  }


  #startLoadButton() {
    this.saveButton.innerHTML = `
      <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
      <span class="sr-only">Loading...</span>
    `;
    this.saveButton.disabled = true;
  }

  #resetLoadButton() {
    this.saveButton.innerHTML = 'Save changes';
    this.saveButton.disabled = false;
  }
}
