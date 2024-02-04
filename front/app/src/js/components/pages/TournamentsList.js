import {Component} from '../Component.js';
import {Cookies} from '../../Cookies.js';

export class TournamentsList extends Component {
  static privateCheckBoxId = 'private-check-box';
  static finishedCheckBoxId = 'finished-check-box';
  static privateCheckBoxCookie = 'private-check-box';
  static finishedCheckBoxCookie = 'finished-check-box';

  constructor() {
    super();
    this.tournaments = [];
  }

  render() {
    return (`
      <div class="card mb-3 mt-3">
          <div class="card-header border-bottom d-flex align-items-center justify-content-between">
            <div class="d-flex justify-content-start">
              <li class="list-group-item d-flex m-2">
                  <input class="form-check-input me-1" type="checkbox" value=""
                         id="${TournamentsList.privateCheckBoxId}"
                         ${Cookies.get(TournamentsList.privateCheckBoxCookie) === 'true' ? 'checked': ''}>
                  <label class="form-check-label" for="private-check-box">private</label>
              </li>
              <li class="list-group-item d-flex m-2">
                  <input class="form-check-input me-1" type="checkbox" value=""
                         id="${TournamentsList.finishedCheckBoxId}"
                         ${Cookies.get(TournamentsList.finishedCheckBoxCookie) === 'true' ? 'checked': ''}>
                  <label class="form-check-label" for="finished-check-box">finished</label>
              </li>
            </div>
            <button type="button" class="btn btn-outline-success btn-sm" onclick="window.router.navigate('/tournaments/create/')">Create</button>
          </div>
          <div class="table-responsive">
              <table class="table table-hover table-nowrap mb-1">
                  <thead class="table table-header">
                  <tr>
                      <th scope="col">Name</th>
                      <th scope="col">Admin</th>
                      <th scope="col">Status</th>
                      <th scope="col">Players</th>
                  </tr>
                  </thead>
                  <tbody>
                    ${this.#generateTrPlaceHolders(10)}
                  </tbody>
              </table>
          </div>
          <nav class="d-flex justify-content-center">
          </nav>
      </div>
    `);
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
        
        tbody {
            font-size: .85rem;
            font-weight: 400;
        }
        
        .card-header {
            background-color: rgba(var(--bs-emphasis-color-rgb), 0.025);
        }
        
        .icon-shape {
            width: 3rem;
            height: 3rem;
            display: flex;
            justify-content: center;
            align-items: center;
        }
      </style>
    `);
  }

  async postRender() {
    this.tbody = this.querySelector('tbody');
    this.pagination = this.querySelector('nav');
  }

  updateTournamentsList(tournaments, page, nbPages) {
    this.tbody.innerHTML = this.#generateTrTournaments(tournaments);
    this.pagination.innerHTML = this.#generatePagination(page, nbPages);
  }
  #generatePagination(currentPage, totalPages) {
    const maxPagesToShow = 3;
    let startPage = Math.max(1, currentPage - Math.floor(maxPagesToShow / 2));
    const endPage = Math.min(totalPages, startPage + maxPagesToShow - 1);
    if (endPage - startPage < maxPagesToShow - 1) {
      startPage = Math.max(1, endPage - maxPagesToShow + 1);
    }
    const previousPage = Math.max(1, currentPage - 1);
    const nextPage = Math.min(totalPages, currentPage + 1);
    const paginationItems = Array.from({length: endPage - startPage + 1},
        (_, i) => this.#generatePageLink(startPage + i,
            startPage + i === currentPage));
    return (`
      <ul class="pagination m-2">
        <li class="page-item">
          <a class="page-link" aria-label="Previous"
          onclick="window.router.navigate('/tournaments/page/${previousPage}')">
            <span aria-hidden="true">&laquo;</span>
          </a>
        </li>
        ${paginationItems.join('')}
        <li class="page-item">
          <a class="page-link" aria-label="Next"
          onclick="window.router.navigate('/tournaments/page/${nextPage}')">
            <span aria-hidden="true">&raquo;</span>
          </a>
        </li>
      </ul>
    `);
  }

  #generatePageLink(pageNumber, active=false) {
    return (`
    <li class="page-item">
      <a class="page-link ${active ? 'active' : ''}"
      onclick="window.router.navigate('/tournaments/page/${pageNumber}')">${pageNumber}
      </a>
    </li>
  `);
  }

  #generateTrPlaceHolders(number=10) {
    return Array.from({length: number}, () => `
      <tr class="placeholder-glow">
        <td><span class="placeholder bg-body-secondary col-12 placeholder-lg"></span></td>
        <td><span class="placeholder bg-body-secondary col-12 placeholder-lg"></span></td>
        <td><span class="placeholder bg-body-secondary col-12 placeholder-lg"></span></td>
        <td><span class="placeholder bg-body-secondary col-12 placeholder-lg"></span></td>
      </tr>
    `).join('');
  }

  #generateTrTournaments(tournaments) {
    if (tournaments.length === 0) {
      return (`
        <tr>
          <td class="text-center" colspan="4">
        <div class="alert alert-warning" role="alert">
          No tournaments created yet
        </div>
          </td>
        </tr>
      `);
    }
    return Array.from(tournaments,
        (tournament) => this.#generateTournament(tournament)).join('');
  }

  #generateTournament(tournament) {
    return (`
    <tr class="align-middle tournament-row" tournament-id="${tournament['id']}">
      <td>
        ${tournament['name']}
      </td>
      <td>
        <a class="text-primary text-decoration-none">${tournament['admin']}</a>
      </td>
      ${this.#generateStatus(tournament['status'])}
      ${this.#generatePlayers(
          tournament['nb-players'],
          tournament['max-players'],
          tournament['is-private'])
      }
    </tr>
    `);
  }

  #generateStatus(status) {
    const statusClasses = {
      'Created': 'bg-success',
      'In progress': 'bg-warning',
      'default': 'bg-danger',
    };
    const background = statusClasses[status] || statusClasses['default'];
    return (`
    <td>
      <span class="badge badge-lg badge-dot">
        <i class="${background}"></i>${status}
      </span>
    </td>
  `);
  }

  #generatePlayers(nbPlayers, maxPlayers, isPrivate) {
    const playersText = `${nbPlayers}/${maxPlayers}`;
    return (`
      <td>
        ${playersText}
        ${isPrivate ? '<i class="bi bi-lock-fill"></i>' : ''}
      </td>
    `);
  }
}
