export class ErrorPage {
  static errorComponentName = 'error-component';
  static networkErrorMessage = 'Network error, ' +
    'please check your network connection.';
  static notFoundMessage = 'Page not found';

  static load(message, refresh = false) {
    window.app.innerHTML = `
        <navbar-component></navbar-component>
        <${ErrorPage.errorComponentName}
            message="${message}"
            refresh="${refresh}">
        </${ErrorPage.errorComponentName}>`;
  }

  static loadNetworkError() {
    ErrorPage.load(ErrorPage.networkErrorMessage, true);
  }

  static loadNotFound() {
    ErrorPage.load(ErrorPage.notFoundMessage, false);
  }
}
