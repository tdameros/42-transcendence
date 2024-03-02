import {Component} from '@components';
import {userStatsClient, userManagementClient} from '@utils/api';
import {getRouter} from '@js/Router.js';
import {ErrorPage} from '@utils/ErrorPage.js';

export class UserProfileMatchList extends Component {
  constructor() {
    super();
  }
  render() {
    this.pageNumber = this.getAttribute('page-number') || 1;
    this.pageNumber = parseInt(this.pageNumber);
    return this.renderPlaceholder();
  }

  style() {
    return (`
      <style>
      .hide-placeholder-text {
        color: var(--bs-secondary-bg)!important;
        background-color: var(--bs-secondary-bg)!important;
      }
      
      .avatar-sm {
          width: 2.25rem;
          height: 2.25rem;
      }
      
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
      
      .progress {
          --x-progress-height: .5rem;
          --x-progress-font-size: .85rem;
          --x-progress-bg: #e7eaf0;
          --x-progress-border-radius: 50rem;
          --x-progress-box-shadow: 0 0 0 0 transparent;
          --x-progress-bar-color: #fff;
          --x-progress-bar-bg: #5c60f5;
          --x-progress-bar-transition: width .6s ease;
          height: var(--x-progress-height);
          font-size: var(--x-progress-font-size);
          background-color: var(--x-progress-bg);
          border-radius: var(--x-progress-border-radius);
          box-shadow: var(--x-progress-box-shadow);
          display: flex;
          overflow: hidden;
      }
      
      tbody {
          font-size: .85rem;
          font-weight: 400;
      }
      </style>
    `);
  }

  loadMatchHistory(userId, matchHistory) {
    this.user_id = userId;
    this.innerHTML = this.#renderMatchHistory(matchHistory);

    const paginationElement = this.querySelector('.pagination');
    const paginationLinks = paginationElement.querySelectorAll('a');

    paginationLinks.forEach((link) => {
      super.addComponentEventListener(link, 'click', () => {
        const pageNumber = parseInt(link.getAttribute('page-number'));
        this.loadNewPage(pageNumber);
      });
    });
  }

  #renderMatchHistory(matchHistory) {
    return (`
      <div class="card mb-3 mt-3">
          <div class="card-header border-bottom">
              <h5 class="mb-0">Latest Matches</h5>
          </div>
          <div class="table-responsive">
              <table class="table table-hover table-nowrap mb-1">
                  <thead class="table table-header">
                    <tr>
                        <th scope="col">Adversary</th>
                        <th scope="col">Date</th>
                        <th scope="col">Result</th>
                        <th scope="col">Score</th>
                        <th scope="col">Elo</th>
                        <th scope="col">Winning Chance</th>
                        <th></th>
                    </tr>
                  </thead>
                  <tbody>
                    ${this.#renderMatches(matchHistory)}
                  </tbody>
              </table>
          </div>
          <nav class="d-flex justify-content-center align-items-center">
              ${this.#renderPagination(this.pageNumber, matchHistory['total_pages'])}
          </nav>
      </div>
    `) + this.style();
  }

  #renderMatches(matchHistory) {
    if (matchHistory['history'].length === 0) {
      return (`
        <tr>
          <td class="text-center" colspan="6">
            <div class="m-2 text-secondary text-center" role="alert">
              No matches played yet
            </div>
         </td>
        </tr>
      `);
    }
    return Array.from(matchHistory['history'],
        (match) => this.#renderMatch(match),
    ).join('');
  }

  #renderPagination(currentPage, totalPages) {
    const maxPagesToShow = 3;
    let startPage = Math.max(1, currentPage - Math.floor(maxPagesToShow / 2));
    const endPage = Math.min(totalPages, startPage + maxPagesToShow - 1);
    if (endPage - startPage < maxPagesToShow - 1) {
      startPage = Math.max(1, endPage - maxPagesToShow + 1);
    }
    const previousPage = Math.max(1, currentPage - 1);
    const nextPage = Math.min(totalPages, currentPage + 1);
    const paginationItems = Array.from({length: endPage - startPage + 1},
        (_, i) => this.#renderPageLink(startPage + i,
            startPage + i === currentPage));
    return (`
      <ul class="pagination m-2">
        <li class="page-item">
          <a class="page-link ${previousPage === currentPage ? 'disabled': ''}" aria-label="Previous"
          page-number="${previousPage}">
            <span aria-hidden="true">&laquo;</span>
          </a>
        </li>
        ${paginationItems.join('')}
        <li class="page-item">
          <a class="page-link ${nextPage === currentPage ? 'disabled': ''}" aria-label="Next"
          page-number="${nextPage}">
            <span aria-hidden="true">&raquo;</span>
          </a>
        </li>
      </ul>
    `);
  }

  #renderPageLink(pageNumber, active=false) {
    return (`
    <li class="page-item">
      <a class="page-link ${active ? 'active' : ''}"
      page-number="${pageNumber}">${pageNumber}
      </a>
    </li>
  `);
  }

  async loadNewPage(pageNumber) {
    this.pageNumber = pageNumber;
    this.innerHTML = this.renderPlaceholder();
    const matchHistory = await this.#getMatchHistory(
        this.user_id, pageNumber, 10,
    );
    if (!matchHistory) {
      return;
    }
    if (!await this.#addUsernameInMatchHistory(matchHistory)) {
      return;
    }
    this.loadMatchHistory(this.user_id, matchHistory);
  }

  async #getMatchHistory(userId, pageNumber, pageSize) {
    try {
      const {response, body} = await userStatsClient.getMatchHistory(
          userId, pageNumber, pageSize,
      );
      if (response.ok) {
        return body;
      } else {
        getRouter().redirect('/signin/');
        return false;
      }
    } catch (error) {
      ErrorPage.loadNetworkError();
      return false;
    }
  }

  async #addUsernameInMatchHistory(matchHistory) {
    const opponentsIds = matchHistory['history'].map(
        (match) => parseInt(match['opponent_id']),
    );
    try {
      const {response, body} =
        await userManagementClient.getUsernameListInCache(opponentsIds);
      if (response.ok) {
        matchHistory['history'].forEach((match) => {
          match['opponent_username'] = body[match['opponent_id']];
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

  #renderMatch(match) {
    const date = new Date(match['date']).toLocaleDateString();
    const username = match['opponent_username'];
    return (`
      <tr class="align-middle">
          <td><img alt="..."
                   src="${userManagementClient.getURLAvatar(username)}"
                   class="avatar avatar-sm rounded-circle object-fit-cover me-2">
              <a class="text-heading font-semibold text-decoration-none"
                 onclick="window.router.navigate('/profile/${username}/')">${username}</a>
          </td>
          <td class="">${date}</tdtext-center>
          <td class="">${this.#renderMatchResult(match['result'])}</td>
          <td class="">${match['user_score']} - ${match['opponent_score']}</td>
          <td class="">${this.#renderMatchEloDelta(match['elo_delta'])}</td>
          <td>
              ${this.#renderMatchWinningChance(parseInt(match['expected_result']))}
          </td>
      </tr>
    `);
  }

  #renderMatchResult(isWinningMatch) {
    if (isWinningMatch) {
      return (`
        <span class="badge badge-lg badge-dot">
            <i class="bg-success"></i>
            Win
        </span>
    `);
    } else {
      return (`
        <span class="badge badge-lg badge-dot">
            <i class="bg-danger"></i>
            Lose
        </span>
    `);
    }
  }

  #renderMatchEloDelta(eloChange) {
    if (eloChange > 0) {
      return (`
        <span class="badge badge-pill bg-soft-success text-success me-2"><i
                class="bi bi-arrow-up me-1"></i>+${eloChange} </span>
    `);
    } else {
      return (`
        <span class="badge badge-pill bg-soft-danger text-danger me-2"><i
                class="bi bi-arrow-down me-1"></i>${eloChange} </span>
    `);
    }
  }

  #renderMatchWinningChance(expectedResult) {
    let bgClass = 'bg-warning';
    if (expectedResult < 20) {
      bgClass = 'bg-danger';
    } else if (expectedResult < 40) {
      bgClass = 'bg-warning';
    } else if (expectedResult < 60) {
      bgClass = 'bg-primary';
    } else {
      bgClass = 'bg-success';
    }
    return (`
      <div class="d-flex align-items-center"><span
              class="me-2">${expectedResult}%</span>
          <div>
              <div class="progress"
                   style="width:100px">
                  <div class="progress-bar ${bgClass}"
                       role="progressbar"
                       aria-valuenow="${expectedResult}"
                       aria-valuemin="0"
                       aria-valuemax="100"
                       style="width:${expectedResult}%"></div>
              </div>
          </div>
      </div>
    `);
  }

  renderPlaceholder() {
    const placeholderClass = 'placeholder placeholder-lg ' +
      'bg-body-secondary rounded hide-placeholder-text';
    return (`
            <div class="card mb-3 mt-3 placeholder-glow">
                <div class="card-header border-bottom">
                    <h5 class="mb-0 ${placeholderClass}">Latest games</h5>
                </div>
                <div class="table-responsive">
                    <table class="table table-hover table-nowrap mb-1">
                        <thead class="table table-header">
                        <tr>
                            <th scope="col"><span class="${placeholderClass}">Adversary</span></th>
                            <th scope="col"><span class="${placeholderClass}">Date</span></th>
                            <th scope="col"><span class="${placeholderClass}">Result</span></th>
                            <th scope="col"><span class="${placeholderClass}">Score</span></th>
                            <th scope="col"><span class="${placeholderClass}">Elo</span></th>
                            <th scope="col"><span class="${placeholderClass}">Winning Chance</span></th>
                            <th></th>
                        </tr>
                        </thead>
                        <tbody>
                        ${this.#renderPlaceholderMatches()}
                        </tbody>
                    </table>
                </div>
                <div class="d-flex align-items-center justify-content-center m-2">
                  <span class="${placeholderClass} p-3 col-2"></spanc>
                </div>
            </div>
    `) + this.style();
  }

  #renderPlaceholderMatches(number=10) {
    return Array.from(
        {length: number}, () => this.#renderPlaceholderMatch(),
    ).join('');
  }

  #renderPlaceholderMatch() {
    const placeholderClass = 'placeholder placeholder-lg ' +
      'bg-body-secondary rounded hide-placeholder-text';
    return (`
      <tr class="align-middle">
          <td>
              <span class="${placeholderClass} col-6"></span>
          </td>
          <td><span class="${placeholderClass} col-8">_</span></td>
          <td>
              <span class="${placeholderClass} col-8"></span>
          </td>
          <td>
              <span class="${placeholderClass} col-8"></span>
          </td>
          <td>
              <span class="${placeholderClass} col-8"></span>
          </td>
          <td>
              <span class="${placeholderClass} col-8"></span>
          </td>
      </tr>
    `);
  }
}
