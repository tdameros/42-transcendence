import {Component} from '@components';
import {Theme} from '@js/Theme.js';
import {NavbarUtils} from '@utils/NavbarUtils.js';

export class ThemeButton extends Component {
  constructor() {
    super();
  }

  render() {
    let classIcon = '';
    if (Theme.get() === 'light') {
      classIcon = 'bi-moon-fill';
    } else {
      classIcon = 'bi-sun-fill';
    }
    return (`
      <div class="btn icon-btn d-flex justify-content-center align-items-center">
        <i class="bi ${classIcon} fs-5"></i>
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
    super.addComponentEventListener(this, 'click', this.#switchTheme);
  }

  #switchTheme() {
    if (Theme.get() === 'light') {
      Theme.set('dark');
    } else {
      Theme.set('light');
    }
    this.icon.classList.toggle('bi-moon-fill');
    this.icon.classList.toggle('bi-sun-fill');
    NavbarUtils.hideCollapse();
  }
}
