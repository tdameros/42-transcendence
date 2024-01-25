import {Component} from './Component.js';

export class ResetPassword extends Component {
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
                  <h2 class="card-title text-center m-5">Reset password</h2>
                  <form>
                      <div class="d-flex justify-content-center mb-4">
                          <i class="bi bi-envelope-at-fill"
                             style="font-size: 7rem;"></i>
                      </div>
                      <div class="form-group mb-4">
                          <input type="email" class="form-control" id="email"
                                 placeholder="Email">
                      </div>
                  </form>
                  <div class="row d-flex justify-content-center">
                      <button type="submit" class="btn btn-primary">Send code</button>
                  </div>
              </div>
          </div>
      </div>
    `);
  }
  style() {
    return (`
      <style>
      #email-icon {
          color: var(--bs-emphasis-color);
      }
  
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
      </style>
    `);
  }
}

export default {ResetPassword};
