export class ErrorPage {
  static errorComponentName = 'error-component';
  static NetworkErrorMessage = 'Network error, ' +
    'please check your network connection.';

  static load(message) {
    window.app.innerHTML = `
        <${ErrorPage.errorComponentName}
            message="${message}">
        </${ErrorPage.errorComponentName}>`;
  }

  static loadNetworkError() {
    ErrorPage.load(ErrorPage.NetworkErrorMessage);
  }
}
