let isDarkMode = false;

const HOST = window.location.protocol + '//'
    + window.location.host + '/';

const navbarBrandElement = document.querySelector('.navbar-brand');
navbarBrandElement.addEventListener('click', homeNav);
history.pushState({'previousComponent': '/'}, null, HOST);

const logPart = document.querySelector('#log-part');
const logoutPart = document.querySelector('#logout-part')
const navUsername = document.querySelector('#nav-username');
const navProfileImg = document.querySelector('#nav-profile-img');
const body = document.querySelector('body');
const switchButton = document.querySelector('#switch-btn');

function switchMode() {
    if (!isDarkMode) {
        body.setAttribute('data-bs-theme', 'dark');
        switchButton.classList.remove('btn-outline-dark');
        switchButton.setAttribute('class', 'btn btn-outline-light')
        isDarkMode = true;
    } else {
        body.setAttribute('data-bs-theme', 'light');
        switchButton.classList.remove('btn-outline-light');
        switchButton.setAttribute('class', 'btn btn-outline-dark');
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

function logNav() {
    const username = 'tdameros';
    const profileImg = 'static/img/tdameros.jpg';
    navUsername.textContent = username;
    navProfileImg.src = profileImg;
    logoutPart.classList.add('d-none');
    logPart.classList.remove('d-none');
    const logoutButton = document.querySelector('#logout');
    logoutButton.addEventListener('click', logoutNav);
}

function logoutNav() {
    logPart.classList.add('d-none');
    logoutPart.classList.remove('d-none');
}

window.addEventListener('popstate', function (event) {
    if (event.state != null) {
        loadComponent(event.state['previousComponent'], 'content', false);
    }
});
