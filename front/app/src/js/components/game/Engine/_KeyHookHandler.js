export class _KeyHookHandler {
  #engine;
  #upKeyIsPressed = false;
  #downKeyIsPressed = false;
  #serverKnownMovement = 'none';

  constructor(engine) {
    this.#engine = engine;
  }

  startListeningForKeyHooks() {
    window.addEventListener('keydown', async () => {
      await this.#onKeyPress(event);
    }, false);
    window.addEventListener('keyup', async () => {
      await this.#onKeyRelease(event);
    }, false);
    window.addEventListener('blur', async () => {
      await this.#onFocusLoss();
    }, false);
  }

  stopListeningForKeyHooks() {
    window.addEventListener('keydown', async () => {}, false);
    window.addEventListener('keyup', async () => {}, false);
    window.addEventListener('blur', async () => {}, false);
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