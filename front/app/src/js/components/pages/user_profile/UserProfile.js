import {Component} from '../../Component.js';

export class UserProfile extends Component {
  constructor() {
    super();
  }

  render() {
    return (`
      <navbar-component></navbar-component>
      <friends-sidebar-component main-component="user-profile-content-component" username="${this.getAttribute('username')}"></friends-sidebar-component>
    `);
  }
}
