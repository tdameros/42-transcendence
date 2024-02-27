import {Component} from '@components';
import {userManagementClient} from '@utils/api';

export class Navbar extends Component {
  constructor() {
    super();
  }

  render() {
    const navActive = this.getAttribute('nav-active');
    if (userManagementClient.isAuth()) {
      return (`<connected-navbar-component nav-active="${navActive}"></connected-navbar-component>`);
    }
    return (`<disconnected-navbar-component nav-active="${navActive}"></disconnected-navbar-component>`);
  }

  style() {
    return (`
      <style>
      .navbar {
          position: fixed;
          top: 0;
          width: 100%;
          z-index: 9999;
          box-shadow: rgba(0, 82, 224, 0.1) 0px 6px 12px 0px;
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

  postRender() {
    const disablePaddingTop = this.getAttribute('disable-padding-top');
    if (disablePaddingTop !== 'true') {
      const navbarHeight = this.querySelector('.navbar').offsetHeight;
      document.body.style.paddingTop = navbarHeight + 'px';
    } else {
      document.body.style.paddingTop = '0px';
    }
  }

  hideCollapse() {
    const navbarToggler = this.querySelector('.navbar-toggler');
    const navbarToggleDisplay = window.getComputedStyle(navbarToggler)
        .getPropertyValue('display');
    if (navbarToggleDisplay !== 'none') {
      navbarToggler.click();
    }
  }

  get height() {
    return this.querySelector('.navbar').offsetHeight;
  }

  addNotification(notification) {
    const notificationNav = this.querySelector('notification-nav-component');
    notificationNav.addNotification(notification);
  }
}
