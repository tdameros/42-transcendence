import {Component} from '@components';

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
    this.type = this.getAttribute('alert-type');
    const alertColorClass = this.type === 'success' ?
      'alert-success' : 'alert-danger';
    if (this.display === 'true' ) {
      return (`
      <div class="alert ${alertColorClass} alert-dismissible fade show"
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
