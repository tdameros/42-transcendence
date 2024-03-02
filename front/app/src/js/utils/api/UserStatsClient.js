import {BaseApiClient} from './BaseClient.js';

export class UserStatsClient extends BaseApiClient {
  static URL = `https://${window.location.hostname}:6003`;

  static URIs = {
    'general-statistics': 'statistics/user/:user_id/',
    'progress-statistics': 'statistics/user/:user_id/progress/',
    'graph-elo': 'statistics/user/:user_id/graph/elo/',
    'graph-win-rate': 'statistics/user/:user_id/graph/win_rate/',
    'graph-matches-played': 'statistics/user/:user_id/graph/matches_played/',
    'match-history': 'statistics/user/:user_id/history/',
    'ranking': 'statistics/ranking/',
  };

  constructor() {
    super();
    this.URL = UserStatsClient.URL;
    this.URIs = UserStatsClient.URIs;
  }

  async getRanking(page, pageSize=50) {
    const params = {
      'page': page,
      'page_size': pageSize,
    };
    const URL = `${this.URL}/${this.URIs['ranking']}`;
    return await this.getAuthRequest(URL, params);
  }

  async getMatchHistory(userId, page, pageSize=10) {
    const params = {
      'page': page,
      'page_size': pageSize,
    };
    const URI = this.URIs['match-history'].replace(':user_id', userId);
    const URL = `${this.URL}/${URI}`;
    return await this.getAuthRequest(URL, params);
  }

  async getMatchesPlayedGraph(userId, startDate, endDate, maxPoints=7) {
    const params = {
      'start': startDate,
      'end': endDate,
      'max_points': maxPoints,
    };
    const URI = this.URIs['graph-matches-played'].replace(':user_id', userId);
    const URL = `${this.URL}/${URI}`;
    return await this.getAuthRequest(URL, params);
  }

  async getEloGraph(userId, startDate, endDate, maxPoints=25) {
    const params = {
      'start': startDate,
      'end': endDate,
      'max_points': maxPoints,
    };
    const URI = this.URIs['graph-elo'].replace(':user_id', userId);
    const URL = `${this.URL}/${URI}`;
    return await this.getAuthRequest(URL, params);
  }

  async getWinRateGraph(userId, startDate, endDate, maxPoints=25) {
    const params = {
      'start': startDate,
      'end': endDate,
      'max_points': maxPoints,
    };
    const URI = this.URIs['graph-win-rate'].replace(':user_id', userId);
    const URL = `${this.URL}/${URI}`;
    return await this.getAuthRequest(URL, params);
  }

  async getProgressStatistics(userId) {
    const URI = this.URIs['progress-statistics'].replace(':user_id', userId);
    const URL = `${this.URL}/${URI}`;
    return await this.getAuthRequest(URL);
  }

  async getGeneralStatistics(userId) {
    const URI = this.URIs['general-statistics'].replace(':user_id', userId);
    const URL = `${this.URL}/${URI}`;
    return await this.getAuthRequest(URL);
  }
}
