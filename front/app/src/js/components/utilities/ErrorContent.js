import {Component} from '@components';
import {NavbarUtils} from '@utils/NavbarUtils.js';

export class ErrorContent extends Component {
  constructor() {
    super();
  }
  render() {
    const message = this.getAttribute('message');
    const refresh = this.getAttribute('refresh');
    return (`
      <div id="error" class="d-flex flex-column justify-content-center align-items-center rounded-3">
        <div class="icon-error">
            <i class="bi bi-exclamation-circle"></i>
        </div>
        <h1 class="text-center">Oops! Something went wrong</h1> 
        <h4 class="text-center text-secondary">${message}</h4>
        ${refresh === 'true' ? '<button class="btn btn-primary" onclick="location.reload()">Refresh</button>' : ''}
      </div>
    `);
  }
  style() {
    return (`
      <style>
        #error {
          height: calc(100vh - ${NavbarUtils.height}px);
        }
        
        .icon-error {
            font-size: 4rem;
        }
      </style>
    `);
  }
}
