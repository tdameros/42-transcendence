import {Component} from '@components';

export class Singleplayer extends Component {
  constructor() {
    super();
  }
  render() {
    return (`
      <navbar-component nav-active="singleplayer"></navbar-component>
      <h1>Singleplayer</h1>
    `);
  }
  style() {
    return (`
      <style>

      </style>
    `);
  }
}
