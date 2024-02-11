import {Component} from '@components';

export class UserProfileStatsCards extends Component {
  constructor() {
    super();
  }
  render() {
    return (`
        <div class="row gx-3 gy-2 mb-3 mt-3">
                <div class="col-xl-3 col-sm-6">
                  <user-profile-stats-card-component id="elo-card" title="Elo"
                                                     icon="bi-bar-chart-line" icon-bg="bg-danger"
                                                     footer-title="Since last week"
                                                     placeholder="true">
                  </user-profile-stats-card-component>
                </div>
                <div class="col-xl-3 col-sm-6">
                  <user-profile-stats-card-component id="win-rate-card" title="Win Rate"
                                                      icon="bi-trophy" icon-bg="bg-success"
                                                      footer-title="Since last week"
                                                      placeholder="true">
                  </user-profile-stats-card-component>
                </div>
                <div class="col-xl-3 col-sm-6">
                  <user-profile-stats-card-component id="matches-played-card" title="Played Games"
                                                      icon="bi-controller" icon-bg="bg-primary"
                                                      footer-title="Since last week"
                                                      placeholder="true">
                  </user-profile-stats-card-component>
                  </div>
                <div class="col-xl-3 col-sm-6">
                  <user-profile-stats-card-component id="friends-card" title="Friends"
                                                      icon="bi-people" icon-bg="bg-warning"
                                                      footer-title="Since last week"
                                                      placeholder="true">
                  </user-profile-stats-card-component>
                </div>
            </div
    `);
  }

  async postRender() {
    this.eloCard = this.querySelector('#elo-card');
    this.winRateCard = this.querySelector('#win-rate-card');
    this.playedGamesCard = this.querySelector('#matches-played-card');
    this.friendsCard = this.querySelector('#friends-card');
  }

  loadStatistics(general, progress) {
    const cards = {
      'elo': this.eloCard,
      'win_rate': this.winRateCard,
      'matches_played': this.playedGamesCard,
      'friends': this.friendsCard,
    };
    for (const key in cards) {
      if (cards.hasOwnProperty(key)) {
        if (key === 'win_rate') {
          cards[key].loadValues(
              parseInt(general[key]), parseInt(progress[key]), '%',
          );
        } else {
          cards[key].loadValues(general[key], progress[key]);
        }
      }
    }
  }

  style() {
    return (`
      <style>
      </style>
    `);
  }
}
