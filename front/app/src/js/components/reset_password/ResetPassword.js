import {Component} from '../Component.js';

export class ResetPassword extends Component {
  constructor() {
    super();
  }
  render() {
    return (`
      <navbar-component disable-padding-top="true"></navbar-component>
      <div id="container">
        <reset-password-email-component></reset-password-email-component>
     </div>
    `);
  }
}
