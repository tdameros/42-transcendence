import {Component} from '@components';
import {userManagementClient} from '@utils/api';
import {getRouter} from '@js/Router.js';

export class SignUp extends Component {
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
      <signup-content-component></signup-content-component>
    `);
  }
  style() {
    return (`
    `);
  }
}
