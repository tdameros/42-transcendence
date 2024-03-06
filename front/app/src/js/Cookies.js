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
    const expireDate = new Date();
    expireDate.setFullYear(expireDate.getFullYear() + 1);
    document.cookie = `${name}=${value};path=/;expires=${expireDate.toUTCString()};${Cookies.#securePart}`;
  }

  static remove(name) {
    const options = `path=/;${Cookies.#expireDate};${Cookies.#securePart}`;
    document.cookie = `${name}=;${options}`;
  }

  static removeAll() {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim().split('=')[0];
      Cookies.remove(cookie);
    }
  }
}
