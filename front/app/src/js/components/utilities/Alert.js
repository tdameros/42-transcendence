import {Component} from '../Component.js';

export class Alert extends Component {
  static get observedAttributes() {
    return ['alert-message', 'alert-display'];
  }

  constructor() {
    super();
  }
  render() {
    this.message = this.getAttribute('alert-message');
    this.display = this.getAttribute('alert-display');
    if (this.display === 'true') {
      return (`
      <div class="alert alert-danger alert-dismissible fade show"
           role="alert">
        <p class="alert-content alert-form">${this.message}</p>
        <button id="alert-form" type="button" class="btn-close alert-content" data-bs-dismiss="alert"
                aria-label="Close"></button>
      </div>`);
    }
    return ('');
  }
  style() {
    return (`
      <style>
      .alert-content {
        margin-top: -0.5rem;
        margin-bottom: -0.5rem;
      }
      </style>
    `);
  }
}
