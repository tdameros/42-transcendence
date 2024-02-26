import {Component} from '@components';

export class DisconnectedNavbar extends Component {
  constructor() {
    super();
  }

  render() {
    return (`
      <nav id="main-navbar" class="navbar navbar-expand-lg bg-body-tertiary">
          <div class="container-fluid">
              <a class="navbar-brand" onclick="window.router.navigate('/')">Transcendence</a>
              <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
                      data-bs-target="#navbarSupportedContent"
                      aria-controls="navbarSupportedContent" aria-expanded="false"
                      aria-label="Toggle navigation">
                  <span class="navbar-toggler-icon"></span>
              </button>
              <div class="collapse navbar-collapse" id="navbarSupportedContent">
                  <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                  </ul>
                  <div class="d-flex align-items-center">
                      <theme-button-component class="me-2"></theme-button-component>
                      <button class="btn btn-outline-success"
                              onclick="window.router.navigate('/signup/')">
                          Sign up
                      </button>
                      <button type="button" class="btn btn-primary ms-2"
                              onclick="window.router.navigate('/signin/')">
                          Sign in
                      </button>
                  </div>
              </div>
          </div>
      </nav>
    `);
  }

  style() {
    return (`
      <style>
      </style>
    `);
  }

  postRender() {
  }

  addNotification(notification) {
    const notificationNav = this.querySelector('notification-nav-component');
    notificationNav.addNotification(notification);
  }
}
