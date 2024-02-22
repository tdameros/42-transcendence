export class NavbarUtils {
  static get height() {
    const navbar = document.querySelector('navbar-component');
    return navbar ? navbar.height: 0;
  }
}
