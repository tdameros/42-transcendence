export class _KeyHookHandler {
    constructor(engine) {
        this._engine = engine;

        this._upKeyIsPressed = false;
        this._downKeyIsPressed = false;
        this._serverKnownMovement = "none";
    }

    listenForKeyHooks() {
        window.addEventListener('keydown', async () => {
            await this._onKeyPress(event)
        }, false);
        window.addEventListener('keyup', async () => {
            await this._onKeyRelease(event);
        }, false);
    }

    stopListeningForKeyHooks() {
        window.addEventListener('keydown', async () => {}, false);
        window.addEventListener('keyup', async () => {}, false);
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
        this._upKeyIsPressed = true;
        if (this._downKeyIsPressed) {
            if (this._serverKnownMovement !== "none") {
                await this._engine.emit("player_stopped_moving", "");
                this._serverKnownMovement = "none";
            }
            return;
        }
        if (this._serverKnownMovement === "up")
            return;

        await this._engine.emit("player_moves_up", "");
        this._serverKnownMovement = "up"
    }

    async _pressDownKey() {
        this._downKeyIsPressed = true;
        if (this._upKeyIsPressed) {
            if (this._serverKnownMovement !== "none") {
                await this._engine.emit("player_stopped_moving", "");
                this._serverKnownMovement = "none";
            }
            return;
        }
        if (this._serverKnownMovement === "down")
            return;

        await this._engine.emit("player_moves_down", "");
        this._serverKnownMovement = "down"
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
            await this._engine.emit("player_moves_down", "");
            this._serverKnownMovement = "down";
        } else {
            await this._engine.emit("player_stopped_moving", "");
            this._serverKnownMovement = "none";
        }
        this._upKeyIsPressed = false;
    }

    async _releaseDownKey() {
        if (this._upKeyIsPressed) {
            await this._engine.emit("player_moves_up", "");
            this._serverKnownMovement = "up";
        } else {
            await this._engine.emit("player_stopped_moving", "");
            this._serverKnownMovement = "none";
        }
        this._downKeyIsPressed = false;
    }
}