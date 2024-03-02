import {Component} from '@components';
import {userStatsClient, userManagementClient} from '@utils/api';
import {getRouter} from '@js/Router.js';
import {ErrorPage} from '@utils/ErrorPage.js';

export class RankingContent extends Component {
  static pageSize = 50;

  constructor() {
    super();
  }
  render() {
    this.pageId = this.getAttribute('pageId') || 1;
    this.pageId = parseInt(this.pageId);
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

  async postRender() {
    const rankingPage = await this.#getRankingPage(this.pageId);
    if (rankingPage !== false) {
      this.innerHTML = this.#renderRankingPage(rankingPage);
    }
  }

  async #getRankingPage(pageId) {
    try {
      const {response, body} = await userStatsClient.getRanking(
          pageId, RankingContent.pageSize,
      );
      if (response.ok) {
        if (await this.#addUsernameInRanking(body['ranking'])) {
          this.#addRankPositions(body, pageId);
          return body;
        }
        return false;
      } else {
        getRouter().redirect('/signin/');
        return false;
      }
    } catch (e) {
      ErrorPage.loadNetworkError();
      return false;
    }
  }

  async #addUsernameInRanking(ranking) {
    const userIds = ranking.map((user) => parseInt(user.id));
    try {
      const {response, body} =
        await userManagementClient.getUsernameListInCache(userIds);
      if (response.ok) {
        ranking.forEach((user) => {
          user['username'] = body[user.id];
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

  #addRankPositions(ranking, pageId) {
    const firstPosition = (pageId - 1) * RankingContent.pageSize + 1;
    ranking['ranking'].forEach((user, index) => {
      user['rank'] = firstPosition + index;
    });
  }

  #renderRankingPage(ranking) {
    return (`
      <div class="card m-2">
          <div class="card-header border-bottom">
              <h5 class="mb-0">Ranking</h5>
          </div>
          <div class="table-responsive">
              <table class="table table-hover table-nowrap table-striped mb-1">
                  <thead class="table table-header">
                    <tr>
                        <th scope="col" class="col">Player</th>
                        <th scope="col" class="text-center">Elo</th>
                        <th scope="col" class="text-center">Win Rate</th>
                        <th scope="col" class="text-center">Matches Played</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${this.#renderRankingRows(ranking)}
                  </tbody>
              </table>
          </div>
          <nav class="d-flex justify-content-center align-items-center">
              ${this.#renderPagination(this.pageId, ranking['total_pages'])}
          </nav>
      </div>
    `) + this.style();
  }

  #renderRankingRows(ranking) {
    if (ranking['ranking'].length === 0) {
      return (`
        <tr>
          <td class="text-center" colspan="6">
            <div class="m-2 text-secondary text-center" role="alert">
              No players found
            </div>
         </td>
        </tr>
      `);
    }
    return Array.from(ranking['ranking'],
        (row) => this.#renderRankingRow(row),
    ).join('');
  }

  #renderRankingRow(row) {
    const username = row['username'];
    return (`
      <tr class="align-middle">
          <td>
            <div class="d-flex align-items-center">
              <p class="m-0">#${row['rank']}</p>
              <img alt="..."
                   src="${userManagementClient.getURLAvatar(username)}"
                   class="avatar avatar-sm rounded-circle object-fit-cover ms-2 me-2">
              <a class="text-heading font-semibold text-decoration-none"
                 onclick="window.router.navigate('/profile/${username}/')">${username}</a>
            </div>
          </td>
          <td class="text-center">${row['elo']}</td>
          <td class="text-center">
              ${this.#renderRankWinRate(parseInt(row['win_rate']))}
          </td>
          <td class="text-center">${row['matches_played']}</td>
      </tr>
    `);
  }

  #renderRankWinRate(winRate) {
    let bgClass = 'bg-warning';
    if (winRate < 20) {
      bgClass = 'bg-danger';
    } else if (winRate < 40) {
      bgClass = 'bg-warning';
    } else if (winRate < 60) {
      bgClass = 'bg-primary';
    } else {
      bgClass = 'bg-success';
    }
    return (`
      <div class="d-flex align-items-center justify-content-center"><span
              class="me-2">${winRate}%</span>
          <div>
              <div class="progress"
                   style="width:100px">
                  <div class="progress-bar ${bgClass}"
                       role="progressbar"
                       aria-valuenow="${winRate}"
                       aria-valuemin="0"
                       aria-valuemax="100"
                       style="width:${winRate}%"></div>
              </div>
          </div>
      </div>
    `);
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
          onclick="window.router.navigate('/ranking/page/${previousPage}/')">
            <span aria-hidden="true">&laquo;</span>
          </a>
        </li>
        ${paginationItems.join('')}
        <li class="page-item">
          <a class="page-link  ${nextPage === currentPage ? 'disabled': ''}" aria-label="Next"
          onclick="window.router.navigate('/ranking/page/${nextPage}/')">
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
      onclick="window.router.navigate('/ranking/page/${pageNumber}/')">${pageNumber}
      </a>
    </li>
  `);
  }

  renderPlaceholder() {
    const placeholderClass = 'placeholder placeholder-lg ' +
      'bg-body-secondary rounded hide-placeholder-text';
    return (`
            <div class="card m-2 placeholder-glow">
                <div class="card-header border-bottom">
                    <h5 class="mb-0 ${placeholderClass}">Ranking</h5>
                </div>
                <div class="table-responsive">
                    <table class="table table-hover table-nowrap mb-1">
                        <thead class="table table-header">
                        <tr>
                            <th scope="col"><span class="${placeholderClass}">Player</span></th>
                            <th scope="col"><span class="${placeholderClass}">Elo</span></th>
                            <th scope="col"><span class="${placeholderClass}">Win Rate</span></th>
                            <th scope="col"><span class="${placeholderClass}">Matches Played</span></th>
                        </tr>
                        </thead>
                        <tbody>
                        ${this.#renderPlaceholderRankingRows()}
                        </tbody>
                    </table>
                </div>
                <div class="d-flex align-items-center justify-content-center m-2">
                  <span class="${placeholderClass} p-3 col-2"></spanc>
                </div>
            </div>
    `) + this.style();
  }

  #renderPlaceholderRankingRows(number=50) {
    return Array.from(
        {length: number}, () => this.#renderPlaceholderRankingRow(),
    ).join('');
  }

  #renderPlaceholderRankingRow() {
    const placeholderClass = 'placeholder placeholder-lg ' +
      'bg-body-secondary rounded hide-placeholder-text';
    return (`
      <tr class="align-middle">
          <td>
              <span class="${placeholderClass} col-8"></span>
          </td>
          <td><span class="${placeholderClass} col-8">_</span></td>
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
