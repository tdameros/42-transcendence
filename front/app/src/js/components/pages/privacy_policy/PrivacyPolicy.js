import {Component} from '@components';
import {userManagementClient} from '@utils/api';

export class PrivacyPolicy extends Component {
  constructor() {
    super();
  }
  render() {
    if (userManagementClient.isAuth()) {
      return (`
      <navbar-component></navbar-component>
      <friends-sidebar-component main-component="privacy-policy-content-component"></friends-sidebar-component>
    `);
    } else {
      return (`
      <navbar-component></navbar-component>
      <privacy-policy-content-component></privacy-policy-content-component>
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
