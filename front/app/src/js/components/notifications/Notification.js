import {Component} from '@components';
import {notificationClient, userManagementClient} from '@utils/api';
import {FriendsCache} from '@utils/cache';
import {ErrorPage} from '@utils/ErrorPage.js';
import {getRouter} from '@js/Router.js';
import {ToastNotifications} from './ToastNotifications.js';
import {Cookies} from '@js/Cookies.js';

export class Notification extends Component {
  static privacyPolicyMessage = `
    We use cookies on our website to enhance your user experience.
    By continuing to use our site, you consent to the use of these cookies in accordance with our privacy policy.

    For more information on our use of cookies and how we protect your personal data, please refer to our <a class='text-primary text-decoration-none' onclick="window.router.navigate('/privacy-policy/')">privacy policy<a>.
  `;

  constructor() {
    super();
    this.notifications = [];
    this.webSocket = null;
    this.URL = `wss://${window.location.hostname}:6005/`;
    this.URI = 'ws/notification/?Authorization=:access_token';
  }
  render() {
    return (`
      <toast-notifications-component></toast-notifications-component>
    `);
  }
  style() {
    return (`
      <style>
      </style>
    `);
  }

  async postRender() {
    await this.tryConnect();
    setInterval(() => {
      this.sendAccessToken();
    }, 10000);
    this.toastNotifications = this.querySelector(
        'toast-notifications-component',
    );
    if (!Cookies.get('policy')) {
      ToastNotifications.addPolicyNotification(
          Notification.privacyPolicyMessage,
      );
    }
  }

  async tryConnect() {
    if (userManagementClient.isAuth()) {
      try {
        const accessToken = await userManagementClient.getValidAccessToken();
        if (accessToken !== null) {
          this.connect(accessToken);
        }
      } catch (error) {
        ErrorPage.loadNetworkError();
      }
    }
  }

  connect(accessToken) {
    try {
      this.webSocket = new WebSocket(
          this.URL + this.URI.replace(':access_token', accessToken),
      );
      this.webSocket.onopen = this.onConnect.bind(this);
      this.webSocket.onmessage = this.onMessage.bind(this);
      this.webSocket.onclose = this.onClose.bind(this);
      this.webSocket.onerror = this.onError.bind(this);
      return true;
    } catch (e) {
      return false;
    }
  }

  onConnect() {
  }

  onClose() {
    this.webSocket = null;
  }

  onError() {
    this.webSocket = null;
  }

  async onMessage(eventMessage) {
    const data = JSON.parse(eventMessage.data);
    const notification = JSON.parse(data.message);
    if (notification.type === 'friend_status') {
      await this.#updateFriendInCache(notification);
      if (document.querySelector('friends-component')) {
        document.querySelector('friends-component').updateFriends();
      }
    } else if (notification.type === 'friend_request' ||
               notification.type === 'tournament_start') {
      await this.addNotification(notification);
    }
  }

  async sendAccessToken() {
    if (this.webSocket !== null && userManagementClient.isAuth() &&
      userManagementClient.accessToken.getTimeRemainingInSeconds() < 60) {
      try {
        if (await userManagementClient.refreshAccessToken()) {
          const messageData = {
            'access_token': await userManagementClient.getValidAccessToken(),
          };
          if (this.webSocket !== null) {
            this.webSocket.send(JSON.stringify(messageData));
          }
        } else {
          this.disconnect();
        }
      } catch (error) {
        this.disconnect();
      }
    }
  }

  disconnect() {
    if (this.webSocket !== null) {
      this.webSocket.close();
    }
  }

  async addNotification(notification) {
    if (notification.type === 'friend_request') {
      if (!await this.#addUsernameInFriendRequestNotification(notification)) {
        return;
      }
    }
    this.notifications.push(notification);
    if (notification['new_notification']) {
      this.toastNotifications.addNotification(notification);
    }
    const navbar = document.querySelector('navbar-component');
    if (navbar) {
      navbar.addNotification(notification);
    }
  }

  async #addUsernameInFriendRequestNotification(notification) {
    try {
      const userId = parseInt(notification.data);
      const {response, body} =
        await userManagementClient.getUsernameListInCache([userId]);
      if (response.ok) {
        notification['sender_username'] = body[notification.data];
        return true;
      } else {
        getRouter().redirect('/signin/');
        return false;
      }
    } catch (error) {
      ErrorPage.loadNetworkError();
      return false;
    }
  }

  async #updateFriendInCache(notification) {
    if (notification['status'] === 'deleted') {
      FriendsCache.delete(notification['friend_id']);
    } else {
      const friend = FriendsCache.get(notification['friend_id']);
      if (friend) {
        friend['connected_status'] = notification['status'];
        friend['status'] = 'accepted';
        FriendsCache.set(notification['friend_id'], friend);
      } else {
        await this.#addFriendInCache(notification);
      }
    }
  }

  async #addFriendInCache(notification) {
    try {
      const {response, body} = await userManagementClient.getUsernameList(
          [notification['friend_id']],
      );
      if (response.ok) {
        const newFriend = {
          'id': notification['friend_id'],
          'username': body[notification['friend_id']],
          'status': 'accepted',
          'connected_status': notification['status'],
        };
        FriendsCache.set(newFriend.id, newFriend);
      } else {
        getRouter().redirect('/signin/');
      }
    } catch (error) {
      ErrorPage.loadNetworkError();
    }
  }

  async removeNotification(notification) {
    this.notifications = this.notifications.filter((n) => n !== notification);
    if (notification.type === 'friend_request') {
      FriendsCache.delete(notification['friend_id']);
    }
    try {
      await notificationClient.deleteNotification(notification.id);
    } catch (error) {
      ErrorPage.loadNetworkError();
    }
  }
}
