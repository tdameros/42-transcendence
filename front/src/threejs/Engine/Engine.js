import {Scene} from '../Scene';
import {_ThreeJS} from './_ThreeJS';
import {_KeyHookHandler} from './_KeyHookHandler';
import {_RedirectionSocketIO} from './sockets/_RedirectionSocketIO';

export class Engine {
    constructor() {
        this._threeJS = new _ThreeJS(this);
        this._keyHookHandler = new _KeyHookHandler(this);
        this._createDefaultScene();
        this._socket = null;
    }

    _createDefaultScene() {
        const boards = [];
        const balls = [
            {
                'position': {x: 0., y: 0., z: 0.5},
                'move_direction': {x: 1., y: 0., z: 0.}
            }
        ];
        const players = [];

        this._scene = new Scene(boards, balls, players);
    }

    connectToServer() {
        this._socket = new _RedirectionSocketIO(this);
    }

    renderFrame() {
        this._threeJS.renderFrame(this._scene.getThreeJSScene());
    }

    emit(event, data) {
        if (this._socket === null) {
            console.log('Error: Socket is null: Failed to send event(', event, '): ', data);
            return;
        }

        this._socket.emit(event, data);
    }

    getScene() {
        return this._scene;
    }

    setScene(newScene) {
        this._scene = newScene;
    }

    setAnimationLoop(loopFunction) {
        this._threeJS.setAnimationLoop(loopFunction);
    }

    stopAnimationLoop() {
        this._threeJS.stopAnimationLoop();
    }

    setSocket(socket) {
        this._socket = socket;
    }

    startListeningForKeyHooks() {
        this._keyHookHandler.startListeningForKeyHooks()
    }

    stopListeningForKeyHooks() {
        this._keyHookHandler.stopListeningForKeyHooks()
    }
}