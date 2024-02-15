import {Component} from '@components';
import {userManagementClient} from '@utils/api/index.js';
import {getRouter} from '@js/Router.js';

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
                      <div class="position-relative z-1 me-2 ms-2">
                        <form id="search-form" class="d-flex" role="search">
                            <input id="search-bar" class="form-control" type="search"
                                   placeholder="Search" aria-label="Search" autocomplete="off">
                        </form>
                        <div id="search-results" class="rounded">
                        </div>
                      </div>

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
        #search-results {
            position: absolute;
            width: 100%;
            background-color: white;
            border: 1px solid #ddd;
            max-height: 200px;
            overflow-y: auto;
            display: none;
            z-index: 2; /* Pour que les suggestions apparaissent au-dessus du contenu */
        }

        .result-item {
            padding: 10px;
            cursor: pointer;
        }

        .result-item:hover {
            background-color: #f4f4f4;
        }
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
    if (userManagementClient.isAuth()) {
      return (this.#logPart());
    }
    return (this.#logOutPart());
  }
  #logPart() {
    const username = userManagementClient.username;
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
                  <span id="nav-username">@${username}</span>
              </span>
              <ul class="dropdown-menu dropdown-menu-end"
                  aria-labelledby="dropdownMenuLink">
                  <li><a class="dropdown-item" onclick="window.router.navigate('/profile/${username}/')">Profil</a></li>
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
    this.searchBar = this.querySelector('#search-bar');
    if (this.searchBar) {
      super.addComponentEventListener(
          this.searchBar, 'input', this.#searchBarHandler,
      );
      super.addComponentEventListener(
          document, 'click', this.#DOMClickHandler,
      );
    }
    this.searchResults = this.querySelector('#search-results');
    this.searchForm = this.querySelector('#search-form');
    if (this.searchForm) {
      super.addComponentEventListener(
          this.searchForm, 'submit', this.#searchFormHandler,
      );
    }
  }

  async #searchBarHandler(event) {
    if (event.target.value.length < 3) {
      this.searchResults.style.display = 'none';
      return;
    }
    try {
      const {response, body} = await userManagementClient.searchUsername(
          event.target.value,
      );
      this.searchResults.innerHTML = '';
      if (response.ok) {
        this.searchResults.innerHTML = this.#renderSearchResults(body['users']);
        if (body['users'].length > 0) {
          this.searchResults.style.display = 'block';
        } else {
          this.searchResults.style.display = 'none';
        }
      }
    } catch (error) {
      ;
    }
  }

  #renderSearchResults(users) {
    return (users.slice(0, 3).map((username) => {
      return (`
      <div class="result-item p-1" onclick="window.router.navigate('/profile/${username}/')" username="${username}">
        <img src="/img/tdameros.jpg" alt="profile image" class="rounded-circle" style="width: 40px; height: 40px;">
        ${username}
      </div>
    `);
    }).join(''));
  }

  #DOMClickHandler(event) {
    if (this.searchResults &&
      !this.searchResults.contains(event.target) &&
      event.target !== this.searchBar) {
      this.searchResults.style.display = 'none';
    }
  }

  #searchFormHandler(event) {
    event.preventDefault();
    const username = this.searchBar.value;
    if (username.length > 0) {
      getRouter().navigate(`/profile/${username}/`);
    }
  }


  #navigate(event) {
    getRouter().navigate(`/${event.target.id}/`);
  }

  #logout() {
    userManagementClient.logout();
    getRouter().navigate('/');
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
