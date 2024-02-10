import {Component} from '@components';
import {Theme} from '@js/Theme.js';

export class ThemeButton extends Component {
  constructor() {
    super();
  }

  render() {
    const theme = Theme.get();
    const btnClass = theme === 'light' ?
      'btn-outline-dark' : 'btn-outline-light';
    return (`
      <button id="switch-btn" class="btn ${btnClass}" type="button">
          <svg xmlns="http://www.w3.org/2000/svg" width="16"
               height="16" fill="currentColor" class="bi bi-moon-fill"
               viewBox="0 0 16 16">
              <path d="M6 .278a.768.768 0 0 1 .08.858 7.208 7.208 0 0 0-.878 3.46c0 4.021 3.278 7.277 7.318 7.277.527 0 1.04-.055 1.533-.16a.787.787 0 0 1 .81.316.733.733 0 0 1-.031.893A8.349 8.349 0 0 1 8.344 16C3.734 16 0 12.286 0 7.71 0 4.266 2.114 1.312 5.124.06A.752.752 0 0 1 6 .278z"/>
          </svg>
      </button>
    `);
  }

  style() {
    return (`
      <style>

      </style>
    `);
  }

  postRender() {
    this.switchBtn = this.querySelector('#switch-btn');
    super.addComponentEventListener(this.switchBtn, 'click', this.#switchTheme);
  }

  #switchTheme() {
    if (Theme.get() === 'light') {
      Theme.set('dark');
    } else {
      Theme.set('light');
    }
    this.switchBtn.classList.toggle('btn-outline-light');
    this.switchBtn.classList.toggle('btn-outline-dark');
  }
}
