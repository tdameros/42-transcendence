import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';
import '../css/style.css';

import 'bootstrap';

import './components';
import {Router, Route} from './Router.js';
import {Theme} from './Theme.js';
import {ApiClient} from './utils/ApiClient.js';

Theme.init();

const client = new ApiClient();
window.ApiClient = client;

const app = document.querySelector('#app');

const router = new Router(app, [
  new Route('/singleplayer/', 'singleplayer-component'),
  new Route('/multiplayer/', 'multiplayer-component'),
  new Route('/tournaments/', 'tournaments-component'),
  new Route('/tournaments/page/:id', 'tournaments-component'),
  new Route('/signin/', 'signin-component'),
  new Route('/signup/', 'signup-component'),
  new Route('/reset-password/', 'reset-password-component'),
  new Route('/oauth/:refresh-token/', 'oauth-component'),
  new Route('/tournaments/create/', 'tournaments-create-component'),
  new Route('', 'home-component'),
]);

window.router = router;
router.init();
