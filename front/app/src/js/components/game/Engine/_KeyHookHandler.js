export class _KeyHookHandler {
  #engine;
  #upKeyIsPressed = false;
  #downKeyIsPressed = false;
  #serverKnownMovement = 'none';
  #upTouchStart = false;
  #downTouchStart = false;

  constructor(engine) {
    this.#engine = engine;
  }

  startListeningForKeyHooks() {
    this.#engine.component.addComponentEventListener(
        window, 'keydown', async (event) => {
          await this.#onKeyPress(event);
        }, this,
    );
    this.#engine.component.addComponentEventListener(
        window, 'keyup', async (event) => {
          await this.#onKeyRelease(event);
        }, this,
    );
    this.#engine.component.addComponentEventListener(
        window, 'blur', async () => {
          await this.#onFocusLoss();
        }, this,
    );
    const canvas = this.#engine.component.querySelector('canvas');
    this.#engine.component.addComponentEventListener(
        canvas, 'touchstart', async (event) => {
          await this.touchStart(event);
        }, this,
    );
    this.#engine.component.addComponentEventListener(
        canvas, 'touchend', async (event) => {
          await this.touchEnd(event);
        }, this,
    );
  }

  async touchStart(event) {
    const touch = event.touches[0];
    if (screen.orientation.type.indexOf('landscape') !== -1) {
      if (touch.clientX < window.innerWidth / 2) {
        await this.#pressUpKey();
        this.#upTouchStart = true;
      } else {
        await this.#pressDownKey();
        this.#downTouchStart = true;
      }
    } else {
      if (touch.clientY < window.innerHeight / 2) {
        await this.#pressUpKey();
        this.#upTouchStart = true;
      } else {
        await this.#pressDownKey();
        this.#downTouchStart = true;
      }
    }
  }

  async touchEnd(event) {
    if (this.#upTouchStart) {
      await this.#releaseUpKey();
      this.#upTouchStart = false;
    } else if (this.#downTouchStart) {
      await this.#releaseDownKey();
      this.#downTouchStart = false;
    }
  }

  async #onKeyPress(event) {
    switch (event.key) {
      case 'w':
        await this.#pressUpKey();
        return;
      case 's':
        await this.#pressDownKey();
        return;
      default:
        return;
    }
  }

  async #pressUpKey() {
    if (this.#downKeyIsPressed) {
      await this.#stopMoving();
    } else {
      await this.#moveUp();
    }
    this.#upKeyIsPressed = true;
  }

  async #pressDownKey() {
    if (this.#upKeyIsPressed) {
      await this.#stopMoving();
    } else {
      await this.#moveDown();
    }
    this.#downKeyIsPressed = true;
  }

  async #onKeyRelease(event) {
    switch (event.key) {
      case 'w':
        await this.#releaseUpKey();
        return;
      case 's':
        await this.#releaseDownKey();
        return;
      default:
        return;
    }
  }

  async #releaseUpKey() {
    if (this.#downKeyIsPressed) {
      await this.#moveDown();
    } else {
      await this.#stopMoving();
    }
    this.#upKeyIsPressed = false;
  }

  async #releaseDownKey() {
    if (this.#upKeyIsPressed) {
      await this.#moveUp();
    } else {
      await this.#stopMoving();
    }
    this.#downKeyIsPressed = false;
  }

  async #onFocusLoss() {
    this.#upKeyIsPressed = false;
    this.#downKeyIsPressed = false;
    await this.#stopMoving();
  }

  async #stopMoving() {
    if (this.#serverKnownMovement !== 'none') {
      const scene = this.#engine.scene;
      const arg = {
        'client_paddle_position': scene.getCurrentPlayerPaddlePositionY(),
        'direction': 'none',
      };
      this.#serverKnownMovement = 'none';
      this.#engine.scene.setCurrentPlayerPaddleDirection('none');
      await this.#engine.emit('update_paddle', arg);
    }
  }

  async #moveUp() {
    if (this.#serverKnownMovement !== 'up') {
      const scene = this.#engine.scene;
      const arg = {
        'client_paddle_position': scene.getCurrentPlayerPaddlePositionY(),
        'direction': 'up',
      };
      this.#serverKnownMovement = 'up';
      this.#engine.scene.setCurrentPlayerPaddleDirection('up');
      await this.#engine.emit('update_paddle', arg);
    }
  }

  async #moveDown() {
    if (this.#serverKnownMovement !== 'down') {
      const scene = this.#engine.scene;
      const arg = {
        'client_paddle_position': scene.getCurrentPlayerPaddlePositionY(),
        'direction': 'down',
      };
      this.#serverKnownMovement = 'down';
      this.#engine.scene.setCurrentPlayerPaddleDirection('down');
      await this.#engine.emit('update_paddle', arg);
    }
  }
}
