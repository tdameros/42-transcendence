import {Component} from '@components';
import {NavbarUtils} from '@utils/NavbarUtils.js';

export class FriendsButton extends Component {
  constructor() {
    super();
  }

  render() {
    return (`
      <div class="btn icon-btn d-flex justify-content-center align-items-center">
        <i class="bi bi-people-fill fs-5"></i>
      </div>
    `);
  }

  style() {
    return (`
      <style>
      .icon-btn {
         cursor: pointer;
         padding: 0.16rem 0.6rem;
      }
      
      .icon-btn:hover {
        background-color: var(--bs-body-bg);
        border: var(--bs-border-width) solid var(--bs-border-color);
      }
      
      .icon-btn:active {
        border-color: var(--bs-border-color)!important;
      }
      </style>
    `);
  }

  postRender() {
    this.icon = this.querySelector('i');
    super.addComponentEventListener(this, 'click', this.#switchFriends);
  }

  #switchFriends() {
    const sidebar = document.querySelector('friends-sidebar-component');
    if (sidebar) {
      sidebar.toggleVisibility();
      NavbarUtils.hideCollapse();
    }
  }
}
