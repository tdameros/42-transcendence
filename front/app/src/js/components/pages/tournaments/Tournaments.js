import {Component} from '@components';
import {ErrorPage} from '@utils/ErrorPage.js';
import {Cookies} from '@js/Cookies.js';
import {tournamentClient} from '@utils/api';
import {getRouter} from '@js/Router.js';
import {TournamentsList} from './TournamentsList.js';

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
      <div class="container-fluid">
        <div class="row">
          <div class="col-md-6">
            <tournaments-list-component display-mode="placeholder"></tournaments-list-component>
          </div>
          <div class="col-md-6">
            <tournament-details-component></tournament-details-component>
          </div>
        </div>
      </div>
    `);
  }

  async postRender() {
    this.tournamentsListComponent = document.querySelector(
        'tournaments-list-component',
    );
    this.tournamentBracketComponent = document.querySelector(
        'tournament-bracket-component',
    );
    this.tournamentDetailsComponent = document.querySelector(
        'tournament-details-component',
    );
    this.privateCheckBox = this.querySelector(`#${
      TournamentsList.privateCheckBoxId
    }`);
    this.finishedCheckBox = this.querySelector(`#${
      TournamentsList.finishedCheckBoxId
    }`);
    super.addComponentEventListener(this.privateCheckBox, 'change',
        this.#privateCheckBoxHandler);
    super.addComponentEventListener(this.finishedCheckBox, 'change',
        this.#finishedCheckBoxHandler);
    this.tournamentsListSelectedRow = null;
    this.tournaments = [];
    this.#updateTournamentsList();
  }

  #privateCheckBoxHandler() {
    Cookies.add(TournamentsList.privateCheckBoxCookie,
        this.privateCheckBox.checked);
    this.#updateTournamentsList();
  }

  #finishedCheckBoxHandler() {
    Cookies.add(TournamentsList.finishedCheckBoxCookie,
        this.finishedCheckBox.checked);
    this.#updateTournamentsList();
  }

  async #updateTournamentsList() {
    this.displayPrivateTournaments = Cookies.get(
        TournamentsList.privateCheckBoxCookie) === 'true';
    this.dispayFinishedTournaments = Cookies.get(
        TournamentsList.finishedCheckBoxCookie) === 'true';
    try {
      const {response, body} = await tournamentClient.getTournaments(this.id,
          10,
          this.displayPrivateTournaments,
          this.dispayFinishedTournaments);
      if (response.ok) {
        this.tournaments = body.tournaments;
        this.tournamentsListComponent.updateTournamentsList(body.tournaments,
            body.page, body['nb-pages']);
        this.#addRowsEventListeners();
      } else {
        getRouter().redirect('/signin/');
      }
    } catch (error) {
      ErrorPage.loadNetworkError();
    }
  }

  style() {
    return (`
      <style>

      </style>
    `);
  }

  #selectTournamentHandler(event) {
    if (this.tournamentsListSelectedRow !== null) {
      this.tournamentsListSelectedRow.classList.remove('table-active');
    }
    let currentRow = event.target;
    while (currentRow.nodeName !== 'TR' && currentRow.nodeName !== 'HTML') {
      currentRow = currentRow.parentNode;
    }
    if (currentRow.nodeName === 'TR') {
      currentRow.classList.add('table-active');
    }
    this.tournamentsListSelectedRow = currentRow;
    const tournamentId = parseInt(
        this.tournamentsListSelectedRow.getAttribute('tournament-id'),
    );
    this.tournamentDetailsComponent.loadTournamentDetails(tournamentId);
  }

  #addRowsEventListeners() {
    this.rows = this.querySelectorAll('.tournament-row');
    this.rows.forEach((row) => {
      super.addComponentEventListener(row, 'click',
          this.#selectTournamentHandler);
    });
    if (this.rows.length > 0) {
      this.rows[0].click();
    } else {
      this.tournamentDetailsComponent.loadNoTournament();
    }
  }
}
