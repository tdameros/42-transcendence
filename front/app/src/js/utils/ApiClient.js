import {JSONRequests} from './JSONRequests.js';
import {JWT} from './JWT.js';

export class ApiClient {
  static userManagement = 'user-management';
  static tournament = 'tournament';

  static microservicesURLs = {
    'user-management': `http://${window.location.hostname}:6002`,
    'tournament': `http://${window.location.hostname}:6001`,
  };

  static userManagementURIs = {
    'signin': 'user/signin/',
    'signup': 'user/signup/',
    'username-exist': 'user/username-exist/',
    'email-exist': 'user/email-exist/',
    'forgot-password-send-code': 'user/forgot-password/send-code/',
    'refresh-access-token': 'user/refresh-access-jwt/',
  };

  static tournamentURIs = {
    'tournaments': 'tournament/',
    'tournament': 'tournament/:id/',
    'tournament-matches': 'tournament/:id/matches/',
    'tournament-join': 'tournament/:id/players/',
    'tournament-delete': 'tournament/:id/',
    'tournament-start': 'tournament/:id/start/',
    'generate-matches': 'tournament/:id/matches/generate/',
    'tournament-create': 'tournament/',
  };

  constructor() {
    this.accessToken = new JWT(null);
  }

  async authRequired() {
    if (this.refreshToken === null) {
      return false;
    }
    if (!this.accessToken.isValid()) {
      const isRefresh = await this.refreshAccessToken();
      if (!isRefresh) {
        return false;
      }
    }
    return true;
  }

  async refreshAccessToken() {
    const requestBody = {
      refresh_token: this.refreshToken,
    };
    const {response, body} = await ApiClient.post(
        ApiClient.userManagement,
        ApiClient.userManagementURIs['refresh-access-token'],
        requestBody);
    if (response.ok) {
      this.accessToken = new JWT(body.access_token);
      return true;
    } else {
      this.logout();
      return false;
    }
  }

  get userId() {
    return new JWT(this.refreshToken).payload.user_id;
  }

  async createTournament(name, maxPlayers, isPrivate, password) {
    const auth = await this.authRequired();
    if (!auth) {
      return {response: {ok: false, status: 401}, body: {}};
    }
    const headers = {
      'Authorization': this.accessToken.jwt,
    };
    const body = {
      'name': name,
      'max-players': maxPlayers,
      'is-private': isPrivate,
    };
    if (isPrivate) {
      body.password = password;
    }
    return await ApiClient.post(ApiClient.tournament,
        ApiClient.tournamentURIs['tournament-create'], body, headers);
  }

  async generateMatches(tournamentId) {
    const auth = await this.authRequired();
    if (!auth) {
      return {response: {ok: false, status: 401}, body: {}};
    }
    const headers = {
      'Authorization': this.accessToken.jwt,
    };
    const URI = ApiClient.tournamentURIs[
        'generate-matches'
    ].replace(':id', tournamentId);
    return await ApiClient.post(ApiClient.tournament,
        URI, {'random': true}, headers);
  }

  async startTournament(tournamentId) {
    const auth = await this.authRequired();
    if (!auth) {
      return {response: {ok: false, status: 401}, body: {}};
    }
    const headers = {
      'Authorization': this.accessToken.jwt,
    };
    const URI = ApiClient.tournamentURIs[
        'tournament-start'
    ].replace(':id', tournamentId);
    return await ApiClient.patch(ApiClient.tournament,
        URI, {}, headers);
  }

  async deleteTournament(tournamentId) {
    const auth = await this.authRequired();
    if (!auth) {
      return {response: {ok: false, status: 401}, body: {}};
    }
    const headers = {
      'Authorization': this.accessToken.jwt,
    };
    const URI = ApiClient.tournamentURIs[
        'tournament-delete'
    ].replace(':id', tournamentId);
    return await ApiClient.delete(ApiClient.tournament,
        URI, {}, headers);
  }

  async joinTournament(tournamentId, nickname, password) {
    const auth = await this.authRequired();
    if (!auth) {
      return {response: {ok: false, status: 401}, body: {}};
    }
    const headers = {
      'Authorization': this.accessToken.jwt,
    };
    const body = {
      nickname: nickname,
      password: password,
    };
    const URI = ApiClient.tournamentURIs[
        'tournament-join'
    ].replace(':id', tournamentId);
    return await ApiClient.post(ApiClient.tournament,
        URI, body, headers);
  }

  async getTournament(tournamentId) {
    const auth = await this.authRequired();
    if (!auth) {
      return {response: {ok: false, status: 401}, body: {}};
    }
    const headers = {
      'Authorization': this.accessToken.jwt,
    };
    const URI = ApiClient.tournamentURIs[
        'tournament'
    ].replace(':id', tournamentId);
    return await ApiClient.get(ApiClient.tournament,
        URI, {}, headers);
  }

  async getTournamentMatches(tournamentId) {
    const auth = await this.authRequired();
    if (!auth) {
      return {response: {ok: false, status: 401}, body: {}};
    }
    const headers = {
      'Authorization': this.accessToken.jwt,
    };
    const URI = ApiClient.tournamentURIs[
        'tournament-matches'
    ].replace(':id', tournamentId);
    return await ApiClient.get(ApiClient.tournament,
        URI,
        {}, headers);
  }

  async getTournaments(page, pageSize=10,
      displayPrivate=false,
      displayFinished=false) {
    const auth = await this.authRequired();
    if (!auth) {
      return {response: {ok: false, status: 401}, body: {}};
    }
    const headers = {
      'Authorization': this.accessToken.jwt,
    };
    const params = {
      'page': page,
      'page-size': pageSize,
      ...(displayPrivate && {'display-private': ''}),
      ...(displayFinished && {'display-completed': ''}),
    };
    return await ApiClient.get(ApiClient.tournament,
        ApiClient.tournamentURIs['tournaments'], params, headers);
  }

  async getFtAuth() {
    return await ApiClient.get('user-management', 'user/oauth/42api/');
  }
  isAuth() {
    return new JWT(this.refreshToken).isValid();
  }

  async restoreCache() {
    const userId = new JWT(this.refreshToken).payload.user_id;
    const {response, body} = await ApiClient.get('user-management', `user/${userId}/`);
    if (response.ok) {
      localStorage.setItem('username', body.username);
    }
  }

  async signIn(username, password) {
    const body = {
      username: username,
      password: password,
    };
    return await ApiClient.post(ApiClient.userManagement,
        ApiClient.userManagementURIs['signin'], body);
  }

  async signUp(username, email, password) {
    const body = {
      username: username,
      email: email,
      password: password,
    };
    return await ApiClient.post(ApiClient.userManagement,
        ApiClient.userManagementURIs['signup'], body);
  }

  async usernameExist(username) {
    const body = {
      username: username,
    };
    return await ApiClient.post(ApiClient.userManagement,
        ApiClient.userManagementURIs['username-exist'], body);
  }

  async emailExist(email) {
    const body = {
      email: email,
    };
    return await ApiClient.post(ApiClient.userManagement,
        ApiClient.userManagementURIs['email-exist'], body);
  }

  async forgotPasswordSendCode(email) {
    const body = {
      email: email,
    };
    return await ApiClient.post(ApiClient.userManagement,
        ApiClient.userManagementURIs['forgot-password-send-code'], body);
  }

  static async patch(microservice, uri, params= {}, headers = {}) {
    const url = `${ApiClient.microservicesURLs[microservice]}/${uri}`;
    return await JSONRequests.patch(url, params, headers);
  }

  static async delete(microservice, uri, params= {}, headers = {}) {
    const url = `${ApiClient.microservicesURLs[microservice]}/${uri}`;
    return await JSONRequests.delete(url, params, headers);
  }

  static async post(microservice, uri, body, headers = {}) {
    const url = `${ApiClient.microservicesURLs[microservice]}/${uri}`;
    return await JSONRequests.post(url, body, headers);
  }

  static async get(microservice, uri, params= {}, headers = {}) {
    const url = `${ApiClient.microservicesURLs[microservice]}/${uri}`;
    return await JSONRequests.get(url, params, headers);
  }

  set refreshToken(token) {
    localStorage.setItem('refreshToken', token);
  }
  get refreshToken() {
    return localStorage.getItem('refreshToken');
  }

  logout() {
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('username');
    this.accessToken = new JWT(null);
  }
}

export class NetworkError extends Error {
  constructor(error) {
    super(error);
    this.name = 'NetworkError';
  }
}
