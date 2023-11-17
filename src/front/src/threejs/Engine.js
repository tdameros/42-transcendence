import * as THREE from "three";

export class Engine {
    constructor() {
        this._initRenderer();
        this._initCamera();
        this._pressedKeys = [];
        this._initEventsHandlers();
    }

    _initRenderer() {
        this._renderer = new THREE.WebGLRenderer();
        this._renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(this._renderer.domElement);
    }

    _initCamera() {
        this._camera = new THREE.PerspectiveCamera(90,
            window.innerWidth / window.innerHeight,
            0.1,
            1000);
        this._camera.position.set(0, 0, 20);
        this._camera.lookAt(0, 0, -1);
    }

    _initEventsHandlers() {
        window.addEventListener('resize', () => {
            this._onWindowResize();
        }, false);
        window.addEventListener('keydown', () => {
            this._onKeyDown(event)
        }, false);
        window.addEventListener('keyup', () => {
            this._onKeyUp(event);
        }, false);
    }

    _onWindowResize() {
        this._renderer.setSize(window.innerWidth, window.innerHeight);

        this._camera.aspect = window.innerWidth / window.innerHeight;
        this._camera.updateProjectionMatrix();
    }

    _onKeyDown(event) {
        if (this._pressedKeys.includes(event.key.toLowerCase())) return;

        this._pressedKeys.push(event.key.toLowerCase());
    }

    _onKeyUp(event) {
        let keyToRemove = event.key.toLowerCase();
        let i = 0;
        while (i < this._pressedKeys.length) {
            if (this._pressedKeys[i] === keyToRemove) {
                this._pressedKeys.splice(i, 1);
                continue;
            }
            ++i;
        }
    }
}
