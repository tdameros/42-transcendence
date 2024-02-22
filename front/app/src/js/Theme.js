import {Cookies} from '@js/Cookies.js';

export class Theme {
  static defaultTheme = 'light';

  static set(theme) {
    Cookies.add('theme', theme);
    document.querySelector('body').setAttribute('data-bs-theme', theme);
    if (theme === 'light') {
      this.hoverBrightness = Theme.darkHoverBrightness;
    } else if (theme === 'dark') {
      this.hoverBrightness = Theme.lightHoverBrightness;
    }
  }

  static set hoverBrightness(value) {
    return document.documentElement.style.setProperty(
        '--hover-brightness', value,
    );
  }

  static get lightHoverBrightness() {
    return getComputedStyle(document.documentElement).getPropertyValue(
        '--light-hover-brightness',
    );
  }

  static get darkHoverBrightness() {
    return getComputedStyle(document.documentElement).getPropertyValue(
        '--dark-hover-brightness',
    );
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
