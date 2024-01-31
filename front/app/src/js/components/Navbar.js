import {Component} from './Component.js';

export class Navbar extends Component {
  constructor() {
    super();
  }

  render() {
    return (`
      <nav class="navbar navbar-expand-lg bg-body-tertiary">
          <div class="container-fluid">
              <a class="navbar-brand">42-Transcendence</a>
              <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
                      data-bs-target="#navbarSupportedContent"
                      aria-controls="navbarSupportedContent" aria-expanded="false"
                      aria-label="Toggle navigation">
                  <span class="navbar-toggler-icon"></span>
              </button>
              <div class="collapse navbar-collapse" id="navbarSupportedContent">
                  <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                      <li class="nav-item">
                          ${this.#generateNavLink('home')}
                      </li>
                      <li class="nav-item">
                          ${this.#generateNavLink('singleplayer')}
                      </li>
                      <li class="nav-item">
                          ${this.#generateNavLink('multiplayer')}
                      </li>
                      <li class="nav-item">
                          ${this.#generateNavLink('tournaments')}
                      </li>
                  </ul>
                  <div class="d-flex mb-2 mb-lg-0">
                      <theme-button-component></theme-button-component>
                      <form class="d-flex" role="search">
                          <input class="form-control ms-2 me-2" type="search"
                                 placeholder="Search" aria-label="Search">
                      </form>
                  </div>
                  <div class="d-flex">
                      ${this.#logNavPart()}
                  </div>
              </div>
          </div>
      </nav>
    `);
  }

  style() {
    return (`
      <style>
      nav {
          box-shadow: rgba(0, 82, 224, 0.1) 0px 6px 12px 0px;
      }

      .navbar {
          position: fixed;
          top: 0;
          width: 100%;
          z-index: 9999;
      }

      .navbar-brand {
          font-family: 'JetBrains Mono Bold', monospace;
      }

      .nav-link {
          font-family: 'JetBrains Mono Light', monospace;
      }
      </style>
    `);
  }

  #logNavPart() {
    if (window.ApiClient.isAuth()) {
      return (this.#logPart());
    }
    return (this.#logOutPart());
  }
  #logPart() {
    return (`
      <div id="log-part"  class="d-flex align-items-center">
          <a class="mx-2">
            <i class="bi bi-bell-fill text-dark-emphasis"></i>
          </a>
          <div class="dropdown mx-2">
              <span class="dropdown-toggle" id="dropdownMenuLink"
                    data-bs-toggle="dropdown" aria-expanded="false">
                  <img id="nav-profile-img" src="/img/tdameros.jpg" alt="profile image"
                       class="rounded-circle"
                       style="width: 40px; height: 40px;">
                  <span id="nav-username">@${localStorage.getItem('username')}</span>
              </span>
              <ul class="dropdown-menu dropdown-menu-end"
                  aria-labelledby="dropdownMenuLink">
                  <li><a class="dropdown-item">Profil</a></li>
                  <li><a class="dropdown-item">Settings</a></li>
                  <li><a id="logout" class="dropdown-item text-danger">Sign out</a></li>
              </ul>
          </div>
      </div>
    `);
  }

  #logOutPart() {
    return (`
      <div id="logout-part" class="d-flex align-items-center">
          <button class="btn btn-outline-success"
                  onclick="window.router.navigate('/signup/')">
              SignUp
          </button>
          <button type="button" class="btn btn-primary ms-2"
                  onclick="window.router.navigate('/signin/')">
              SignIn
          </button>
      </div>
    `);
  }

  postRender() {
    this.home = this.querySelector('#home');
    this.singleplayer = this.querySelector('#singleplayer');
    this.multiplayer = this.querySelector('#multiplayer');
    this.tournaments = this.querySelector('#tournaments');

    super.addComponentEventListener(this.home, 'click', this.#navigate);
    super.addComponentEventListener(this.singleplayer, 'click', this.#navigate);
    super.addComponentEventListener(this.multiplayer, 'click', this.#navigate);
    super.addComponentEventListener(this.tournaments, 'click', this.#navigate);

    const disablePaddingTop = this.getAttribute('disable-padding-top');
    if (disablePaddingTop !== 'true') {
      const navbarHeight = this.querySelector('.navbar').offsetHeight;
      document.body.style.paddingTop = navbarHeight + 'px';
    } else {
      document.body.style.paddingTop = '0px';
    }
    const logout = this.querySelector('#logout');
    if (logout) {
      super.addComponentEventListener(logout, 'click', this.#logout);
    }
  }

  #navigate(event) {
    window.router.navigate(`/${event.target.id}/`);
  }

  #logout() {
    window.ApiClient.logout();
    window.router.navigate('/');
  }

  #generateNavLink(linkId) {
    const activeLink = this.getAttribute('nav-active');
    const navLink = document.createElement('a');
    navLink.setAttribute('id', linkId);
    navLink.classList.add('nav-link');
    if (activeLink === linkId) {
      navLink.classList.add('active');
    }
    navLink.text = linkId.charAt(0).toUpperCase() + linkId.slice(1);
    return (navLink.outerHTML);
  }
}
