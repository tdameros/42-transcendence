import {Component} from '@components';
import {ErrorPage} from '@utils/ErrorPage.js';

export class NotFound extends Component {
  constructor() {
    super();
  }
  render() {
    ErrorPage.loadNotFound();
    return (``);
  }
  style() {
    return (`
      <style>

      </style>
    `);
  }
}
