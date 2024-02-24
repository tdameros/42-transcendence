import {Component} from '../../Component.js';
import {userManagementClient} from '@utils/api/index.js';
import {getRouter} from '@js/Router.js';

export class UserProfile extends Component {
  constructor() {
    super();
  }

  render() {
    if (!userManagementClient.isAuth()) {
      getRouter().redirect('/signin/');
      return false;
    }
    return (`
      <navbar-component></navbar-component>
      <friends-sidebar-component main-component="user-profile-content-component" username="${this.getAttribute('username')}"></friends-sidebar-component>
    `);
  }
}
