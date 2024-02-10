import {Component} from '@components';

export class Home extends Component {
  constructor() {
    super();
  }
  render() {
    return (`
      <navbar-component nav-active="home"></navbar-component>
    `);
  }
  style() {
    return (`
      <style>

      </style>
    `);
  }
}
