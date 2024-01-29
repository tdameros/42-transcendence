import {Cookies} from './Cookies.js';

export class Theme {
  static defaultTheme = 'light';

  static set(theme) {
    Cookies.add('theme', theme);
    document.querySelector('body').setAttribute('data-bs-theme', theme);
  }

  static get() {
    const theme = Cookies.get('theme');
    if (theme === null) {
      return Theme.defaultTheme;
    }
    return theme;
  }

  static init() {
    Theme.set(Theme.get());
  }
}

export default {Theme};
