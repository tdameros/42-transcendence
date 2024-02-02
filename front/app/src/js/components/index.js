import {
  GithubButton,
  IntraButton,
  ThemeButton,
} from './buttons';

import {
  Home,
  Multiplayer,
  Signin,
  Signup,
  Singleplayer,
  Tournaments,
} from './pages';

import {
  ResetPassword,
  ResetPasswordCode,
  ResetPasswordEmail,
  ResetPasswordNew,
} from './reset_password';

import {
  Alert,
  Error,
} from './utilities';

import {
  Navbar,
} from './Navbar';

customElements.define('github-button-component', GithubButton);
customElements.define('intra-button-component', IntraButton);
customElements.define('theme-button-component', ThemeButton);

customElements.define('home-component', Home);
customElements.define('multiplayer-component', Multiplayer);
customElements.define('signin-component', Signin);
customElements.define('signup-component', Signup);
customElements.define('singleplayer-component', Singleplayer);
customElements.define('tournaments-component', Tournaments);

customElements.define('reset-password-component', ResetPassword);
customElements.define('reset-password-code-component', ResetPasswordCode);
customElements.define('reset-password-email-component', ResetPasswordEmail);
customElements.define('reset-password-new-component', ResetPasswordNew);

customElements.define('alert-component', Alert);
customElements.define('error-component', Error);

customElements.define('navbar-component', Navbar);
