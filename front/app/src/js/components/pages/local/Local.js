import {Component} from '@components';
import {userManagementClient} from '@utils/api/index.js';
import {getRouter} from '@js/Router.js';

export class Local extends Component {
  constructor() {
    super();
  }
  render() {
    if (!userManagementClient.isAuth()) {
      getRouter().redirect('/signin/');
      return false;
    }
    return (`
      <navbar-component nav-active="local"></navbar-component>
      <friends-sidebar-component main-component="local-content-component"></friends-sidebar-component>
    `);
  }
  style() {
    return (`
      <style>

      </style>
    `);
  }
}
