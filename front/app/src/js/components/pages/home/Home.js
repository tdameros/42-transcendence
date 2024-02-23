import {Component} from '@components';
import {userManagementClient} from '@utils/api';

export class Home extends Component {
  constructor() {
    super();
  }
  render() {
    if (userManagementClient.isAuth()) {
      return (`
      <navbar-component nav-active="home"></navbar-component>
      <friends-sidebar-component main-component="home-content-component"></friends-sidebar-component>
    `);
    } else {
      return (`
        <navbar-component nav-active="home"></navbar-component>
        <home-content-component></home-content-component>
      `);
    }
  }
  style() {
    return (`
      <style>

      </style>
    `);
  }
}
