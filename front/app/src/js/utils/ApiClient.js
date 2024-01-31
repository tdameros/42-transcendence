import {JSONRequests} from './JSONRequests.js';
import {JWT} from './JWT.js';

export class ApiClient {
  static microservicesURLs = {
    'user-management': 'http://localhost:6002',
  };

  constructor() {
    this.accessToken = new JWT(null);
  }

  async getFtAuth() {
    return await ApiClient.get('user-management', 'user/oauth/42api/');
  }
  isAuth() {
    return new JWT(this.refreshToken).isValid();
  }

  async restoreCache() {
    const userId = new JWT(this.refreshToken).payload.user_id;
    const {response, body} = await ApiClient.get('user-management', `user/${userId}/`);
    if (response.ok) {
      localStorage.setItem('username', body.username);
    }
  }

  async signIn(username, password) {
    const body = {
      username: username,
      password: password,
    };
    return await ApiClient.post('user-management',
        'user/signin/', body);
  }

  async signUp(username, email, password) {
    const body = {
      username: username,
      email: email,
      password: password,
    };
    return await ApiClient.post('user-management',
        'user/signup/', body);
  }

  async usernameExist(username) {
    const body = {
      username: username,
    };
    return await ApiClient.post('user-management',
        'user/username-exist/', body);
  }

  async emailExist(email) {
    const body = {
      email: email,
    };
    return await ApiClient.post('user-management',
        'user/email-exist/', body);
  }

  async forgotPasswordSendCode(email) {
    const body = {
      email: email,
    };
    return await ApiClient.post('user-management',
        'user/forgot-password/send-code/', body);
  }

  static async post(microservice, uri, body, headers = {}) {
    const url = `${ApiClient.microservicesURLs[microservice]}/${uri}`;
    return await JSONRequests.post(url, body, headers);
  }

  static async get(microservice, uri, headers = {}) {
    const url = `${ApiClient.microservicesURLs[microservice]}/${uri}`;
    return await JSONRequests.get(url, headers);
  }

  set refreshToken(token) {
    localStorage.setItem('refreshToken', token);
  }
  get refreshToken() {
    return localStorage.getItem('refreshToken');
  }

  logout() {
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('username');
    this.accessToken = null;
  }
}

export class NetworkError extends Error {
  constructor(error) {
    super(error);
    this.name = 'NetworkError';
  }
}
