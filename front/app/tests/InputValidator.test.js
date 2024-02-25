import {InputValidator} from '../src/js/utils/InputValidator.js';

describe('InputValidator', () => {
  describe('isValidEmail', () => {
    it('valid email', () => {
      const validEmail = 'tests@example.com';
      const result = InputValidator.isValidEmail(validEmail);
      expect(result.validity).toBe(true);
      expect(result.missingRequirements).toHaveLength(0);
    });

    it('email exceeding max length', () => {
      const longEmail = 'a'.repeat(InputValidator.emailMaxLength + 1) +
          '@example.com';
      const result = InputValidator.isValidEmail(longEmail);
      expect(result.validity).toBe(false);
      expect(result.missingRequirements).toContain(
          InputValidator.MessageEmailMaxLength,
      );
    });

    it('invalid email format', () => {
      const invalidEmail = 'invalidemail@.com';
      const result = InputValidator.isValidEmail(invalidEmail);
      expect(result.validity).toBe(false);
      expect(result.missingRequirements).toContain(
          InputValidator.MessageEmailInvalidFormat,
      );
    });

    it('email with an empty local part', () => {
      const shortLocalPart = '@ex.com';
      const result = InputValidator.isValidEmail(shortLocalPart);
      expect(result.validity).toBe(false);
      expect(result.missingRequirements).toContain(
          InputValidator.MessageEmailLocalMinLength,
      );
    });
  });

  describe('isValidUsername', () => {
    it('valid username', () => {
      const validUsername = 'validUsername123';
      const result = InputValidator.isValidUsername(validUsername);
      expect(result.validity).toBe(true);
      expect(result.missingRequirements).toHaveLength(0);
    });

    it('username below min length', () => {
      const shortUsername = 'a';
      const result = InputValidator.isValidUsername(shortUsername);
      expect(result.validity).toBe(false);
      expect(result.missingRequirements).toContain(
          InputValidator.MessageUsernameMinLength,
      );
    });

    it('username above max length', () => {
      const longUsername = 'a'.repeat(InputValidator.usernameMaxLength + 1);
      const result = InputValidator.isValidUsername(longUsername);
      expect(result.validity).toBe(false);
      expect(result.missingRequirements).toContain(
          InputValidator.MessageUsernameMaxLength,
      );
    });

    it('username with non-alphanumeric characters', () => {
      const invalidUsername = 'invalid@username';
      const result = InputValidator.isValidUsername(invalidUsername);
      expect(result.validity).toBe(false);
      expect(result.missingRequirements).toContain(
          InputValidator.MessageUsernameAlnum,
      );
    });
  });

  describe('isValidSecurePassword', () => {
    it('valid secure password', () => {
      const validPassword = 'ValidPassword123!';
      const result = InputValidator.isValidSecurePassword(validPassword);
      expect(result.validity).toBe(true);
      expect(result.missingRequirements).toHaveLength(0);
    });

    it('password below min length', () => {
      const shortPassword = 'WPwd1!';
      const result = InputValidator.isValidSecurePassword(shortPassword);
      expect(result.validity).toBe(false);
      expect(result.missingRequirements).toContain(
          InputValidator.MessagePasswordMinLength,
      );
    });

    it('password above max length', () => {
      const longPassword = 'StrongPwd'.repeat(5) + '123!';
      const result = InputValidator.isValidSecurePassword(longPassword);
      expect(result.validity).toBe(false);
      expect(result.missingRequirements).toContain(
          InputValidator.MessagePasswordMaxLength,
      );
    });

    it('password without uppercase letter', () => {
      const passwordWithoutUppercase = 'weakpassword1!';
      const result = InputValidator.isValidSecurePassword(
          passwordWithoutUppercase,
      );
      expect(result.validity).toBe(false);
      expect(result.missingRequirements).toContain(
          InputValidator.MessagePasswordUpperCase,
      );
    });

    it('password without a number', () => {
      const passwordWithoutNumber = 'WeakPassword!';
      const result = InputValidator.isValidSecurePassword(
          passwordWithoutNumber,
      );
      expect(result.validity).toBe(false);
      expect(result.missingRequirements).toContain(
          InputValidator.MessagePasswordNumber,
      );
    });

    it('password without a lowercase letter', () => {
      const passwordWithoutLowercase = 'WEAKPASSWORD1!';
      const result = InputValidator.isValidSecurePassword(
          passwordWithoutLowercase,
      );
      expect(result.validity).toBe(false);
      expect(result.missingRequirements).toContain(
          InputValidator.MessagePasswordLowerCase,
      );
    });

    it('password without a special character', () => {
      const passwordWithoutSpecialChar = 'StrongPassword123';
      const result = InputValidator.isValidSecurePassword(
          passwordWithoutSpecialChar,
      );
      expect(result.validity).toBe(false);
      expect(result.missingRequirements).toContain(
          InputValidator.MessagePasswordSpecialChar,
      );
    });
  });
});
