import {Component} from '@components';
import {userManagementClient} from '@utils/api';
import {ErrorPage} from '@utils/ErrorPage.js';
import {FriendsCache} from '@utils/cache';
import {getRouter} from '@js/Router.js';
import {NavbarUtils} from '@utils/NavbarUtils.js';

export class Friends extends Component {
  constructor() {
    super();
  }

  render() {
    if (FriendsCache.isDefine()) {
      return (this.renderFriends(FriendsCache.getFriends()));
    }
    return (this.renderPlaceholder());
  }

  style() {
    return (`
      <style>
      .badge-dot {
          color: var(--bs-heading-color);
          background: 0 0;
          align-items: center;
          padding: 0;
          font-weight: 400;
          display: inline-flex;
          font-size: .85rem;
      }
      
      .badge-dot.badge-lg i {
          width: .625rem;
          height: .625rem;
      }
      
      .badge-dot i {
          vertical-align: middle;
          width: .375rem;
          height: .375rem;
          border-radius: 50%;
          margin-right: .5rem;
          display: inline-block;
      }
      
      .hide-placeholder-text {
        color: var(--bs-secondary-bg);
        background-color: var(--bs-secondary-bg)!important;
      }
      
      .friend-card {
        transition: transform 0.3s ease;
      }
      .friend-card:hover {
        transform: translateY(-5px);
      } 
      </style>
    `);
  }

  updateFriends() {
    this.innerHTML = this.render() + this.style();
  }

  renderPlaceholder() {
    const placeholderClass = 'placeholder ' +
      'bg-body-secondary rounded hide-placeholder-text';
    return (`
        <div class="card" style="height: calc(100vh - ${NavbarUtils.height}px - 1rem)">
          <div class="card-header">
            <h3>Friends</h3>
          </div>
          <div class="card-body ps-2 pe-2">
        ${Array.from({length: 5}, () => `
    <div class="card friend-card mb-2 bg-body-tertiary placeholder-glow">
      <div class="card-body p-2">
        <div class="d-flex flex-row align-items-center">
          <img src="/img/default_avatar.png" alt="profile image"
               class="rounded-circle object-fit-cover me-2 placeholder placeholder-lg"
               style="width: 45px; height: 45px;">
          <div class="w-100">
              <span class="${placeholderClass} col-8">_</span>
              <span class="${placeholderClass} col-6" style="height: 18px">_</span>
          </div>
        </div>
      </div>
    </div>
     `).join('')}
        </div>
      </div>
    `);
  }

  renderFriends(friends) {
    if (friends.size === 0) {
      return (`
      <div class="card" style="height: calc(100vh - ${NavbarUtils.height}px - 1rem)">
        <div class="card-header">
          <h3>Friends</h3>
        </div>
        <div class="card-body ps-2 pe-2">
          <div class="mt-2 text-secondary text-center" role="alert">
            No friends yet
          </div>
        </div>
      </div>
    `);
    }
    return (`
      <div class="card overflow-auto" style="height: calc(100vh - ${NavbarUtils.height}px - 1rem)">
        <div class="card-header">
          <h3>Friends</h3>
        </div>
        <div class="card-body ps-2 pe-2">
            ${this.renderFriendCards(friends)}
        </div>
      </div>
    `);
  }


  renderFriendCards(friends) {
    const onlineFriendCards = [];
    const offlineFriendCards = [];
    const unknownFriendCards = [];
    const pendingFriendCards = [];

    friends.forEach((friend, userId) => {
      if (friend['connected_status'] === 'online') {
        onlineFriendCards.push(this.renderFriendCard(friend));
      } else if (friend['connected_status'] === 'offline') {
        offlineFriendCards.push(this.renderFriendCard(friend));
      } else if (friend['status'] !== 'pending' &&
          friend['connected_status'] === 'unknown') {
        unknownFriendCards.push(this.renderFriendCard(friend));
      } else if (friend['status'] === 'pending') {
        pendingFriendCards.push(this.renderFriendCard(friend));
      }
    });
    return onlineFriendCards.join('') + offlineFriendCards.join('') +
      unknownFriendCards.join('') + pendingFriendCards.join('');
  }

  renderFriendCard(friend) {
    const opacity = friend['status'] == 'pending' ? '0.5' : '1';
    const username = friend['username'];
    return (`
    <div class="card friend-card mb-2 bg-body-tertiary" style="opacity: ${opacity};"
         onclick="window.router.navigate('/profile/${username}/')">
      <div class="card-body p-2">
        <div class="d-flex flex-row align-items-center">
          <img src="${userManagementClient.getURLAvatar(username)}" alt="profile image"
               class="rounded-circle object-fit-cover me-2"
               style="width: 45px; height: 45px;">
            <div>
              <p class="m-0">@${friend['username']}</p>
              ${this.renderFriendOnlineStatus(friend)}
            </div>
        </div>
      </div>
    </div>
  `);
  }

  renderFriendOnlineStatus(friend) {
    let backgroundStatus;
    if (friend['connected_status'] === 'online') {
      backgroundStatus = 'bg-success';
    } else if (friend['connected_status'] === 'offline') {
      backgroundStatus = 'bg-danger';
    } else {
      backgroundStatus = 'bg-secondary';
    }
    let textStatus;
    if (friend['status'] === 'pending') {
      textStatus = 'Pending';
    } else {
      textStatus = friend['connected_status'].charAt(0).toUpperCase() +
                   friend['connected_status'].slice(1);
    }
    return (`
        <span class="badge badge-lg badge-dot">
          <i class="${backgroundStatus}"></i>
          <p class="text-muted m-0">${textStatus}</p>
        </span>
    `);
  }

  async postRender() {
    try {
      const {response, body} = await userManagementClient.getFriends();
      if (response.ok) {
        if (!await this.#addUsernameInFriends(body['friends'])) {
          return;
        }
        this.storeFriendsCache(body['friends']);
        this.updateFriends();
      }
    } catch (error) {
      ErrorPage.loadNetworkError();
    }
  }

  storeFriendsCache(friendsList) {
    FriendsCache.defineIfNot();
    friendsList.forEach((friend) => {
      const lastFriendCache = FriendsCache.get(friend.id);
      if (lastFriendCache) {
        friend['connected_status'] =
          lastFriendCache['connected_status'];
      } else {
        friend['connected_status'] = 'unknown';
      }
      return FriendsCache.set(friend.id, friend);
    });
  }

  async #addUsernameInFriends(friends) {
    const friendIds = friends.map((friend) => parseInt(friend.id));
    try {
      const {response, body} =
        await userManagementClient.getUsernameListInCache(friendIds);
      if (response.ok) {
        friends.forEach((friend) => {
          friend['username'] = body[friend.id];
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
