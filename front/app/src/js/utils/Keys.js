export class Keys {
  static digitKeyMaxCode = 57;
  static digitKeyMinCode = 48;
  static deleteKeyCode = 8;
  static vKeyCode = 86;

  static isDigitKey(event) {
    const keyCode = Keys.getKeyCode(event);
    return (keyCode >= Keys.digitKeyMinCode && keyCode <= Keys.digitKeyMaxCode);
  }

  static isDeleteKey(event) {
    return (Keys.getKeyCode(event) === Keys.deleteKeyCode);
  }

  static getKeyCode(event) {
    return event.keyCode || event.which;
  }

  static isPasteShortcut(event) {
    const isVPressed = (event.key === 'v' || event.keyCode === Keys.vKeyCode);
    return (isVPressed && Keys.isCtrlPressed(event));
  }

  static isCtrlPressed(event) {
    return (event.ctrlKey || event.metaKey);
  }

  static getDigitValue(event) {
    return Keys.getKeyCode(event) - Keys.digitKeyMinCode;
  }
}
