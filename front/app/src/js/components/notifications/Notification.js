import {Component} from '@components';
import {notificationClient, userManagementClient} from '@utils/api/index.js';

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
    // on socket open
    console.log('Socket successfully connected');
  }

  onClose() {
    // on socket close
    console.log('Socket closed');
    this.webSocket = null;
  }

  onError() {
    console.log('Failed to connect');
    this.webSocket = null;
  }

  onMessage(eventMessage) {
    const data = JSON.parse(eventMessage.data);
    const notification = JSON.parse(data.message);

    if (notification.type === 'friend_status') {
      // TODO: implement friend status change
      console.log('Friend status changed');
    } else if (notification.type === 'friend_request' ||
               notification.type === 'tournament_start') {
      this.addNotification(notification);
    }
  };

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

  addNotification(notification) {
    this.notifications.push(notification);
    if (notification['new_notification']) {
      this.toastNotifications.addNotification(notification);
    }
    const navbar = document.querySelector('navbar-component');
    if (navbar) {
      navbar.addNotification(notification);
    }
  }

  async removeNotification(notification) {
    this.notifications = this.notifications.filter((n) => n !== notification);
    try {
      await notificationClient.deleteNotification(notification.id);
    } catch (error) {
      getRouter().navigate('/signin/');
    }
  }
}
