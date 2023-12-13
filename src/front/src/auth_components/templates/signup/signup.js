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
        missingRequirements.push("Password must be at least 8 characters long.");
    }
    if (password.length > 20) {
        missingRequirements.push("Password must contain a maximum of 20 characters.");
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


const username = document.querySelector("#username");
username.addEventListener('input', function () {
    if (username.value.length === 0) {
        username.classList.remove("is-valid")
        username.classList.add("is-invalid");
    } else {
        username.classList.remove("is-invalid")
        username.classList.add("is-valid");
    }
});

const email = document.querySelector("#email");
email.addEventListener('input', function () {
    if (!isValidEmail(email.value)) {
        email.classList.remove("is-valid")
        email.classList.add("is-invalid");
    } else {
        email.classList.remove("is-invalid")
        email.classList.add("is-valid");
    }
});

const password = document.querySelector("#password");
const confirm_password = document.querySelector("#confirm_password");
password.addEventListener('input', function () {
    validy = isValidPassword(password.value);
    console.log(validy.join(', '));
    if (validy.length !== 0) {
        password.classList.remove("is-valid")
        password.classList.add("is-invalid");
        const feedback = document.querySelector("#password-feedback");
        feedback.innerHTML = '';
        let htmlMessage = document.createElement('p');
        htmlMessage.textContent = validy[0];
        feedback.appendChild(htmlMessage);
    } else {
        password.classList.remove("is-invalid")
        password.classList.add("is-valid");
    }
});

confirm_password.addEventListener('input', function () {
    if (confirm_password.value !== password.value) {
        confirm_password.classList.remove("is-valid")
        confirm_password.classList.add("is-invalid");
    } else {
        confirm_password.classList.remove("is-invalid")
        confirm_password.classList.add("is-valid");
    }
});

const confirm_password_eye_icon = document.querySelector('#confirm-password-eye');
confirm_password_eye_icon_status = false;

confirm_password_eye_icon.addEventListener('click', function () {
    if (!confirm_password_eye_icon_status) {
        confirm_password_eye_icon.children[0].classList.remove('fa-eye');
        confirm_password_eye_icon.children[0].classList.add('fa-eye-slash');
        confirm_password.type = 'text';
        confirm_password_eye_icon_status = true;
    }
    else {
        confirm_password_eye_icon.children[0].classList.remove('fa-eye-slash');
        confirm_password_eye_icon.children[0].classList.add('fa-eye');
        confirm_password.type = 'password';
        confirm_password_eye_icon_status = false;
    }
})

const password_eye_icon = document.querySelector('#password-eye');
password_eye_icon_status = false;

password_eye_icon.addEventListener('click', function () {
    if (!password_eye_icon_status) {
        password_eye_icon.children[0].classList.remove('fa-eye');
        password_eye_icon.children[0].classList.add('fa-eye-slash');
        password.type = 'text';
        password_eye_icon_status = true;
    }
    else {
        password_eye_icon.children[0].classList.remove('fa-eye-slash');
        password_eye_icon.children[0].classList.add('fa-eye');
        password.type = 'password';
        password_eye_icon_status = false;
    }
})
