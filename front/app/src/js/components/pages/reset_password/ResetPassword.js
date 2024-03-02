import {Component} from '@components';
import {userManagementClient} from '@utils/api';
import {getRouter} from '@js/Router.js';

export class ResetPassword extends Component {
  constructor() {
    super();
  }
  render() {
    if (userManagementClient.isAuth()) {
      getRouter().redirect('/');
      return false;
    }
    return (`
      <navbar-component></navbar-component>
      <div id="container">
        <reset-password-email-component></reset-password-email-component>
     </div>
    `);
  }
}
