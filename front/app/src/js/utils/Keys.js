export class Keys {
  static deleteKeyCode = 8;
  static vKeyCode = 86;

  static isDigitKey(event) {
    return (/^\d$/.test(Keys.getKeyValue(event)));
  }

  static isDeleteKey(event) {
    return (Keys.getKeyCode(event) === Keys.deleteKeyCode);
  }

  static getKeyCode(event) {
    return event.keyCode || event.which;
  }

  static getKeyValue(event) {
    return event.data || event.key;
  }

  static isPasteShortcut(event) {
    const isVPressed = (Keys.getKeyValue(event) === 'v' ||
      event.keyCode === Keys.vKeyCode);
    return (isVPressed && Keys.isCtrlPressed(event));
  }

  static isCtrlPressed(event) {
    return (event.ctrlKey || event.metaKey);
  }

  static getDigitValue(event) {
    return parseInt(Keys.getKeyValue(event));
  }
}
