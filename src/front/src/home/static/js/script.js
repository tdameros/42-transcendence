isDarkMode = false;

function switchMode() {
    if (!isDarkMode) {
        document.querySelector("body").setAttribute("data-bs-theme", "dark");
        document.querySelector("#switch-btn").classList.remove("btn-outline-dark");
        document.querySelector("#switch-btn").setAttribute("class", "btn btn-outline-light")
        isDarkMode = true;
    } else {
        document.querySelector("body").setAttribute("data-bs-theme", "light");
        document.querySelector("#switch-btn").classList.remove("btn-outline-light");
        document.querySelector("#switch-btn").setAttribute("class", "btn btn-outline-dark")
        isDarkMode = false;
    }
}

async function loadComponent(uri, parentId) {
    try {
        const host = window.location.href;
        const response = await fetch(host + uri);
        if (!response.ok) {
            throw new Error('Request failed');
            return false;
        }
        const html = await response.text();
        const contentDiv = document.querySelector("#" + parentId);
        contentDiv.innerHTML = html;
        // Exécuter le script à l'aide de eval()
        const scripts = document.getElementById(parentId).getElementsByTagName('script');
        for (let i = 0; i < scripts.length; i++) {
            eval(scripts[i].innerText);
        }
    } catch (error) {
        console.error('Error:', error);
        return false;
    }
    return false;
}

function homeNav(event) {
    const contentDiv = document.querySelector("#content");
    contentDiv.innerHTML = "";
    return false;
}

document.addEventListener('DOMContentLoaded', function () {
    const navbarBrandElement = document.querySelector('.navbar-brand');
    navbarBrandElement.addEventListener('click', homeNav);
});
