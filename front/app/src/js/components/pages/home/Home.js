import {Component} from '@components';

export class Home extends Component {
  constructor() {
    super();
  }
  render() {
    return (`
      <navbar-component nav-active="home"></navbar-component>
      <friends-sidebar-component main-component="home-content-component"></friends-sidebar-component>
    `);
  }
  style() {
    return (`
      <style>

      </style>
    `);
  }
}
