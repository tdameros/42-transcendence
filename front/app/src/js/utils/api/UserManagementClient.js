import {BaseApiClient} from './BaseClient.js';
import {JSONRequests} from '@utils/JSONRequests.js';

export class UserManagementClient extends BaseApiClient {
  static URL = `https://${window.location.hostname}:6002`;

  static URIs = {
    'signin': 'user/signin/',
    'signup': 'user/signup/',
    'username-exist': 'user/username-exist/',
    'email-exist': 'user/email-exist/',
    'forgot-password-send-code': 'user/forgot-password/send-code/',
    'refresh-access-token': 'user/refresh-access-jwt/',
    'user-id': 'user/id/:id/',
    'user-username': 'user/:username/',
    'search-username': 'user/search-username/',
    'user-id-list': 'user/id-list/',
    'oauth': 'user/oauth/:oauth-service/',
  };

  constructor() {
    super();
    this.URL = UserManagementClient.URL;
    this.URIs = UserManagementClient.URIs;
  }

  async getOAuthIntra(source) {
    const URL = `${this.URL}/${this.URIs['oauth'].replace(':oauth-service', '42api')}`;
    const params = {
      'source': source,
    };
    return await JSONRequests.get(URL, params);
  }

  async getOAuthGithub(source) {
    const URL = `${this.URL}/${this.URIs['oauth'].replace(':oauth-service', 'github')}`;
    const params = {
      'source': source,
    };
    return await JSONRequests.get(URL, params);
  }

  async getUsernameList(IDList) {
    const body = {
      'id_list': IDList,
    };
    const URL = `${this.URL}/${this.URIs['user-id-list']}`;
    return await this.postAuthRequest(URL, body);
  }

  async getUserByUsername(username) {
    const URI = this.URIs['user-username'].replace(':username', username);
    const URL = `${this.URL}/${URI}`;
    return await this.getAuthRequest(URL);
  }

  async getUserById(userId) {
    const URI = this.URIs['user-id'].replace(':id', userId);
    const URL = `${this.URL}/${URI}`;
    return await this.getAuthRequest(URL);
  }

  async searchUsername(username) {
    const body = {
      'username': username,
    };
    const URL = `${this.URL}/${this.URIs['search-username']}`;
    return await this.postAuthRequest(URL, body);
  }

  async signIn(username, password) {
    const body = {
      username: username,
      password: password,
    };
    const URL = `${this.URL}/${this.URIs['signin']}`;
    return await JSONRequests.post(URL, body);
  }

  async signUp(username, email, password) {
    const body = {
      username: username,
      email: email,
      password: password,
    };
    const URL = `${this.URL}/${this.URIs['signup']}`;
    return await JSONRequests.post(URL, body);
  }

  async usernameExist(username) {
    const body = {
      username: username,
    };
    const URL = `${this.URL}/${this.URIs['username-exist']}`;
    return await JSONRequests.post(URL, body);
  }

  async emailExist(email) {
    const body = {
      email: email,
    };
    const URL = `${this.URL}/${this.URIs['email-exist']}`;
    return await JSONRequests.post(URL, body);
  }

  async forgotPasswordSendCode(email) {
    const body = {
      email: email,
    };
    const URL = `${this.URL}/${this.URIs['forgot-password-send-code']}`;
    return await JSONRequests.post(URL, body);
  }
}
