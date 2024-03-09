export class _KeyHookHandler {
  #engine;
  #upKeyIsPressed = [false, false];
  #downKeyIsPressed = [false, false];
  #upTouchStart = false;
  #downTouchStart = false;

  constructor(engine) {
    this.#engine = engine;
  }

  startListeningForKeyHooks() {
    this.#engine.component.addComponentEventListener(
        window, 'keydown', (event) => {
          this.#onKeyPress(event);
        }, this,
    );
    this.#engine.component.addComponentEventListener(
        window, 'keyup', (event) => {
          this.#onKeyRelease(event);
        }, this,
    );
    this.#engine.component.addComponentEventListener(
        window, 'blur', () => {
          this.#onFocusLoss();
        }, this,
    );
    const canvas = this.#engine.component.querySelector('canvas');
    this.#engine.component.addComponentEventListener(
        canvas, 'touchstart', (event) => {
          this.touchStart(event);
        }, this,
    );
    this.#engine.component.addComponentEventListener(
        canvas, 'touchend', (event) => {
          this.touchEnd(event);
        }, this,
    );
  }

  touchStart(event) {
    const touch = event.touches[0];
    if (screen.orientation.type.indexOf('landscape') !== -1) {
      if (touch.clientX < window.innerWidth / 2) {
        this.#pressUpKey();
        this.#upTouchStart = true;
      } else {
        this.#pressDownKey();
        this.#downTouchStart = true;
      }
    } else {
      if (touch.clientY < window.innerHeight / 2) {
        this.#pressUpKey();
        this.#upTouchStart = true;
      } else {
        this.#pressDownKey();
        this.#downTouchStart = true;
      }
    }
  }

  touchEnd(event) {
    if (this.#upTouchStart) {
      this.#releaseUpKey();
      this.#upTouchStart = false;
    } else if (this.#downTouchStart) {
      this.#releaseDownKey();
      this.#downTouchStart = false;
    }
  }

  #onKeyPress(event) {
    switch (event.key) {
      case 'w':
      case 'W':
        this.#pressUpKey(0);
        return;
      case 'ArrowUp':
        this.#pressUpKey(1);
        return;
      case 's':
      case 'S':
        this.#pressDownKey(0);
        return;
      case 'ArrowDown':
        this.#pressDownKey(1);
        return;
      default:
        return;
    }
  }

  #pressUpKey(index) {
    if (this.#downKeyIsPressed[index]) {
      this.#stopMoving(index);
    } else {
      this.#moveUp(index);
    }
    this.#upKeyIsPressed[index] = true;
  }

  #pressDownKey(index) {
    if (this.#upKeyIsPressed[index]) {
      this.#stopMoving(index);
    } else {
      this.#moveDown(index);
    }
    this.#downKeyIsPressed[index] = true;
  }

  #onKeyRelease(event) {
    switch (event.key) {
      case 'w':
      case 'W':
        this.#releaseUpKey(0);
        return;
      case 'ArrowUp':
        this.#releaseUpKey(1);
        return;
      case 's':
      case 'S':
        this.#releaseDownKey(0);
        return;
      case 'ArrowDown':
        this.#releaseDownKey(1);
        return;
      default:
        return;
    }
  }

  #releaseUpKey(index) {
    if (this.#downKeyIsPressed[index]) {
      this.#moveDown(index);
    } else {
      this.#stopMoving(index);
    }
    this.#upKeyIsPressed[index] = false;
  }

  #releaseDownKey(index) {
    if (this.#upKeyIsPressed[index]) {
      this.#moveUp(index);
    } else {
      this.#stopMoving(index);
    }
    this.#downKeyIsPressed[index] = false;
  }

  #onFocusLoss() {
    this.#upKeyIsPressed[0] = false;
    this.#upKeyIsPressed[1] = false;
    this.#downKeyIsPressed[0] = false;
    this.#downKeyIsPressed[1] = false;

    this.#stopMoving(0);
    this.#stopMoving(1);
  }

  #stopMoving(index) {
    this.#engine.scene.setPlayerPaddleDirection('none', index);
  }

  #moveUp(index) {
    this.#engine.scene.setPlayerPaddleDirection('up', index);
  }

  #moveDown(index) {
    this.#engine.scene.setPlayerPaddleDirection('down', index);
  }
}
