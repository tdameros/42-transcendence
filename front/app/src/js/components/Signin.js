import {Component} from './Component.js';
import {Cookies} from '../Cookies.js';

export class Signin extends Component {
  constructor() {
    super();
  }

  render() {
    return (`
      <navbar-component disable-padding-top="true"></navbar-component>
      <div id="login"
           class="d-flex justify-content-center align-items-center rounded-3">
          <div class="login-card card m-3">
              <div class="card-body m-2">
                  <h2 class="card-title text-center m-5">Sign in</h2>
                  <form id="signin-form">
                      <div class="form-group mb-4">
                          <input type="email" class="form-control" id="email"
                                 placeholder="Email">
                          <div id="email-feedback" class="invalid-feedback">
                              Please enter a valid email.
                          </div>
                      </div>
                      <div class="form-group mb-4">
                          <input type="password" class="form-control" id="password"
                                 placeholder="Password">
                      </div>
                      <div class="d-flex justify-content-between mb-3">
                          <a id="dont-have-account">Don't have an account?</a>
                          <a id="forgot-password">Forgot pasword?</a>
                      </div>
                      <div class="row d-flex justify-content-center">
                          <button id="signin-btn" class="btn btn-primary">Sign in
                          </button>
                      </div>
                  </form>
                  <hr class="my-4">
                  <div class="row">
                      <button id="github-btn" class="btn btn-lg mb-2" type="submit">
                          <svg xmlns="http://www.w3.org/2000/svg" width="24"
                               height="24" fill="currentColor" class="bi bi-github"
                               viewBox="0 0 16 16">
                              <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>
                          </svg>
                          Sign in with Github
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
                          Sign in with 42 Intra
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
          color: #000000;
      "
      }
      
      
      #intra-btn:hover {
          background-color: #f6f6f6;
          color: #000000;
      "
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
      
      #forgot-password, #dont-have-account {
          font-size: 13px;
          color: rgb(13, 110, 253);
      }
      </style>
    `);
  }

  postRender() {
    this.forgotPassword = this.querySelector('#forgot-password');
    this.donthaveAccount = this.querySelector('#dont-have-account');
    this.signinBtn = this.querySelector('#signin-btn');
    this.signinForm = this.querySelector('#signin-form');
    super.addComponentEventListener(this.forgotPassword, 'click', () => {
      window.router.navigate('/reset-password/');
    });
    super.addComponentEventListener(this.donthaveAccount, 'click', () => {
      window.router.navigate('/signup/');
    });
    super.addComponentEventListener(this.signinBtn, 'click', (event) => {
      event.preventDefault();
      this.#signin();
    });
    super.addComponentEventListener(this.signinForm, 'submit', (event) => {
      event.preventDefault();
      this.#signin();
    });
  }

  #signin() {
    Cookies.add('jwt', 'jwt');
    window.router.navigate('/');
  }
}

export default {Signin};