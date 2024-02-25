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
    return (`
      <navbar-component nav-active="tournaments"></navbar-component>
      <friends-sidebar-component main-component="tournaments-content-component" username="${this.getAttribute('id')}"></friends-sidebar-component>
    `);
  }
}
