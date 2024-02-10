import {Component} from '@components';
import {userManagementClient} from '@utils/api';

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
                    <img src="/img/default_avatar.jpeg" alt="Profile picture"
                         class="profile-img mr-2 placeholder placeholder-lg">
                </div>
                <div class="user-info">
                    <h1 class="mt-4 ${placeholderClass} col-12">_</h1>
                    <div class="d-flex">
                        <button class="btn btn-sm me-2 ${placeholderClass}">
                            Follow
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
          <button class="btn btn-sm btn-outline-success me-2">
              Follow
          </button>
          <button class="btn btn-sm btn-outline-secondary">
              Challenge
          </button>
      </div>
    `);
  }

  loadUserProfile(username) {
    this.headerContainer = this.querySelector('#header-container');
    if (this.headerContainer) {
      this.headerContainer.classList.remove('placeholder-glow');
    }
    this.profileInfo = this.querySelector('#profile-info');
    if (this.profileInfo) {
      this.profileInfo.innerHTML = this.renderProfileInfo(
          username, '/img/tdameros.jpg',
          username === userManagementClient.username,
      );
    }
  }
}
