
isDarkMode = false;

function switchMode() {
    if (!isDarkMode) {
        document.querySelector("body").setAttribute("data-bs-theme", "dark");
        document.querySelector("#switch-btn").classList.remove("btn-outline-dark");
        document.querySelector("#switch-btn").setAttribute("class", "btn btn-outline-light")
        isDarkMode = true;
    }
    else {
        document.querySelector("body").setAttribute("data-bs-theme", "light");
        document.querySelector("#switch-btn").classList.remove("btn-outline-light");
        document.querySelector("#switch-btn").setAttribute("class", "btn btn-outline-dark")
        isDarkMode = false;
    }
}