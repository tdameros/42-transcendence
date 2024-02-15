import {Component} from '@components';
import {userManagementClient, UserManagementClient} from '@utils/api/index.js';

export class Notification extends Component {
  constructor() {
    super();
    this.notifications = [];
  }
  render() {
    return (`
    
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
    }, 1000);
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

  onMessage(message) {
    let data = JSON.parse(message.data);
    data = JSON.parse(data.message);

    if (data.type === 'friend_status')
    // TODO: handle status in front
    {
      console.log('Friend status received: ' + data.friend_id + ' ' + data.status);
    } else {
      console.log('Notification received: ' + data.title);
      this.addNotification(data);
    }
  };

  async sendAccessToken() {
    if (userManagementClient.isAuth() && UserManagementClient.accessToken.getTimeRemainingInSeconds() < 60 * 15) {
      if (await userManagementClient.refreshAccessToken()) {
        const messageData = {
          'access_token': await userManagementClient.getValidAccessToken(),
        };
        if (this.webSocket !== null) {
          this.webSocket.send(JSON.stringify(messageData));
        }
      }
    }
  }

  disconnect() {
    this.webSocket.close();
  }

  addNotification(notification) {
    let navbar = document.querySelector('navbar-component');
    while (!navbar) {
      navbar = document.querySelector('navbar-component');
    }
    this.notifications.push(notification);
    navbar.addNotification(notification);
  }

  createButtons(notification) {
    const buttonContainer = document.createElement('div');
    const acceptButton = document.createElement('button');
    const declineButton = document.createElement('button');

    buttonContainer.className = 'button-container';

    acceptButton.textContent = 'Accept';
    acceptButton.className = 'btn btn-accept btn-sm';
    declineButton.textContent = 'Decline';
    declineButton.className = 'btn btn-decline btn-sm';

    this.buttonAddListenerRouter(notification, acceptButton);
    this.buttonAddListenerRouter(notification, declineButton);
    buttonContainer.appendChild(acceptButton);
    buttonContainer.appendChild(declineButton);
    return buttonContainer;
  }

  buttonAddListenerRouter(notification, button) {
    if (notification.type === 'friend_request') {
      if (button.textContent === 'Accept') {
        this.acceptFriendRequestListener(notification, button);
      } else if (button.textContent === 'Decline') {
        this.declineFriendRequestListener(notification, button);
      }
    } else if (notification.type === 'tournament_start') {
      if (button.textContent === 'Accept') {
        this.acceptTournamentRequestListener(notification, button);
      } else if (button.textContent === 'Decline') {
        this.declineTournamentRequestListener(notification, button);
      }
    }
  }

  acceptFriendRequestListener(notification, button) {
    button.addEventListener('click', (e) => {
      fetch('https://localhost:6002/user/friends/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3Mzg1MDUyODksInVzZXJfaWQiOjEsInRva2VuX3R5cGUiOiJhY2Nlc3MifQ.UTLsTUj5PqLoVpE93CY0zy3KaeQqmlqYss3GNtYVKyg07sSnIOzS06ZSWrEHFBpDGmPye8LjDvcIlrpes0-0pDnIVkqNjwiSeyOCJmbZAT3FyqBSszsYet4LNhdav7FgunuMnYEaNUHF-7xlWfUKxlzkfMv_sO_xUNjY2utn-XrzMjWuJoA0s5gvD37RLe4bwJNmuXxrTXRpG80jLakIFY6R9ny1owQktZU6NNCwu5mALqyj6QWSzVTzanEwSgnE8fkWxdVsH1z4xj-y5aI6zhTR04b0FCpOhKkeMJs1DVkkK2drDO3cnxjVqRGmmvr9p3AioVsCfkXSYpqQYA459A',
        },
        body: JSON.stringify({friend_id: notification.data}),
      }).then((response) => {
        if (!response.ok) {
          response.json().then((text) => console.error(text['errors']));
          return;
        }
        return response.json();
      }).then((response) => {
        console.log(response);
        deleteNotification(notification.id);
      });
    });
  }

  declineFriendRequestListener(notification, button) {
    button.addEventListener('click', (e) => {
      fetch('https://localhost:6002/user/friends/', {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3Mzg1MDUyODksInVzZXJfaWQiOjEsInRva2VuX3R5cGUiOiJhY2Nlc3MifQ.UTLsTUj5PqLoVpE93CY0zy3KaeQqmlqYss3GNtYVKyg07sSnIOzS06ZSWrEHFBpDGmPye8LjDvcIlrpes0-0pDnIVkqNjwiSeyOCJmbZAT3FyqBSszsYet4LNhdav7FgunuMnYEaNUHF-7xlWfUKxlzkfMv_sO_xUNjY2utn-XrzMjWuJoA0s5gvD37RLe4bwJNmuXxrTXRpG80jLakIFY6R9ny1owQktZU6NNCwu5mALqyj6QWSzVTzanEwSgnE8fkWxdVsH1z4xj-y5aI6zhTR04b0FCpOhKkeMJs1DVkkK2drDO3cnxjVqRGmmvr9p3AioVsCfkXSYpqQYA459A',
        },
        body: JSON.stringify({friend_id: notification.data}),
      }).then((response) => {
        if (!response.ok) {
          response.json().then((text) => console.error(text['errors']));
          return;
        }
        return response.json();
      }).then((response) => {
        console.log(response);
        deleteNotification(notification.id);
      });
    });
  }

  acceptTournamentRequestListener(notification, button) {
    button.addEventListener('click', (e) => {
      window.location.href = 'https://localhost:6001/tournament/' + notification.data + '/';
      deleteNotification(notification.id);
    });
  }

  declineTournamentRequestListener(notification, button) {
    button.addEventListener('click', (e) => {
      deleteNotification(notification.id);
    });
  }

  deleteNotification(notificationId) {
    fetch('https://localhost:6005/notification/user/' + notificationId + '/', {
      method: 'DELETE',
      headers: {
        // TODO: Get access token from local storage
        'Authorization': '',
      },
    }).then((response) => {
      if (!response.ok) {
        response.json().then((text) => console.error(text['errors']));
      } else {
        const notif = document.getElementById(notificationId);
        notif.remove();
        const count = document.getElementById('bellCount').getAttribute('data-count');
        document.getElementById('bellCount').setAttribute('data-count', parseInt(count) - 1);
      }
    });
  }
}
