export class ErrorPage {
  static errorComponentName = 'error-component';
  static NetworkErrorMessage = 'Network error, ' +
    'please check your network connection.';

  static load(message, refresh = false) {
    window.app.innerHTML = `
        <${ErrorPage.errorComponentName}
            message="${message}"
            refresh="${refresh}">
        </${ErrorPage.errorComponentName}>`;
  }

  static loadNetworkError() {
    ErrorPage.load(ErrorPage.NetworkErrorMessage, true);
  }

  static loadNotFound() {
    ErrorPage.load('Page not found');
  }
}
