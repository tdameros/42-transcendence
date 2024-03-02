import {Component} from '@components';
import {tournamentClient} from '@utils/api';
import {getRouter} from '@js/Router.js';

export class Tournaments extends Component {
  constructor() {
    super();
  }


  render() {
    if (!tournamentClient.isAuth()) {
      getRouter().redirect('/signin/');
      return false;
    }
    const pageId = this.getAttribute('pageId');
    return (`
      <navbar-component nav-active="tournaments"></navbar-component>
      <friends-sidebar-component main-component="tournaments-content-component" ${pageId ? `pageId=${pageId}`: ''}>
      </friends-sidebar-component>
    `);
  }
}
