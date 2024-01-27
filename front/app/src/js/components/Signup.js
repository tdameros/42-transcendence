import {Component} from './Component.js';
import {InputValidator} from '../utils/InputValidator.js';
import {BootstrapUtils} from '../utils/BootstrapUtils.js';

export class Signup extends Component {
  constructor() {
    super();
    this.passwordHiden = true;
    this.confirmPasswordHiden = true;
  }

  render() {
    return (`
      <navbar-component disable-padding-top="true"></navbar-component>
      <div id="login"
           class="d-flex justify-content-center align-items-center rounded-3">
          <div class="login-card card m-3">
              <div class="card-body m-2">
                  <h2 class="card-title text-center m-5">Sign up</h2>
                  <form>
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
                              <div class="invalid-feedback">
                                  Passwords do not match.
                              </div>
                          </div>
                      </div>
                      <div class="d-flex mb-3">
                          <a id="have-account">Already have an account?</a>
                      </div>
                  </form>
                  <div class="row d-flex justify-content-center">
                      <button type="submit" class="btn btn-primary">Sign up</button>
                  </div>
                  <hr class="my-4">
                  <div class="row">
                      <button id="github-btn" class="btn btn-lg mb-2" type="submit">
                          <svg xmlns="http://www.w3.org/2000/svg" width="24"
                               height="24" fill="currentColor" class="bi bi-github"
                               viewBox="0 0 16 16">
                              <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>
                          </svg>
                          Sign up with Github
                      </button>
                      <button id="intra-btn" class="btn btn-lg btn-outline-dark mb-2"
                              type="submit">
                          <svg xmlns:dc="http://purl.org/dc/elements/1.1/"
                               xmlns:cc="http://creativecommons.org/ns#"
                               xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                               xmlns:svg="http://www.w3.org/2000/svg"
                               xmlns="http://www.w3.org/2000/svg"
                               xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
                               xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
                               version="1.1" id="Calque_1" x="0px" y="0px"
                               viewBox="0 0 137.6 96.599998"
                               enable-background="new 0 0 595.3 841.9"
                               xml:space="preserve" inkscape:version="0.48.2 r9819"
                               width="24" height="24" sodipodi:docname="42_logo.svg"><script xmlns=""/>
                              <metadata id="metadata17"><rdf:RDF><cc:Work rdf:about=""><dc:format>image/svg+xml</dc:format><dc:type
                                      rdf:resource="http://purl.org/dc/dcmitype/StillImage"/></cc:Work></rdf:RDF></metadata>
                              <defs id="defs15"/>
                              <sodipodi:namedview pagecolor="#ffffff"
                                                  bordercolor="#666666"
                                                  borderopacity="1"
                                                  objecttolerance="10"
                                                  gridtolerance="10"
                                                  guidetolerance="10"
                                                  inkscape:pageopacity="0"
                                                  inkscape:pageshadow="2"
                                                  inkscape:window-width="1060"
                                                  inkscape:window-height="811"
                                                  id="namedview13" showgrid="false"
                                                  fit-margin-top="0"
                                                  fit-margin-left="0"
                                                  fit-margin-right="0"
                                                  fit-margin-bottom="0"
                                                  inkscape:zoom="0.39642998"
                                                  inkscape:cx="68.450005"
                                                  inkscape:cy="48.350011"
                                                  inkscape:window-x="670"
                                                  inkscape:window-y="233"
                                                  inkscape:window-maximized="0"
                                                  inkscape:current-layer="Calque_1"/>
                              <g id="g3" transform="translate(-229.2,-372.70002)">
                                  <polygon
                                          points="229.2,443.9 279.9,443.9 279.9,469.3 305.2,469.3 305.2,423.4 254.6,423.4 305.2,372.7 279.9,372.7 229.2,423.4 "
                                          id="polygon5"/>
                                  <polygon
                                          points="316.1,398.1 341.4,372.7 316.1,372.7 "
                                          id="polygon7"/>
                                  <polygon
                                          points="341.4,398.1 316.1,423.4 316.1,448.7 341.4,448.7 341.4,423.4 366.8,398.1 366.8,372.7 341.4,372.7 "
                                          id="polygon9"/>
                                  <polygon
                                          points="366.8,423.4 341.4,448.7 366.8,448.7 "
                                          id="polygon11"/>
                              </g>
                          </svg>
                          Sign up with 42 Intra
                      </button>
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
      
      #login {
          height: 100vh;
      }
      
      .login-card {
          width: 550px;
      }
      
      #github-btn {
          background-color: #000000;
          color: #ffffff;
      }
      
      #github-btn:hover {
          background-color: #252525;
          color: #ffffff;
      }
      
      #intra-btn {
          background-color: #ffffff;
          color: #000000;"
      }
      
      
      #intra-btn:hover {
          background-color: #f6f6f6;
          color: #000000;"
      }
      
      .form-group mb-4 {
          display: flex;
          align-items: center;
      }
      
      #password-feedback {
          white-space: pre-line;
          word-wrap: break-word;
      }
      
      .eye-box:hover {
          background: #efefef;
          color: #2d2d2d;
      }
      
      .invalid-feedback p {
          margin: 0;
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
    super.addComponentEventListener(this.confirmPassword, 'input',
        this.#confirmPasswordHandler);
    super.addComponentEventListener(this.confirmPasswordEyeIcon, 'click',
        this.#toggleConfirmPasswordVisibility);

    this.haveAccount = this.querySelector('#have-account');
    super.addComponentEventListener(this.haveAccount, 'click', () =>
      window.router.navigate('/signin/'),
    );
  }

  #usernameHandler() {
    const {validity, missingRequirements} =
      InputValidator.isValidUsername(this.username.value);
    if (validity) {
      BootstrapUtils.setValidInput(this.username);
    } else {
      BootstrapUtils.setInvalidInput(this.username);
      this.usernameFeedback.innerHTML = missingRequirements[0];
    }
  }

  #emailHandler() {
    const {validity, missingRequirements} =
      InputValidator.isValidEmail(this.email.value);
    if (validity) {
      BootstrapUtils.setValidInput(this.email);
    } else {
      BootstrapUtils.setInvalidInput(this.email);
      this.emailFeedback.innerHTML = missingRequirements[0];
    }
  }
  #passwordHandler() {
    const {validity, missingRequirements} =
      InputValidator.isValidSecurePassword(this.password.value);
    if (validity) {
      BootstrapUtils.setValidInput(this.password);
    } else {
      BootstrapUtils.setInvalidInput(this.password);
      this.passwordFeeback.innerHTML = missingRequirements[0];
    }
    if (this.confirmPassword.value.length !== 0) {
      this.#confirmPasswordHandler();
    }
  }

  #confirmPasswordHandler() {
    if (this.confirmPassword.value === this.password.value) {
      BootstrapUtils.setValidInput(this.confirmPassword);
    } else {
      BootstrapUtils.setInvalidInput(this.confirmPassword);
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
}

export default {Signup};
