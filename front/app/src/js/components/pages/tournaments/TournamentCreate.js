import {Component} from '@components';
import {tournamentClient} from '@utils/api';
import {getRouter} from '@js/Router.js';

export class TournamentCreate extends Component {
  constructor() {
    super();
    this.passwordHiden = true;
  }

  render() {
    if (!tournamentClient.isAuth()) {
      getRouter().redirect('/signin/');
      return false;
    }
    return (`
      <navbar-component nav-active="tournaments"></navbar-component>
      <friends-sidebar-component main-component="tournament-create-content-component"></friends-sidebar-component>
    `);
  }
}
