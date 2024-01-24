import {Component} from "./Component.js";

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

export default { Home };