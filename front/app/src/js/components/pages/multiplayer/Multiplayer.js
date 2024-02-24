import {Component} from '@components';
import {userManagementClient} from '@utils/api/index.js';
import {getRouter} from '@js/Router.js';

export class Multiplayer extends Component {
  constructor() {
    super();
  }
  render() {
    if (!userManagementClient.isAuth()) {
      getRouter().redirect('/signin/');
      return false;
    }
    return (`
      <navbar-component nav-active="multiplayer"></navbar-component>
      <friends-sidebar-component main-component="multiplayer-content-component"></friends-sidebar-component>
  `);
  }

  style() {
    return (`
      <style>
      </style>
    `);
  }
}
