export class InputValidator {

  static usernameMaxLength = 20;
  static usernameMinLength = 2;
  static passwordMaxLength = 20;
  static passwordMinLength = 8;
  static emailMaxLength = 60;
  static emailLocalMinLength = 5;

  constructor() {

  }

  static isAlphaNumeric(string) {
    const alphaNumericRegex = /^[a-zA-Z0-9_]+$/;
    return alphaNumericRegex.test(string);
  }

  static #createValidityObject(missingRequirements) {
    if (missingRequirements.length !== 0)
      return {validity: false, missingRequirements};
    return {validity: true, missingRequirements};
  }

  static isValidEmail(email) {
    const emailRegex = /^[\w-.]+@([\w-]+\.)+[\w-]{2,4}$/;
    const missingRequirements = [];
    if (email.length > InputValidator.emailMaxLength) {
      missingRequirements.push(`Email must contain a maximum of ${InputValidator.emailMaxLength} characters.`);
    }
    if (!emailRegex.test(email)) {
      missingRequirements.push('Invalid email format.');
    }
    const emailLocal = email.split('@')[0];
    if (emailLocal.length < InputValidator.emailLocalMinLength) {
      missingRequirements.push(`Email local part must contain at least ${InputValidator.emailLocalMinLength} characters.`);
    }
    return InputValidator.#createValidityObject(missingRequirements);
  }

  static isValidUsername(username) {
    const missingRequirements = [];
    if (username.length < InputValidator.usernameMinLength) {
      missingRequirements.push(`Username must be at least ${InputValidator.usernameMinLength} characters long.`);
    }
    if (username.length > InputValidator.usernameMaxLength) {
          missingRequirements.push(`Username must contain a maximum of ${InputValidator.usernameMaxLength} characters.`);
    }
    if (!InputValidator.isAlphaNumeric(username)) {
      missingRequirements.push('Username must contain only alphanumeric characters.');
    }
    return InputValidator.#createValidityObject(missingRequirements);
  }

  static isValidSecurePassword(password) {
    const uppercaseRegex = /[A-Z]/;
    const numberRegex = /[0-9]/;
    const specialCharacterRegex = /[!@#$%^&*()_+]/;
    const missingRequirements = [];

    if (password.length < InputValidator.passwordMinLength) {
      missingRequirements.push(`Password must be at least ${InputValidator.passwordMinLength} characters long.`);
    }
    if (password.length > InputValidator.passwordMaxLength) {
      missingRequirements.push(`Password must contain a maximum of ${InputValidator.passwordMaxLength} characters.`);
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
    return InputValidator.#createValidityObject(missingRequirements);
  }

}

export default {InputValidator};