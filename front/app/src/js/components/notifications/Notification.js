import {Component} from '@components';
import {notificationClient, userManagementClient} from '@utils/api/index.js';
import {FriendsCache} from '@utils/cache';
import {ErrorPage} from '@utils/ErrorPage.js';
import {getRouter} from '@js/Router.js';

export class Notification extends Component {
  constructor() {
    super();
    this.notifications = [];
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
  }

  async tryConnect() {
    if (userManagementClient.isAuth()) {
      const accessToken = await userManagementClient.getValidAccessToken();
      if (accessToken === null) {
        return;
      } else {
        this.connect(accessToken);
      }
    }
  }

  connect(accessToken) {
    try {
      this.webSocket = new WebSocket(
          `wss://${
            window.location.hostname
          }:6005/ws/notification/?Authorization=${accessToken}`,
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
    }
  }

  disconnect() {
    this.webSocket.close();
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
      const {response, body} = await userManagementClient.getUsernameList(
          [notification.data],
      );
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
