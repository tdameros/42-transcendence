import {Cache} from './Cache.js';

export class UsersCache {
  static CacheKey = 'users';

  static set(userId, value) {
    if (!Cache.get(UsersCache.CacheKey)) {
      UsersCache.define();
    }
    Cache.get(UsersCache.CacheKey).set(userId, value);
  }

  static get(userId) {
    if (Cache.get(UsersCache.CacheKey)) {
      return Cache.get(UsersCache.CacheKey).get(userId);
    } else {
      return null;
    }
  }

  static getUserId(username) {
    if (Cache.get(UsersCache.CacheKey)) {
      for (const [userId, value] of Cache.get(UsersCache.CacheKey)) {
        if (value === username) {
          return userId;
        }
      }
    }
    return null;
  }

  static delete(userId) {
    if (Cache.get(UsersCache.CacheKey)) {
      Cache.get(UsersCache.CacheKey).delete(userId);
    }
  }

  static isDefine() {
    return Cache.get(UsersCache.CacheKey) !== undefined;
  }

  static defineIfNot() {
    if (!UsersCache.isDefine()) {
      UsersCache.define();
    }
  }

  static define() {
    Cache.set(UsersCache.CacheKey, new Map());
  }
}
