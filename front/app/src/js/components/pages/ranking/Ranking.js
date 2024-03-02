import {Component} from '@components';
import {userManagementClient} from '@utils/api';
import {getRouter} from '@js/Router.js';

export class Ranking extends Component {
  constructor() {
    super();
  }
  render() {
    if (!userManagementClient.isAuth()) {
      getRouter().redirect('/signin/');
      return false;
    }
    const pageId = this.getAttribute('pageId');
    return (`
      <navbar-component nav-active="ranking"></navbar-component>
      <friends-sidebar-component main-component="ranking-content-component" ${pageId ? `pageId=${pageId}`: ''}></friends-sidebar-component>
    `);
  }
  style() {
    return (`
      <style>

      </style>
    `);
  }
}
