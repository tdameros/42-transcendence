import {Component} from '@components';
import {userManagementClient} from '@utils/api';
import {ErrorPage} from '@utils/ErrorPage.js';
import {FriendsCache} from '@utils/cache';

export class UserProfileHeader extends Component {
  constructor() {
    super();
  }

  render() {
    return this.renderPlaceholder();
  }
  style() {
    return (`
      <style>
      .banner {
          width: 100%;
          height: 17vh;
          object-fit: cover;
          position: relative;
      }
      
      .profile-info {
          gap: 10px;
          transform: translateY(-20%);
      }
      
      .profile-img-container {
          margin-left: 50px;
          border: 3px solid var(--bs-body-bg);
          border-radius: 50%;
          overflow: hidden;
      }
      
      .profile-img {
          width: 15vw;
          height: 15vw;
          min-width: 85px;
          min-height: 85px;
          max-width: 125px;
          max-height: 125px;
          object-fit: cover;
          border-radius: 50%;
      }
      
      @media (max-width: 650px) {
            .user-info {
              font-size: 1rem;
            }
      }
      </style>
    `);
  }

  renderPlaceholder() {
    const placeholderClass = 'placeholder placeholder-lg' +
      'bg-body-secondary rounded hide-placeholder-text';
    return (`
      <div id="header-container" class="profile-card card rounded placeholder-glow">
        <div class="card-body p-0">
            <div class="banner">
                <img src="/img/user_profile_banner.jpg" alt="Profile banner"
                     class="banner img-fluid vh-10 rounded-top">
            </div>
            <div id="profile-info" class="profile-info d-flex align-items-center">
                <div id="picture-container" class="profile-img-container ">
                    <img src="/img/default_avatar.png" alt="Profile picture"
                         class="profile-img mr-2 placeholder placeholder-lg">
                </div>
                <div class="user-info">
                    <h1 class="mt-4 ${placeholderClass} col-12">_</h1>
                    <div class="d-flex">
                        <button class="btn btn-sm me-2 ${placeholderClass}">
                            Send Friend Request
                        </button>
                        <button class="btn btn-sm ${placeholderClass}">
                            Challenge
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
   `);
  }

  renderProfileInfo(username, profilePicture, isYourProfile = false) {
    return (`
      <div class="profile-img-container">
          <img id="profile-picture" src="${profilePicture}" alt="Profile picture"
               class="profile-img mr-2">
      </div>
      <div class="user-info">
          <h1 class="mt-4">@${username}</h1>
          ${isYourProfile ? '' : this.renderProfileInteractionButtons()}
      </div>
    `);
  }

  renderProfileInteractionButtons() {
    return (`
      <div class="d-flex">
        ${this.#renderFriendButton()}
          <button class="btn btn-sm btn-outline-secondary">
              Challenge
          </button>
      </div>
    `);
  }

  loadUserProfile(username, userId) {
    this.userId = userId;
    this.username = username;
    this.headerContainer = this.querySelector('#header-container');
    if (this.headerContainer) {
      this.headerContainer.classList.remove('placeholder-glow');
    }
    this.profileInfo = this.querySelector('#profile-info');
    if (this.profileInfo) {
      this.profileInfo.innerHTML = this.renderProfileInfo(
          username, `${userManagementClient.getURLAvatar(username)}`,
          username === userManagementClient.username,
      );
      this.friendActionBtn = this.querySelector('#friend-action-btn');
      super.addComponentEventListener(
          this.friendActionBtn, 'click', this.#friendActionHandler,
      );
      super.addComponentEventListener(
          document, FriendsCache.event, () => {
            if (this.friendActionBtn) {
              this.friendActionBtn.outerHTML = this.#renderFriendButton();
              this.friendActionBtn = this.querySelector('#friend-action-btn');
              super.addComponentEventListener(
                  this.friendActionBtn, 'click', this.#friendActionHandler,
              );
            }
          },
      );
    }
  }

  #renderFriendButton() {
    const friend = FriendsCache.get(this.userId);
    if (!friend) {
      return (`
        <button id="friend-action-btn" friend-action="send-request" class="btn btn-sm btn-success me-2">
            Send Friend Request
        </button>
      `);
    } else if (friend['status'] === 'pending') {
      return (`
        <button id="friend-action-btn" class="btn btn-sm btn-success me-2" disabled>
            Friend Request Sent
        </button>
      `);
    } else {
      return (`
        <button id="friend-action-btn" friend-action="remove-friend" class="btn btn-sm btn-danger me-2">
          Remove Friend
        </button>
      `);
    }
  }

  async #friendActionHandler() {
    const action = this.friendActionBtn.getAttribute('friend-action');
    if (action === 'send-request') {
      await this.#addFriend();
    } else if (action === 'remove-friend') {
      await this.#removeFriend();
    }
  }

  async #addFriend() {
    try {
      const {response} = await userManagementClient.sendFriendRequest(
          this.userId,
      );
      if (response.ok) {
        FriendsCache.set(this.userId, {
          'id': this.userId,
          'username': this.username,
          'status': 'pending',
          'connected_status': 'unknow',
        });
        document.querySelector('friends-component').updateFriends();
      }
    } catch {
      ErrorPage.loadNetworkError();
    }
  }

  async #removeFriend() {
    try {
      const {response} = await userManagementClient.removeFriend(
          this.userId,
      );
      if (response.ok) {
        FriendsCache.delete(this.userId);
        document.querySelector('friends-component').updateFriends();
      }
    } catch {
      ErrorPage.loadNetworkError();
    }
  }
}
