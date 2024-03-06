import {Component} from '@components';
import {userManagementClient} from '@utils/api';
import {getRouter} from '@js/Router.js';
import {ErrorPage} from '@utils/ErrorPage.js';

export class SearchNav extends Component {
  constructor() {
    super();
  }

  render() {
    return (`
      <div class="position-relative z-1">
          <form id="search-form" class="d-flex" role="search">
              <input id="search-bar" class="form-control" type="search"
                     placeholder="Search users..." aria-label="Search" autocomplete="off">
          </form>
          <div id="search-results" class="rounded">
          </div>
      </div>
    `);
  }

  style() {
    return (`
      <style>
      #search-results {
          position: absolute;
          width: 100%;
          max-height: 200px;
          overflow-y: auto;
          display: none;
          z-index: 2; 
      }
        
      .result-item {
          cursor: pointer;
          background-color: var(--bs-body-bg);
          border: 1px solid var(--bs-border-color);
      }
      </style>
    `);
  }

  postRender() {
    this.searchBar = this.querySelector('#search-bar');
    super.addComponentEventListener(
        this.searchBar, 'input', this.#searchBarHandler,
    );
    super.addComponentEventListener(
        document, 'click', this.#DOMClickHandler,
    );
    this.searchResults = this.querySelector('#search-results');
    this.searchForm = this.querySelector('#search-form');
    super.addComponentEventListener(
        this.searchForm, 'submit', this.#searchFormHandler,
    );
  }

  async #searchBarHandler(event) {
    if (event.target.value.length < 2) {
      this.searchResults.style.display = 'none';
      return;
    }
    try {
      const {response, body} = await userManagementClient.searchUsername(
          event.target.value,
      );
      this.searchResults.innerHTML = '';
      if (response.ok) {
        this.searchResults.innerHTML = this.#renderSearchResults(body['users']);
        if (body['users'].length > 0) {
          this.searchResults.style.display = 'block';
        } else {
          this.searchResults.style.display = 'none';
        }
      }
    } catch (error) {
      ErrorPage.loadNetworkError();
    }
  }

  #renderSearchResults(users) {
    return (users.slice(0, 3).map((username) => {
      return (`
      <div class="result-item p-1" onclick="window.router.navigate('/profile/${username}/')" username="${username}">
        <img src="${userManagementClient.getURLAvatar(username)}" alt="profile image" class="rounded-circle object-fit-cover" style="width: 40px; height: 40px;">
        ${username}
      </div>
    `);
    }).join(''));
  }

  #DOMClickHandler(event) {
    if (this.searchResults &&
      !this.searchResults.contains(event.target) &&
      event.target !== this.searchBar) {
      this.searchResults.style.display = 'none';
    }
  }

  #searchFormHandler(event) {
    event.preventDefault();
    const username = this.searchBar.value;
    if (username.length > 0) {
      getRouter().navigate(`/profile/${username}/`);
    }
  }
}
