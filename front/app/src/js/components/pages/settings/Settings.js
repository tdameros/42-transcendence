import {Component} from '@components';
import {userManagementClient} from '@utils/api';
import {getRouter} from '@js/Router.js';

export class Settings extends Component {
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
      <friends-sidebar-component main-component="settings-content-component"></friends-sidebar-component>
    `);
  }
}
