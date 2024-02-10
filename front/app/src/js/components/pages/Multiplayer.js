import {Component} from '@components';

export class Multiplayer extends Component {
  constructor() {
    super();
  }
  render() {
    return (`
      <navbar-component nav-active="multiplayer"></navbar-component>
      <h1>Multiplayer</h1>
    `);
  }
  style() {
    return (`
      <style>

      </style>
    `);
  }
}
