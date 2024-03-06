import {Component} from '@components';
import {userManagementClient} from '@utils/api';
import {getRouter} from '@js/Router.js';

export class ConnectedNavbar extends Component {
  constructor() {
    super();
  }

  render() {
    const username = userManagementClient.username;
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
                      <li class="nav-item">
                          ${this.#generateNavLink('local')}
                      </li>
                      <li class="nav-item">
                          ${this.#generateNavLink('multiplayer')}
                      </li>
                      <li class="nav-item">
                          ${this.#generateNavLink('tournaments')}
                      </li>
                      <li class="nav-item">
                          ${this.#generateNavLink('ranking')}
                      </li>
                  </ul>
                  <div class="d-flex align-items-center mb-2 mb-lg-0">
                      <search-nav-component class="me-2"></search-nav-component>
                  </div>
                  <div id="log-part" class="d-flex align-items-center">
                      <theme-button-component class="me-1"></theme-button-component>
                      <friends-button-component class="me-1"></friends-button-component>
                      <notification-nav-component class="me-1"></notification-nav-component>
                      <div class="dropdown mx-2">
                                      <span class="dropdown-toggle" id="dropdownMenuLink"
                                            data-bs-toggle="dropdown" aria-expanded="false">
                                          <img id="nav-profile-img" src="${userManagementClient.getURLAvatar(username)}"
                                               alt="profile image"
                                               class="rounded-circle object-fit-cover"
                                               style="width: 40px; height: 40px;">
                                          <span id="nav-username">@${username}</span>
                                      </span>
                          <ul class="dropdown-menu dropdown-menu-end"
                              aria-labelledby="dropdownMenuLink">
                              <li><a class="dropdown-item"
                                     onclick="window.router.navigate('/profile/${username}/')">Profile</a></li>
                              <li><a class="dropdown-item"
                                     onclick="window.router.navigate('/settings/')">Settings</a></li>
                              <li><a id="logout" class="dropdown-item text-danger">Sign out</a></li>
                          </ul>
                      </div>
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
    this.local = this.querySelector('#local');
    this.multiplayer = this.querySelector('#multiplayer');
    this.tournaments = this.querySelector('#tournaments');
    this.ranking = this.querySelector('#ranking');

    super.addComponentEventListener(this.local, 'click', this.#navigate);
    super.addComponentEventListener(this.multiplayer, 'click', this.#navigate);
    super.addComponentEventListener(this.tournaments, 'click', this.#navigate);
    super.addComponentEventListener(this.ranking, 'click', this.#navigate);

    const disablePaddingTop = this.getAttribute('disable-padding-top');
    if (disablePaddingTop !== 'true') {
      const navbarHeight = this.querySelector('.navbar').offsetHeight;
      document.body.style.paddingTop = navbarHeight + 'px';
    } else {
      document.body.style.paddingTop = '0px';
    }
    const logout = this.querySelector('#logout');
    super.addComponentEventListener(logout, 'click', this.#logout);
  }


  #navigate(event) {
    getRouter().navigate(`/${event.target.id}/`);
  }

  #logout() {
    userManagementClient.logout();
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

  addNotification(notification) {
    const notificationNav = this.querySelector('notification-nav-component');
    if (notificationNav) {
      notificationNav.addNotification(notification);
    }
  }
}
