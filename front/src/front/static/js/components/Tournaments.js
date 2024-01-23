import {Component} from "./Component.js";

export class Tournaments extends Component {
  constructor() {
    super();
  }
  render() {
    return (`
      <navbar-component nav-active="tournaments"></navbar-component>
      <h1>Tournaments</h1>
    `);
  }
  style() {
    return (`
      <style>

      </style>
    `);
  }
}

export default { Tournaments };