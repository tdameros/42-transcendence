const username = document.querySelector('#username');
username.addEventListener('input', function () {
    if (username.value.length === 0) {
        username.classList.remove('is-valid')
        username.classList.add('is-invalid');
    } else {
        username.classList.remove('is-invalid')
        username.classList.add('is-valid');
    }
});

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

const password = document.querySelector('#password');
const confirmPassword = document.querySelector('#confirm-password');
password.addEventListener('input', function () {
    const validity = isValidPassword(password.value);
    if (validity.length !== 0) {
        password.classList.remove('is-valid')
        password.classList.add('is-invalid');
        const feedback = document.querySelector('#password-feedback');
        feedback.innerHTML = '';
        let htmlMessage = document.createElement('p');
        htmlMessage.textContent = validity[0];
        feedback.appendChild(htmlMessage);
    } else {
        password.classList.remove('is-invalid')
        password.classList.add('is-valid');
    }
});

confirmPassword.addEventListener('input', function () {
    if (confirmPassword.value !== password.value) {
        confirmPassword.classList.remove('is-valid')
        confirmPassword.classList.add('is-invalid');
    } else {
        confirmPassword.classList.remove('is-invalid')
        confirmPassword.classList.add('is-valid');
    }
});

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function isValidPassword(password) {
    const uppercaseRegex = /[A-Z]/;
    const numberRegex = /[0-9]/;
    const specialCharacterRegex = /[!@#$%^&*()_+]/;

    const missingRequirements = [];
    if (password.length < 8) {
        missingRequirements.push('Password must be at least 8 characters long.');
    }
    if (password.length > 20) {
        missingRequirements.push('Password must contain a maximum of 20 characters.');
    }
    if (!uppercaseRegex.test(password)) {
        missingRequirements.push('Password must contain at least one uppercase letter.');
    }
    if (!numberRegex.test(password)) {
        missingRequirements.push('Password must contain at least one number.');
    }
    if (!specialCharacterRegex.test(password)) {
        missingRequirements.push('Password must contain at least one special character.');
    }
    return missingRequirements;
}

const passwordEyeIcon = document.querySelector('#password-eye');
let passwordEyeIconStatus = false;

passwordEyeIcon.addEventListener('click', function () {
    if (!passwordEyeIconStatus) {
        passwordEyeIcon.children[0].classList.remove('fa-eye');
        passwordEyeIcon.children[0].classList.add('fa-eye-slash');
        password.type = 'text';
        passwordEyeIconStatus = true;
    }
    else {
        passwordEyeIcon.children[0].classList.remove('fa-eye-slash');
        passwordEyeIcon.children[0].classList.add('fa-eye');
        password.type = 'password';
        passwordEyeIconStatus = false;
    }
})

const confirmPasswordEyeIcon = document.querySelector('#confirm-password-eye');
let confirmPasswordEyeIconStatus = false;

confirmPasswordEyeIcon.addEventListener('click', function () {
    if (!confirmPasswordEyeIconStatus) {
        confirmPasswordEyeIcon.children[0].classList.remove('fa-eye');
        confirmPasswordEyeIcon.children[0].classList.add('fa-eye-slash');
        confirmPassword.type = 'text';
        confirmPasswordEyeIconStatus = true;
    }
    else {
        confirmPasswordEyeIcon.children[0].classList.remove('fa-eye-slash');
        confirmPasswordEyeIcon.children[0].classList.add('fa-eye');
        confirmPassword.type = 'password';
        confirmPasswordEyeIconStatus = false;
    }
})

const haveAccount = document.querySelector('#have-account');

haveAccount.addEventListener('click', function () {
    loadComponent('auth/signin/', 'content');
})

