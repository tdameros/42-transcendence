import {Scene} from '../Scene/Scene';
import {_ThreeJS} from './_ThreeJS';
import {_KeyHookHandler} from './_KeyHookHandler';
import {_RedirectionSocketIO} from './sockets/_RedirectionSocketIO';
import {LoadingScreenScene} from "../Scene/LoadingScreenScene";

export class Engine {
    #threeJS;
    #keyHookHandler;
    #socket;
    #scene

    constructor() {
        this.#threeJS = new _ThreeJS(this);
        this.#keyHookHandler = new _KeyHookHandler(this);
        this.#scene = new LoadingScreenScene();
        this.#socket = null;
    }

    connectToServer() {
        this.#socket = new _RedirectionSocketIO(this);
    }

    renderFrame() {
        this.#threeJS.renderFrame(this.#scene.threeJSScene);
    }

    emit(event, data) {
        if (this.#socket === null) {
            console.log('Error: Socket is null: Failed to send event(', event, '): ', data);
            return;
        }

        this.#socket.emit(event, data);
    }

    get scene() {
        return this.#scene;
    }

    set scene(newScene) {
        this.#scene = newScene;
    }

    setAnimationLoop(loopFunction) {
        this.#threeJS.setAnimationLoop(loopFunction);
    }

    stopAnimationLoop() {
        this.#threeJS.stopAnimationLoop();
    }

    set socket(socket) {
        this.#socket = socket;
    }

    startListeningForKeyHooks() {
        this.#keyHookHandler.startListeningForKeyHooks()
    }

    stopListeningForKeyHooks() {
        this.#keyHookHandler.stopListeningForKeyHooks()
    }
}