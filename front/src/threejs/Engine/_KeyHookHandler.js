export class _KeyHookHandler {
    constructor(engine) {
        this._engine = engine;

        this._upKeyIsPressed = false;
        this._downKeyIsPressed = false;
        this._serverKnownMovement = 'none';
    }

    startListeningForKeyHooks() {
        window.addEventListener('keydown', async () => {
            await this._onKeyPress(event)
        }, false);
        window.addEventListener('keyup', async () => {
            await this._onKeyRelease(event);
        }, false);
        window.addEventListener('blur', async () => {
            await this._onFocusLoss();
        }, false);
    }

    stopListeningForKeyHooks() {
        window.addEventListener('keydown', async () => {}, false);
        window.addEventListener('keyup', async () => {}, false);
        window.addEventListener('blur', async () => {}, false);
    }

    async _onKeyPress(event) {
        switch (event.key) {
            case 'w':
                await this._pressUpKey();
                return;
            case 's':
                await this._pressDownKey();
                return;
            default:
                return;
        }
    }

    async _pressUpKey() {
        if (this._downKeyIsPressed) {
            await this._stopMoving()
        } else {
            await this._moveUp()
        }
        this._upKeyIsPressed = true;
    }

    async _pressDownKey() {
        if (this._upKeyIsPressed) {
            await this._stopMoving()
        } else {
            await this._moveDown()
        }
        this._downKeyIsPressed = true;
    }

    async _onKeyRelease(event) {
        switch (event.key) {
            case 'w':
                await this._releaseUpKey();
                return;
            case 's':
                await this._releaseDownKey();
                return;
            default:
                return;
        }
    }

    async _releaseUpKey() {
        if (this._downKeyIsPressed) {
            await this._moveDown()
        } else {
            await this._stopMoving()
        }
        this._upKeyIsPressed = false;
    }

    async _releaseDownKey() {
        if (this._upKeyIsPressed) {
            await this._moveUp()
        } else {
            await this._stopMoving()
        }
        this._downKeyIsPressed = false;
    }

    async _onFocusLoss() {
        await this._stopMoving()
        this._upKeyIsPressed = false;
        this._downKeyIsPressed = false;
    }

    async _stopMoving() {
        if (this._serverKnownMovement !== 'none') {
            await this._engine.emit('player_stopped_moving',
                                    this._engine.getScene()
                                                .getCurrentPlayerPositionAsArray());
            this._serverKnownMovement = 'none';
            this._engine.getScene().currentPlayerStopsMoving();
        }
    }

    async _moveUp() {
        if (this._serverKnownMovement !== 'up') {
            await this._engine.emit('player_moves_up',
                                    this._engine.getScene()
                                                .getCurrentPlayerPositionAsArray());
            this._serverKnownMovement = 'up'
            this._engine.getScene().currentPlayerMovesUp();
        }
    }

    async _moveDown() {
        if (this._serverKnownMovement !== 'down') {
            await this._engine.emit('player_moves_down',
                                    this._engine.getScene()
                                                .getCurrentPlayerPositionAsArray());
            this._serverKnownMovement = 'down'
            this._engine.getScene().currentPlayerMovesDown();
        }
    }
}