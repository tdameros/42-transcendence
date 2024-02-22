import {Component} from '@components';

export class Local extends Component {
  constructor() {
    super();
  }
  render() {
    return (`
      <navbar-component nav-active="singleplayer"></navbar-component>
      <friends-sidebar-component main-component="local-content-component"></friends-sidebar-component>
    `);
  }
  style() {
    return (`
      <style>

      </style>
    `);
  }
}
