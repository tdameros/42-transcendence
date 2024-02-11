import {Component} from './Component.js';

import {
  GithubButton,
  IntraButton,
  ThemeButton,
} from './buttons';

import {
  ResetPassword,
  ResetPasswordCode,
  ResetPasswordEmail,
  ResetPasswordNew,
  TournamentBracket,
  TournamentCreate,
  TournamentDetails,
  Tournaments,
  TournamentsList,
  UserProfile,
  UserProfileChart,
  UserProfileChartsCards,
  UserProfileHeader,
  UserProfileMatchList,
  UserProfileStatsCard,
  UserProfileStatsCards,
  Home,
  Multiplayer,
  NotFound,
  Signin,
  Signup,
  Singleplayer,
} from './pages';

import {
  Alert,
  Error,
} from './utilities';

import {
  Navbar,
} from './Navbar';

import {
  Game,
} from './game';

customElements.define('github-button-component', GithubButton);
customElements.define('intra-button-component', IntraButton);
customElements.define('theme-button-component', ThemeButton);

customElements.define('reset-password-component', ResetPassword);
customElements.define('reset-password-code-component', ResetPasswordCode);
customElements.define('reset-password-email-component', ResetPasswordEmail);
customElements.define('reset-password-new-component', ResetPasswordNew);


customElements.define('tournament-bracket-component', TournamentBracket);
customElements.define('tournament-create-component', TournamentCreate);
customElements.define('tournament-details-component', TournamentDetails);
customElements.define('tournaments-list-component', TournamentsList);
customElements.define('tournaments-component', Tournaments);

customElements.define('home-component', Home);
customElements.define('multiplayer-component', Multiplayer);
customElements.define('notfound-component', NotFound);
customElements.define('signin-component', Signin);
customElements.define('signup-component', Signup);
customElements.define('singleplayer-component', Singleplayer);


customElements.define('user-profile-component', UserProfile);
customElements.define('user-profile-chart-component', UserProfileChart);
customElements.define(
    'user-profile-charts-cards-component', UserProfileChartsCards,
);
customElements.define('user-profile-header-component', UserProfileHeader);
customElements.define(
    'user-profile-match-list-component', UserProfileMatchList,
);
customElements.define(
    'user-profile-stats-card-component', UserProfileStatsCard,
);
customElements.define(
    'user-profile-stats-cards-component', UserProfileStatsCards,
);

customElements.define('alert-component', Alert);
customElements.define('error-component', Error);

customElements.define('navbar-component', Navbar);

customElements.define('game-component', Game);

export {
  Component,
  GithubButton,
  IntraButton,
  ThemeButton,
  ResetPassword,
  ResetPasswordCode,
  ResetPasswordEmail,
  ResetPasswordNew,
  TournamentBracket,
  TournamentCreate,
  TournamentDetails,
  Tournaments,
  TournamentsList,
  UserProfile,
  UserProfileChart,
  UserProfileChartsCards,
  UserProfileHeader,
  UserProfileMatchList,
  UserProfileStatsCard,
  UserProfileStatsCards,
  Home,
  Multiplayer,
  NotFound,
  Signin,
  Signup,
  Singleplayer,
  Alert,
  Error,
  Navbar,
};
