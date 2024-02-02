export class Cookies {
  static #securePart = 'SameSite=Strict;Secure';
  static #expireDate = 'expires=Thu, 01 Jan 1970 00:00:01 GMT';

  static get(name) {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith(name)) {
        return cookie.substring(name.length + 1, cookie.length);
      }
    }
    return null;
  }

  static add(name, value) {
    document.cookie = `${name}=${value};path=/;${Cookies.#securePart}`;
  }

  static remove(name) {
    const options = `path=/;${Cookies.#expireDate};${Cookies.#securePart}`;
    document.cookie = `${name}=;${options}`;
  }
}
