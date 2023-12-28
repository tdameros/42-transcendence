const email = document.querySelector('#email');
email.addEventListener('input', function () {
    if (!isValidEmail(email.value)) {
        email.classList.remove('is-valid')
        email.classList.add('is-invalid');
    } else {
        email.classList.remove('is-invalid')
        email.classList.add('is-valid');
    }
});

function isValidEmail(email) {
    const emailRegex = /^[\w-.]+@([\w-]+\.)+[\w-]{2,4}$/;
    return emailRegex.test(email);
}

const forgotPassword = document.querySelector('#forgot-password');
forgotPassword.addEventListener('click', function () {
    loadComponent('auth/reset-password-email/', 'content');
})

const dontHaveAccount = document.querySelector('#dont-have-account');
dontHaveAccount.addEventListener('click', function () {
    loadComponent('auth/signup/', 'content');
})

const signinBtn = document.querySelector('#signin-btn');
signinBtn.addEventListener('click', function (event) {
    event.preventDefault();
    signin();
})
const signinForm = document.querySelector('#signin-form');
signinForm.addEventListener('submit', function (event) {
    event.preventDefault();
   signin();
})

function signin() {
    logNav();
    homeNav();
}