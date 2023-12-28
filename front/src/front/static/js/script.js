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
    const logPart = document.querySelector('#log-part');
    const logoutPart = document.querySelector('#logout-part')
    const navUsername = document.querySelector('#nav-username');
    const navProfileImg = document.querySelector('#nav-profile-img');
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
    const logPart = document.querySelector('#log-part');
    const logoutPart = document.querySelector('#logout-part')
    logPart.classList.add('d-none');
    logoutPart.classList.remove('d-none');
}

window.addEventListener('popstate', function (event) {
    if (event.state != null) {
        loadComponent(event.state['previousComponent'], 'content', false);
    }
});
