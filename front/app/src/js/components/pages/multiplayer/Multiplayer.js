import {Component} from '@components';

export class Multiplayer extends Component {
  constructor() {
    super();
  }
  render() {
    return (`
      <navbar-component nav-active="multiplayer"></navbar-component>
      <friends-sidebar-component main-component="multiplayer-content-component"></friends-sidebar-component>
    `);
  }

  style() {
    return (`
      <style>
      </style>
    `);
  }
}
