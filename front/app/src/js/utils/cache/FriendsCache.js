import {Cache} from './Cache.js';

export class FriendsCache {
  static CacheKey = 'friends';
  static event = 'friends-cache-update';

  static set(friendId, value) {
    if (!Cache.get(FriendsCache.CacheKey)) {
      FriendsCache.define();
    }
    Cache.get(FriendsCache.CacheKey).set(friendId, value);
    document.dispatchEvent(new Event(FriendsCache.event));
  }

  static get(friendId) {
    if (Cache.get(FriendsCache.CacheKey)) {
      return Cache.get(FriendsCache.CacheKey).get(friendId);
    } else {
      return null;
    }
  }

  static delete(friendId) {
    if (Cache.get(FriendsCache.CacheKey)) {
      Cache.get(FriendsCache.CacheKey).delete(friendId);
      document.dispatchEvent(new Event(FriendsCache.event));
    }
  }

  static isDefine() {
    return Cache.get(FriendsCache.CacheKey) !== undefined;
  }

  static defineIfNot() {
    if (!FriendsCache.isDefine()) {
      FriendsCache.define();
    }
  }

  static define() {
    Cache.set(FriendsCache.CacheKey, new Map());
  }

  static getFriends() {
    return Cache.get(FriendsCache.CacheKey);
  }
}
