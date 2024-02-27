import {Component} from '@components';
import {ErrorPage} from '@utils/ErrorPage.js';
import {userManagementClient} from '@utils/api';
import {getRouter} from '@js/Router.js';

export class ActivateAccount extends Component {
  constructor() {
    super();
  }

  render() {
    return (`
      <navbar-component disable-padding-top="true"></navbar-component>
      <div class="d-flex justify-content-center align-items-center" style="height: 100vh">
          <div class="spinner-border" role="status">
              <span class="visually-hidden">Loading...</span>
          </div>
      </div>
    `);
  }

  style() {
    return (`
      <style>
      </style>
    `);
  }

  async postRender() {
    const base64UserId = this.getAttribute('id');
    let userId;
    try {
      userId = atob(base64UserId);
    } catch (error) {
      getRouter().redirect(`/signin/?error=Error, failed to decode user id`);
      return false;
    }
    const token = this.getAttribute('token');
    try {
      const {response, body} = await userManagementClient.verifyEmail(
          userId, token,
      );
      if (response.ok) {
        await this.#cacheAndSignin(body.refresh_token);
      } else {
        getRouter().redirect(`/signin/?error=${body.errors[0]}`);
      }
    } catch (error) {
      ErrorPage.loadNetworkError();
    }
  }

  async #cacheAndSignin(refreshToken) {
    userManagementClient.refreshToken = refreshToken;
    if (!await userManagementClient.restoreCache()) {
      userManagementClient.logout();
      getRouter().redirect(`/signin/?error=Error, failed to store cache`);
    } else {
      getRouter().navigate('/');
    }
  }
}
