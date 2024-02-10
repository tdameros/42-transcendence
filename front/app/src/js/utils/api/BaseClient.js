import {JSONRequests} from '@utils/JSONRequests.js';
import {JWT} from '@utils/JWT.js';
import {UserManagementClient} from './UserManagementClient.js';
import {userManagementClient} from '@utils/api/index.js';

export class BaseApiClient {
  static accessToken = new JWT(null);
  constructor() {
  }

  isAuth() {
    return new JWT(this.refreshToken).isValid();
  }

  get accessToken() {
    return BaseApiClient.accessToken;
  }

  set accessToken(token) {
    BaseApiClient.accessToken = token;
  }

  async restoreCache() {
    const userId = new JWT(this.refreshToken).payload.user_id;
    const {response, body} = await userManagementClient.getUserById(userId);
    if (response.ok) {
      localStorage.setItem('username', body.username);
    }
  }

  async authRequired() {
    if (this.refreshToken === null) {
      return false;
    }
    if (await this.getValidAccessToken() === null) {
      return false;
    }
    return true;
    // if (!this.accessToken.isValid()) {
    //   const isRefresh = await this.refreshAccessToken();
    //   if (!isRefresh) {
    //     return false;
    //   }
    // }
    // return true;
  }

  async getValidAccessToken() {
    if (this.accessToken.isValid()) {
      return this.accessToken.jwt;
    }
    const isRefresh = await this.refreshAccessToken();
    if (!isRefresh) {
      return null;
    }
    return this.accessToken.jwt;
  }

  async refreshAccessToken() {
    const requestBody = {
      'refresh_token': this.refreshToken,
    };
    const {response, body} = await JSONRequests.post(
        `${UserManagementClient.URL}/${UserManagementClient.URIs['refresh-access-token']}`,
        requestBody);
    if (response.ok) {
      this.accessToken = new JWT(body['access_token']);
      return true;
    } else {
      this.logout();
      return false;
    }
  }

  logout() {
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('username');
    this.accessToken = new JWT(null);
  }

  get username() {
    return localStorage.getItem('username');
  }

  get userId() {
    return new JWT(this.refreshToken).payload.user_id;
  }

  set refreshToken(token) {
    localStorage.setItem('refreshToken', token);
  }
  get refreshToken() {
    return localStorage.getItem('refreshToken');
  }

  async getAuthRequest(url, params={}, headers={}) {
    const auth = await this.authRequired();
    if (!auth) {
      return {response: {ok: false, status: 401}, body: {}};
    }
    headers['Authorization'] = this.accessToken.jwt;
    return await JSONRequests.get(url, params, headers);
  }

  async postAuthRequest(url, body, headers={}) {
    const auth = await this.authRequired();
    if (!auth) {
      return {response: {ok: false, status: 401}, body: {}};
    }
    headers['Authorization'] = this.accessToken.jwt;
    return await JSONRequests.post(url, body, headers);
  }

  async patchAuthRequest(url, body={}, headers={}) {
    const auth = await this.authRequired();
    if (!auth) {
      return {response: {ok: false, status: 401}, body: {}};
    }
    headers['Authorization'] = this.accessToken.jwt;
    return await JSONRequests.patch(url, body, headers);
  }

  async deleteAuthRequest(url, body={}, headers={}) {
    const auth = await this.authRequired();
    if (!auth) {
      return {response: {ok: false, status: 401}, body: {}};
    }
    headers['Authorization'] = this.accessToken.jwt;
    return await JSONRequests.delete(url, body, headers);
  }
}