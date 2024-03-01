import {Component} from '@components';

export class Error extends Component {
  constructor() {
    super();
  }
  render() {
    return (`
      <navbar-component></navbar-component>
      <error-content-component refresh="${this.getAttribute('refresh')}" message="${this.getAttribute('message')}"></error-content-component>
    `);
  }
  style() {
    return (`
    `);
  }
}
