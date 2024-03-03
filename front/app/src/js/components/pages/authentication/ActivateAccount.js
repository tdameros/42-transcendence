import {Component} from '@components';

export class ActivateAccount extends Component {
  constructor() {
    super();
  }

  render() {
    return (`
      <navbar-component></navbar-component>
      <activate-account-content-component id="${this.getAttribute('id')}" token="${this.getAttribute('token')}">
      </activate-account-content-component>
    `);
  }

  style() {
    return (`
      <style>
      </style>
    `);
  }
}
