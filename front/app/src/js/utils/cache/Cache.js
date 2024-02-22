
export class Cache {
  static cache = {};

  static set(key, value) {
    this.cache[key] = value;
  }

  static get(key) {
    return this.cache[key];
  }
}
