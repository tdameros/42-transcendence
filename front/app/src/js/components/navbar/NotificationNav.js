import {Component} from '@components';
import {userManagementClient} from '@utils/api/index.js';
import {getRouter} from '@js/Router.js';
import {ErrorPage} from '@utils/ErrorPage.js';

export class NotificationNav extends Component {
  constructor() {
    super();
  }

  render() {
    return (`
    <div class="position-relative z-1">
        <div id="bell-btn" class="btn btn-sm icon-btn">
          <i id="bell-icon" class="bi-bell-fill fs-5 bell-counter"></i>
        </div>
        <div id="notification-list" class="border rounded" style="display: none">
        </div>
    </div>
    <div class="toast-container position-relative">
    `);
  }

  style() {
    return (`
      <style>
      #notification-list {
          position: absolute;
          width: 300px;
          top: 43px;
          left: -280px;
          background-color: var(--bs-body-bg);
          max-height: 300px;
          overflow-y: auto;
          display: none;
          z-index: 2;
      }
      
      @media (max-width: 1000px) {
          #notification-list {
              left: 0px;
          }
      }
      
      .bell-counter[data-count]:after {
          position: absolute;
          right: 0%;
          top: 1%;
          content: attr(data-count);
          font-size: 40%;
          padding: .6em;
          border-radius: 999px;
          line-height: .75em;
          color: white;
          background: var(--bs-danger);
          text-align: center;
          min-width: 2em;
          font-weight: bold;
      }
      
      .btn-little {
        padding: 0.25rem 0.5rem;
        font-size: 0.75rem;
        line-height: 1.5;
        border-radius: 0.2rem;
      }
        
      .notification:hover {
        background-color: var(--bs-secondary-bg);
      }
      
      .icon-btn {
         cursor: pointer;
         padding: 0.16rem 0.6rem;
      }
      
      .icon-btn:hover {
        background-color: var(--bs-body-bg);
        border: var(--bs-border-width) solid var(--bs-border-color);
      }
      
      .icon-btn:active {
        border-color: var(--bs-border-color)!important;
      }
      </style>
    `);
  }

  async postRender() {
    this.notificationComponent = document.querySelector(
        'notification-component',
    );
    if (this.notificationComponent) {
      this.notifications = this.notificationComponent.notifications;
    } else {
      this.notifications = [];
    }
    this.bellIcon = this.querySelector('#bell-icon');
    this.bellBtn = this.querySelector('#bell-btn');
    super.addComponentEventListener(
        this.bellBtn, 'click', this.#toggleNotification,
    );
    this.notificationList = this.querySelector('#notification-list');
    super.addComponentEventListener(document, 'click', this.#DOMClickHandler);
    if (await this.#generateNotifications(this.notifications)) {
      this.#updateBellCount(this.notifications.length);
    }
  }

  #DOMClickHandler(event) {
    if (this.notificationList &&
      !this.notificationList.contains(event.target) &&
      !this.bellBtn.contains(event.target)) {
      this.notificationList.style.display = 'none';
    }
  }

  #updateBellCount(newCount) {
    if (newCount > 0) {
      this.bellIcon.setAttribute('data-count', newCount);
    } else {
      this.bellIcon.removeAttribute('data-count');
    }
  }

  #toggleNotification() {
    if (this.notificationComponent.notifications.length === 0 ||
      this.notificationList.style.display === 'block') {
      this.notificationList.style.display = 'none';
    } else {
      this.notificationList.style.display = 'block';
    }
  }

  async addNotification(notification) {
    if (!await this.#addUsernameInFriendRequestNotifications([notification])) {
      return false;
    }
    this.notificationList.appendChild(this.#generateNotification(notification));
    const currentCount = this.bellIcon.getAttribute('data-count') ?
      parseInt(this.bellIcon.getAttribute('data-count')): 0;
    this.#updateBellCount(currentCount + 1);
    this.#updateBellCount(this.notificationComponent.notifications.length);
  }

  async #generateNotifications(notifications) {
    if (!await this.#addUsernameInFriendRequestNotifications(notifications)) {
      return false;
    }
    for (const notification of notifications) {
      this.notificationList.appendChild(
          this.#generateNotification(notification),
      );
    }
    return true;
  }

  #generateNotification(notification) {
    if (notification.type === 'friend_request') {
      return this.#generateFriendRequestNotification(notification);
    } else if (notification.type === 'tournament_start') {
      return this.#generateTournamentStartNotification(notification);
    }
  }

  #generateFriendRequestNotification(notification) {
    notification.data = parseInt(notification.data);
    const username = notification['sender_username'];
    const profileUrl = `/profile/${username}/`;
    const notificationDiv = document.createElement('div');
    notificationDiv.setAttribute('notification-id', notification.id);
    notificationDiv.classList.add('p-2', 'rounded', 'notification');
    notificationDiv.innerHTML = `
      <div class="d-flex justify-content-start align-items-center">
          <div class="d-flex align-items-center mb-1">
              <img src="/img/tdameros.jpg" alt="profile image"
                   class="rounded-circle me-2"
                   style="width: 40px; height: 40px; min-height: 40px; min-width: 40px">
              <p class="mb-0 text-muted" style="font-size: 0.8rem;">
                  <a class="text-primary text-decoration-none" onclick="window.router.navigate('${profileUrl}')">${username}</a>
                  wants to be friends with you
              </p>
          </div>
      </div>
      <div class="d-flex justify-content-around">
          <button class="btn btn-little btn-success w-100 me-1">Accept</button>
          <button class="btn btn-little btn-danger w-100 ms-1">Decline</button>
      </div>
    `;
    const acceptButton = notificationDiv.querySelector('.btn-success');
    const declineButton = notificationDiv.querySelector('.btn-danger');

    super.addComponentEventListener(acceptButton, 'click', () => {
      this.#acceptFriendRequest(notification);
    });
    super.addComponentEventListener(declineButton, 'click', () => {
      this.#declineFriendRequest(notification);
    });
    return notificationDiv;
  }

  async #acceptFriendRequest(notification) {
    try {
      const {response} = await userManagementClient.addFriend(
          notification.data,
      );
      if (response.ok || response.status !== 401) {
        this.removeNotification(notification);
      } else {
        getRouter().redirect('/signin/');
      }
    } catch (error) {
      ErrorPage.loadNetworkError();
    }
  }

  async #declineFriendRequest(notification) {
    try {
      const {response} = await userManagementClient.deleteFriend(
          notification.data,
      );
      if (response.ok || response.status !== 401) {
        this.removeNotification(notification);
      } else {
        getRouter().redirect('/signin/');
      }
    } catch (error) {
      ErrorPage.loadNetworkError();
    }
  }

  #generateTournamentStartNotification(notification) {
    const notificationDiv = document.createElement('div');
    notificationDiv.setAttribute('notification-id', notification.id);
    notificationDiv.classList.add('p-2', 'rounded', 'notification');
    notificationDiv.innerHTML = `
      <div class="d-flex justify-content-start align-items-center">
          <div class="d-flex align-items-center mb-1">
          <div class="me-2">
           <i class="bi bi-trophy-fill rounded-circle fs-3" ></i>
          </div>
              <p class="mb-0 text-muted" style="font-size: 0.8rem;">
                  Tournament 
                  <a class="text-primary text-decoration-none" onclick="window.router.navigate('/game/${notification.data}/')">${notification.title}</a>
                  has started
              </p>
          </div>
      </div>
      <button class="btn btn-little btn-primary w-100 me-1">Join</button>
    `;
    const joinButton = notificationDiv.querySelector('.btn-primary');

    super.addComponentEventListener(joinButton, 'click', () => {
      this.#joinTournament(notification);
    });
    return notificationDiv;
  }

  #joinTournament(notification) {
    this.removeNotification(notification);
    getRouter().navigate(`/game/${notification.data}/`);
  }

  removeNotification(notification) {
    this.notificationList.removeChild(
        this.querySelector(`div[notification-id="${notification.id}"]`),
    );
    this.notificationComponent.removeNotification(notification);
    this.#updateBellCount(this.notificationComponent.notifications.length);
    if (this.notificationComponent.notifications.length === 0) {
      this.notificationList.style.display = 'none';
    }
  }

  async #addUsernameInFriendRequestNotifications(notifications) {
    const senderIds = notifications.filter(
        (notification) => notification.type === 'friend_request',
    ).map((notification) => notification.data);
    try {
      const {response, body} = await userManagementClient.getUsernameList(
          senderIds,
      );
      if (response.ok) {
        notifications.forEach((notification) => {
          notification['sender_username'] = body[notification.data];
        });
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
}
