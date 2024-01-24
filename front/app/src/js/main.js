import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';
import '../css/style.css';

import * as bootstrap from 'bootstrap'

import { Router, Route } from './Router.js';
import { Home } from "./components/Home.js";
import { Navbar } from "./components/Navbar.js";
import {Singleplayer} from "./components/Singleplayer.js";
import {Tournaments} from "./components/Tournaments.js";
import {Multiplayer} from "./components/Multiplayer.js";
import {Theme} from "./Theme.js";
import {ThemeButton} from "./components/ThemeButton.js";
import {Signin} from "./components/Signin.js";
import {Signup} from "./components/Signup.js";
import {ResetPassword} from "./components/ResetPassword.js";


Theme.init();

customElements.define('home-component', Home);
customElements.define('navbar-component', Navbar);
customElements.define('singleplayer-component', Singleplayer);
customElements.define('multiplayer-component', Multiplayer);
customElements.define('tournaments-component', Tournaments);
customElements.define('theme-button-component', ThemeButton);
customElements.define('signin-component', Signin);
customElements.define('signup-component', Signup);
customElements.define('reset-password-component', ResetPassword);

const app = document.querySelector('#app');

const router = new Router(app, [
    new Route('/singleplayer/', 'singleplayer-component'),
    new Route('/multiplayer/', 'multiplayer-component'),
    new Route('/tournaments/', 'tournaments-component'),
    new Route('/signin/', 'signin-component'),
    new Route('/signup/', 'signup-component'),
    new Route('', 'home-component'),
    new Route('/reset-password/', 'reset-password-component'),
]);

window.router = router;
