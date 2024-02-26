import {Component} from '@components';
import {ErrorPage} from '@utils/ErrorPage.js';
import {userManagementClient, userStatsClient} from '@utils/api';
import {getRouter} from '@js/Router.js';

export class UserProfileContent extends Component {
  constructor() {
    super();
  }

  render() {
    return (`
      <div class="m-2">
          <user-profile-header-component placeholder="true"></user-profile-header-component>
          <user-profile-stats-cards-component></user-profile-stats-cards-component>
          <user-profile-charts-cards-component></user-profile-charts-cards-component>
          <user-profile-match-list-component></user-profile-match-list-component>
      </div>
    `);
  }

  style() {
    return (`
      <style>
      </style>
    `);
  }


  async postRender() {
    const username = this.getAttribute('username');
    const userId = await this.getUserId(username);
    if (!userId) {
      return;
    }
    const statistics = await this.fetchStatistics(userId);
    if (!statistics) {
      return;
    }
    this.updateComponents(userId, username, statistics);
  }

  updateComponents(userId, username, statistics) {
    this.userProfileHeader = this.querySelector(
        'user-profile-header-component',
    );
    this.userProfileHeader.loadUserProfile(username, userId);

    this.statisticsCards = this.querySelector(
        'user-profile-stats-cards-component',
    );
    this.statisticsCards.loadStatistics(
        statistics.general, statistics.progress,
    );

    this.chartsCards = this.querySelector(
        'user-profile-charts-cards-component',
    );
    this.chartsCards.loadStatistics(
        statistics.eloGraph,
        statistics.winRateGraph,
        statistics.matchesPlayedGraph,
    );

    this.userProfileMatchList = this.querySelector(
        'user-profile-match-list-component',
    );
    this.userProfileMatchList.loadMatchHistory(
        userId, statistics.matchHistory,
    );
  }

  async fetchStatistics(userId) {
    const week = this.convertDatesToIsoString(this.getDatesFromThisWeek());
    const month = this.convertDatesToIsoString(this.getDatesFromLastMonth());
    const [
      general,
      progress,
      eloGraph,
      winRateGraph,
      matchesPlayedGraph,
      matchHistory,
    ] = await Promise.all([
      this.fetchData('getGeneralStatistics', userId),
      this.fetchData('getProgressStatistics', userId),
      this.fetchData('getEloGraph', userId, month.startDate, month.endDate),
      this.fetchData('getWinRateGraph', userId, month.startDate, month.endDate),
      this.fetchData('getMatchesPlayedGraph', userId,
          week.startDate, week.endDate),
      this.fetchData('getMatchHistory', userId, 1),
    ]);

    if ([general, progress, eloGraph, winRateGraph,
      matchesPlayedGraph, matchHistory].includes(false)) {
      return false;
    }
    if (!await this.addUsernameInMatchHistory(matchHistory)) {
      return false;
    }
    return {
      general,
      progress,
      eloGraph,
      winRateGraph,
      matchesPlayedGraph,
      matchHistory,
    };
  }

  async fetchData(endpoint, ...args) {
    try {
      const {response, body} = await userStatsClient[endpoint](...args);
      if (response.ok) {
        return body;
      } else {
        getRouter().redirect('/signin/');
        return false;
      }
    } catch (error) {
      ErrorPage.loadNetworkError();
      return false;
    }
  }

  async addUsernameInMatchHistory(matchHistory) {
    const opponentsIds = matchHistory['history'].map(
        (match) => parseInt(match['opponent_id']),
    );
    try {
      const {response, body} =
        await userManagementClient.getUsernameListInCache(opponentsIds);
      if (response.ok) {
        matchHistory['history'].forEach((match) => {
          match['opponent_username'] = body[match['opponent_id']];
        });
        return true;
      } else {
        getRouter().redirect('/signin/');
        return false;
      }
    } catch (error) {
      ErrorPage.loadNetworkError();
      return false;
    }
  }

  async getUserId(username) {
    try {
      const {response, body} =
        await userManagementClient.getUserByUsernameInCache(username);
      if (response.ok) {
        return body.id;
      } else if (response.status === 404) {
        ErrorPage.load('User not found');
        return false;
      } else {
        getRouter().redirect('/signin/');
        return false;
      }
    } catch (error) {
      ErrorPage.loadNetworkError();
      return false;
    }
  }

  getDatesFromThisWeek() {
    const currentDate = new Date();
    const startDate = new Date();
    startDate.setDate(currentDate.getDate() - currentDate.getDay() +
      (currentDate.getDay() === 0 ? -6 : 1));
    const endDate = new Date();
    endDate.setDate(startDate.getDate() + 7);
    return {startDate, endDate};
  }

  getDatesFromLastMonth() {
    const startDate = new Date();
    startDate.setDate(startDate.getDate() - 30);
    const endDate = new Date();
    return {startDate, endDate};
  }

  convertDatesToIsoString(dates) {
    return {
      startDate: dates.startDate.toISOString(),
      endDate: dates.endDate.toISOString(),
    };
  }
}
