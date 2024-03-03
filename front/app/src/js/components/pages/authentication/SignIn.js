import {Component} from '@components';
import {userManagementClient} from '@utils/api';
import {getRouter} from '@js/Router.js';

export class SignIn extends Component {
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
      <signin-content-component></signin-content-component>
    `);
  }

  style() {
    return (`
    `);
  }
}
