import {Component} from '@components';
import {Cookies} from '@js/Cookies.js';

export class FriendsSidebar extends Component {
  constructor() {
    super();
  }
  render() {
    const mainComponent = this.getAttribute('main-component');
    const navbarHeight = document.querySelector('navbar-component').height;
    const sidebarPosition = Cookies.get('sidebar-position');
    const sidebarPositionClass = sidebarPosition === 'visible' ? '' : 'active';
    return (`
      <div id="wrapper">
          <div id="main-content" class="${sidebarPositionClass}">
            <${mainComponent} ${this.getHeritedAttributes()}></${mainComponent}>
          </div>
          <nav id="sidebar-content" class="${sidebarPositionClass}" style="margin-top: ${navbarHeight}px">
              <div class="m-2 ms-0">
                  <friends-component></friends-component>
              </div>
          </nav>
      </div>
    `);
  }
  style() {
    return (`
      <style>
.wrapper {
    display: flex;
    width: 100%;
}

#sidebar-content {
    width: 250px;
    position: fixed;
    top: 0;
    left: calc(100% - 250px);
    height: 100vh;
    z-index: 999;
    transition: all 0.3s;
    background-color: var(--bs-secondary-bg);
}

#sidebar-content.active {
    margin-left: +250px;
}

a[data-toggle="collapse"] {
    position: relative;
}

@media (max-width: 768px) {
    #sidebar-content {
        width: 100vw;
        position: fixed;
        top: 0;
        padding-left: 0.5rem;
        left: calc(0px);
        height: 100vh;
        z-index: 999;
        transition: all 0.3s;
    }
    #sidebar-content.active {
        margin-left: +2500px;
    }
    #main-content {
        width: 100%;
    }
    #main-content.active {
        width: calc(-100%);
    }
}


#main-content {
    width: calc(100% - 250px);
    position: absolute;
    transition: all 0.3s;
}

#main-content.active {
    width: 100%;
}
      </style>
    `);
  }

  postRender() {
  }

  toggleVisibility() {
    const sidebarMainContent = this.querySelector('#main-content');
    const sidebarContent = this.querySelector('#sidebar-content');
    if (sidebarMainContent) {
      sidebarMainContent.classList.toggle('active');
    }
    if (sidebarContent) {
      sidebarContent.classList.toggle('active');
    }
    if (Cookies.get('sidebar-position') === 'visible') {
      Cookies.add('sidebar-position', 'hidden');
    } else {
      Cookies.add('sidebar-position', 'visible');
    }
    window.dispatchEvent(new Event('resize'));
  }

  getHeritedAttributes() {
    const attributeNames = this.getAttributeNames();
    let attributesString = '';
    attributeNames.forEach(function(name, index) {
      if (name !== 'main-component' && name !== 'sidebar-component') {
        attributesString += `${name}="${this.getAttribute(name)}"`;
      }
      if (index < attributeNames.length - 1) {
        attributesString += ' ';
      }
    }, this);
    return attributesString;
  }
}
