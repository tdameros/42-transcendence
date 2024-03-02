import {BaseApiClient} from './BaseClient.js';
import {JSONRequests} from '@utils/JSONRequests.js';
import {UsersCache} from '@utils/cache';

export class UserManagementClient extends BaseApiClient {
  static URL = `https://${window.location.hostname}:6002`;

  static URIs = {
    'signin': 'user/signin/',
    'signup': 'user/signup/',
    'username-exist': 'user/username-exist/',
    'email-exist': 'user/email-exist/',
    'forgot-password-send-code': 'user/forgot-password/send-code/',
    'forgot-password-check-code': 'user/forgot-password/check-code/',
    'forgot-password-change': 'user/forgot-password/change-password/',
    'refresh-access-token': 'user/refresh-access-jwt/',
    'user-id': 'user/id/:id/',
    'user-username': 'user/:username/',
    'search-username': 'user/search-username/',
    'user-id-list': 'user/id-list/',
    'oauth': 'user/oauth/:oauth-service/',
    'friends-accept': 'user/friends/accept/',
    'friends-decline': 'user/friends/decline/',
    'friends-request': 'user/friends/request/',
    'friends': 'user/friends/',
    'avatar': 'user/avatar/:username/',
    'change-avatar': 'user/avatar/',
    'delete-avatar': 'user/avatar/',
    'update-infos': 'user/update-infos/',
    'verify-email': 'user/verify-email/:id/:token/',
    'me': 'user/me/',
    'send-user-infos': 'user/send-user-infos/',
    'delete-account': 'user/delete-account/',
    'enable-2fa': 'user/2fa/enable/',
    'verify-2fa': 'user/2fa/verify/',
    'disable-2fa': 'user/2fa/disable/',
  };

  constructor() {
    super();
    this.URL = UserManagementClient.URL;
    this.URIs = UserManagementClient.URIs;
  }

  async disable2FA() {
    const URL = `${this.URL}/${this.URIs['disable-2fa']}`;
    return await this.postAuthRequest(URL, {});
  }

  async verify2FA(code) {
    const body = {
      'code': code,
    };
    const URL = `${this.URL}/${this.URIs['verify-2fa']}`;
    return await this.postAuthRequest(URL, body);
  }

  async enable2FA() {
    const auth = await this.authRequired();
    if (!auth) {
      return {response: {ok: false, status: 401}, body: {}};
    }
    const headers = {'Authorization': this.accessToken.jwt};
    const URL = `${this.URL}/${this.URIs['enable-2fa']}`;
    const options = {
      method: 'POST',
      headers: headers,
    };
    return {response: await fetch(URL, options), body: {}};
  }

  async deleteAccount() {
    const URL = `${this.URL}/${this.URIs['delete-account']}`;
    return await this.deleteAuthRequest(URL);
  }

  async sendUserInfos() {
    const URL = `${this.URL}/${this.URIs['send-user-infos']}`;
    return await this.getAuthRequest(URL);
  }

  async getMe() {
    const URL = `${this.URL}/${this.URIs['me']}`;
    return await this.getAuthRequest(URL);
  }

  async updateInfo(newUsername=null, newEmail=null, newPassword=null) {
    const body = {
      'change_list': [],
    };
    if (newUsername) {
      body['username'] = newUsername;
      body['change_list'].push('username');
    }
    if (newEmail) {
      body['email'] = newEmail;
      body['change_list'].push('email');
    }
    if (newPassword) {
      body['password'] = newPassword;
      body['change_list'].push('password');
    }
    const URL = `${this.URL}/${this.URIs['update-infos']}`;
    return await this.postAuthRequest(URL, body);
  }

  async deleteAvatar(username) {
    const URI = this.URIs['delete-avatar'].replace(':username', username);
    const URL = `${this.URL}/${URI}`;
    return await this.deleteAuthRequest(URL);
  }

  async changeAvatar(newAvatarInBase64, username) {
    const body = {
      'avatar': newAvatarInBase64,
    };
    const URI = this.URIs['change-avatar'].replace(':username', username);
    const URL = `${this.URL}/${URI}`;
    return await this.postAuthRequest(URL, body);
  }

  async verifyEmail(userId, token) {
    const URI = this.URIs['verify-email']
        .replace(':id', userId).replace(':token', token);
    const URL = `${this.URL}/${URI}`;
    return await JSONRequests.post(URL, {});
  }

  getURLAvatar(username) {
    const URI = this.URIs['avatar'].replace(':username', username);
    return `${this.URL}/${URI}`;
  }

  async getFriends() {
    const URL = `${this.URL}/${this.URIs['friends']}`;
    return await this.getAuthRequest(URL);
  }

  async removeFriend(userId) {
    const params = {
      'friend_id': userId,
    };
    const URL = `${this.URL}/${this.URIs['friends']}`;
    return await this.deleteAuthRequest(URL, params);
  }

  async sendFriendRequest(userId) {
    const body = {
      'friend_id': userId,
    };
    const URL = `${this.URL}/${this.URIs['friends-request']}`;
    return await this.postAuthRequest(URL, body);
  }

  async acceptFriend(userId) {
    const body = {
      'friend_id': userId,
    };
    const URL = `${this.URL}/${this.URIs['friends-accept']}`;
    return await this.postAuthRequest(URL, body);
  }

  async declineFriend(userId) {
    const body = {
      'friend_id': userId,
    };
    const URL = `${this.URL}/${this.URIs['friends-decline']}`;
    return await this.postAuthRequest(URL, body);
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

  async getUsernameListInCache(IDList) {
    const usersList = {};
    const unknownUsersID = [];

    IDList.forEach((userId) => {
      const cachedUsername = UsersCache.get(userId);
      if (cachedUsername) {
        usersList[userId] = cachedUsername;
      } else {
        unknownUsersID.push(userId);
      }
    });

    if (unknownUsersID.length > 0) {
      const {response, body} = await this.getUsernameList(unknownUsersID);
      if (!response.ok) return {response, body};
      Object.entries(body).forEach(([userId, username]) => {
        const parsedUserId = parseInt(userId);
        UsersCache.set(parsedUserId, username);
        usersList[parsedUserId] = username;
      });
    }
    return {response: {ok: true}, body: usersList};
  }


  async getUsernameList(IDList) {
    const body = {
      'id_list': IDList,
    };
    const URL = `${this.URL}/${this.URIs['user-id-list']}`;
    return await this.postAuthRequest(URL, body);
  }

  async getUserByUsernameInCache(username) {
    const cachedUserId = UsersCache.getUserId(username);
    if (cachedUserId) {
      const user = {'id': cachedUserId, 'username': username};
      return {response: {ok: true}, body: user};
    }
    const {response, body} = await this.getUserByUsername(username);
    if (response.ok) {
      UsersCache.set(body['id'], body['username']);
    }
    return {response, body};
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

  async signIn(login, password, twoFactorCode=null) {
    const body = {
      'login': login,
      'password': password,
      '2fa_code': twoFactorCode,
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

  async sendResetPasswordCode(email) {
    const body = {
      email: email,
    };
    const URL = `${this.URL}/${this.URIs['forgot-password-send-code']}`;
    return await JSONRequests.post(URL, body);
  }

  async checkResetPasswordCode(email, code) {
    const body = {
      email: email,
      code: code,
    };
    const URL = `${this.URL}/${this.URIs['forgot-password-check-code']}`;
    return await JSONRequests.post(URL, body);
  }

  async changePassword(email, code, newPassword) {
    const body = {
      'email': email,
      'code': code,
      'new_password': newPassword,
    };
    const URL = `${this.URL}/${this.URIs['forgot-password-change']}`;
    return await JSONRequests.post(URL, body);
  }
}
