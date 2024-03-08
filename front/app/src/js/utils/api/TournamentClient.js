import {BaseApiClient} from './BaseClient.js';

export class TournamentClient extends BaseApiClient {
  static URL = `https://${window.location.hostname}:6001`;

  static URIs = {
    'tournaments': 'tournament/',
    'tournament': 'tournament/:id/',
    'tournament-matches': 'tournament/:id/matches/',
    'tournament-join': 'tournament/:id/players/',
    'tournament-delete': 'tournament/:id/',
    'tournament-start': 'tournament/:id/start/',
    'generate-matches': 'tournament/:id/matches/generate/',
    'tournament-create': 'tournament/',
    'tournament-leave': 'tournament/:id/players/',
  };

  constructor() {
    super();
    this.URL = TournamentClient.URL;
    this.URIs = TournamentClient.URIs;
  }

  async leaveTournament(tournamentId) {
    const URI = this.URIs['tournament-leave'].replace(':id', tournamentId);
    const URL = `${this.URL}/${URI}`;
    return await this.deleteAuthRequest(URL);
  }

  async createTournament(name, maxPlayers, isPrivate, password) {
    const body = {
      'name': name,
      'max-players': maxPlayers,
      'is-private': isPrivate,
    };
    if (isPrivate) {
      body.password = password;
    }
    const URL = `${this.URL}/${this.URIs['tournament-create']}`;
    return await this.postAuthRequest(URL, body);
  }

  async generateMatches(tournamentId, random=true) {
    const body = {
      'random': random,
    };
    const URI = this.URIs['generate-matches'].replace(':id', tournamentId);
    const URL = `${this.URL}/${URI}`;
    return await this.postAuthRequest(URL, body);
  }

  async startTournament(tournamentId) {
    const URI = this.URIs['tournament-start'].replace(':id', tournamentId);
    const URL = `${this.URL}/${URI}`;
    return await this.patchAuthRequest(URL);
  }

  async deleteTournament(tournamentId) {
    const URI = this.URIs['tournament-delete'].replace(':id', tournamentId);
    const URL = `${this.URL}/${URI}`;
    return await this.deleteAuthRequest(URL);
  }

  async joinTournament(tournamentId, nickname, password) {
    const body = {
      nickname: nickname,
      password: password,
    };
    const URI = this.URIs['tournament-join'].replace(':id', tournamentId);
    const URL = `${this.URL}/${URI}`;
    return await this.postAuthRequest(URL, body);
  }

  async getTournament(tournamentId) {
    const URI = this.URIs['tournament'].replace(':id', tournamentId);
    const URL = `${this.URL}/${URI}`;
    return await this.getAuthRequest(URL);
  }

  async getTournamentMatches(tournamentId) {
    const URI = this.URIs['tournament-matches'].replace(':id', tournamentId);
    const URL = `${this.URL}/${URI}`;
    return await this.getAuthRequest(URL);
  }

  async getTournaments(page, pageSize=10,
      displayPrivate=false,
      displayFinished=false) {
    const params = {
      'page': page,
      'page-size': pageSize,
      ...(displayPrivate && {'display-private': ''}),
      ...(displayFinished && {'display-completed': ''}),
    };
    const URL = `${this.URL}/${this.URIs['tournaments']}`;
    return await this.getAuthRequest(URL, params);
  }
}
