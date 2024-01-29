export class InputValidator {
  static usernameMaxLength = 20;
  static usernameMinLength = 2;
  static passwordMaxLength = 20;
  static passwordMinLength = 8;
  static emailMaxLength = 60;
  static emailLocalMinLength = 5;

  static MessageEmailMaxLength =
    `Email must contain a maximum of ${
      InputValidator.emailMaxLength
    } characters.`;
  static MessageEmailInvalidFormat = 'Invalid email format.';
  static MessageEmailLocalMinLength =
    `Email local part must contain at least ${
      InputValidator.emailLocalMinLength
    } characters.`;
  static MessageUsernameMinLength =
    `Username must be at least ${
      InputValidator.usernameMinLength
    } characters long.`;
  static MessageUsernameMaxLength =
    `Username must contain a maximum of ${
      InputValidator.usernameMaxLength
    } characters.`;
  static MessageUsernameAlnum =
    `Username must contain only alphanumeric characters.`;
  static MessagePasswordMinLength =
    `Password must be at least ${
      InputValidator.passwordMinLength
    } characters long.`;
  static MessagePasswordMaxLength =
    `Password must contain a maximum of ${
      InputValidator.passwordMaxLength
    } characters.`;
  static MessagePasswordUpperCase =
    `Password must contain at least one uppercase letter.`;
  static MessagePasswordNumber =
    `Password must contain at least one number.`;
  static MessagePasswordSpecialChar =
    `Password must contain at least one special character.`;

  constructor() {
  }

  static isAlphaNumeric(string) {
    const alphaNumericRegex = /^[a-zA-Z0-9_]+$/;
    return alphaNumericRegex.test(string);
  }

  static isValidEmail(email) {
    const emailRegex = /^[\w-.]+@([\w-]+\.)+[\w-]{2,4}$/;
    const missingRequirements = [];
    if (email.length > InputValidator.emailMaxLength) {
      missingRequirements.push(InputValidator.MessageEmailMaxLength);
    }
    if (!emailRegex.test(email)) {
      missingRequirements.push(InputValidator.MessageEmailInvalidFormat);
    }
    const emailLocal = email.split('@')[0];
    if (emailLocal.length < InputValidator.emailLocalMinLength) {
      missingRequirements.push(InputValidator.MessageEmailLocalMinLength);
    }
    return InputValidator.#createValidityObject(missingRequirements);
  }

  static isValidUsername(username) {
    const missingRequirements = [];
    if (username.length < InputValidator.usernameMinLength) {
      missingRequirements.push(InputValidator.MessageUsernameMinLength);
    }
    if (username.length > InputValidator.usernameMaxLength) {
      missingRequirements.push(InputValidator.MessageUsernameMaxLength);
    }
    if (!InputValidator.isAlphaNumeric(username)) {
      missingRequirements.push(InputValidator.MessageUsernameAlnum);
    }
    return InputValidator.#createValidityObject(missingRequirements);
  }

  static isValidSecurePassword(password) {
    const uppercaseRegex = /[A-Z]/;
    const numberRegex = /[0-9]/;
    const specialCharacterRegex = /[!@#$%^&*()_+]/;
    const missingRequirements = [];

    if (password.length < InputValidator.passwordMinLength) {
      missingRequirements.push(InputValidator.MessagePasswordMinLength);
    }
    if (password.length > InputValidator.passwordMaxLength) {
      missingRequirements.push(InputValidator.MessagePasswordMaxLength);
    }
    if (!uppercaseRegex.test(password)) {
      missingRequirements.push(InputValidator.MessagePasswordUpperCase);
    }
    if (!numberRegex.test(password)) {
      missingRequirements.push(InputValidator.MessagePasswordNumber);
    }
    if (!specialCharacterRegex.test(password)) {
      missingRequirements.push(InputValidator.MessagePasswordSpecialChar);
    }
    return InputValidator.#createValidityObject(missingRequirements);
  }

  static #createValidityObject(missingRequirements) {
    if (missingRequirements.length !== 0) {
      return {validity: false, missingRequirements};
    }
    return {validity: true, missingRequirements};
  }
}

export default {InputValidator};