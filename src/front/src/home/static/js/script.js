let isDarkMode = false;

const HOST = window.location.protocol + '//'
    + window.location.host + '/';

function switchMode() {
    if (!isDarkMode) {
        document.querySelector('body').setAttribute('data-bs-theme', 'dark');
        document.querySelector('#switch-btn').classList.remove('btn-outline-dark');
        document.querySelector('#switch-btn').setAttribute('class', 'btn btn-outline-light')
        isDarkMode = true;
    } else {
        document.querySelector('body').setAttribute('data-bs-theme', 'light');
        document.querySelector('#switch-btn').classList.remove('btn-outline-light');
        document.querySelector('#switch-btn').setAttribute('class', 'btn btn-outline-dark');
        isDarkMode = false;
    }
}

async function loadComponent(uri, parentId, setState = true) {
    try {
        if (setState) {
            history.pushState({'previousComponent': uri}, null, HOST);
        }
        const response = await fetch(HOST + uri);
        if (!response.ok) {
            console.error('Request failed');
            return false;
        }
        const html = await response.text();
        const contentDiv = document.querySelector('#' + parentId);
        contentDiv.innerHTML = html;
        evalScript(parentId);
    } catch (error) {
        console.error('Error:', error);
        return false;
    }
    return true;
}

function evalScript(containerId) {
    const scripts = document.querySelectorAll(`#${containerId} > script`);
    for (let i = 0; i < scripts.length; i++) {
        eval(scripts[i].innerText);
    }
}

function homeNav(event) {
    const contentDiv = document.querySelector('#content');
    contentDiv.innerHTML = '';
    return false;
}

document.addEventListener('DOMContentLoaded', function () {
    const navbarBrandElement = document.querySelector('.navbar-brand');
    navbarBrandElement.addEventListener('click', homeNav);
    history.pushState({'previousComponent': '/'}, null, HOST);
});

function logNav() {
    const loginPart = document.querySelector('#login-part');
    loginPart.innerHTML = `
        <a class="mx-2">
            <i class="fas fa-bell text-dark-emphasis"></i>
        </a>
        <div class="dropdown mx-2">
        <span class="dropdown-toggle" id="dropdownMenuLink"
              data-bs-toggle="dropdown" aria-expanded="false">
              <img src="static/img/tdameros.jpg" alt="Photo de profil"
                   class="rounded-circle"
                   style="width: 40px; height: 40px;">
                <span class="">@tdameros</span>
        </span>
            <ul class="dropdown-menu dropdown-menu-end"
                aria-labelledby="dropdownMenuLink">
                <li><a class="dropdown-item">Profil</a></li>
                <li><a class="dropdown-item">Settings</a></li>
                <li><a id="logout" class="dropdown-item text-danger">Sign out</a>
                </li>
            </ul>
        </div>
    `
    document.querySelector('#logout').addEventListener('click', function () {
        delogNav();
    })
}

function delogNav() {
    const loginPart = document.querySelector('#login-part');
    loginPart.innerHTML = `
        <button class="btn btn-outline-success" onclick="loadComponent('auth/signup/', 'content')">SignUp</button>
        <button type="button" class="btn btn-primary ms-2" onclick="loadComponent('auth/signin/', 'content')">SignIn</button>
    `
}

window.addEventListener('popstate', function (event) {
    if (event.state != null) {
        loadComponent(event.state['previousComponent'], 'content', false);
    }
});
