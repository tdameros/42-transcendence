import * as THREE from "three";

import {Scene} from "./Scene";
import {io} from "socket.io-client";
import {RectAreaLightUniformsLib} from "three/addons";

export class Engine {
    constructor() {
        this._initSocketIO();
        this._initRenderer();
        this._initCamera();
        this._scene = null;
        window.addEventListener('resize', () => {
            this._onWindowResize();
        }, false);
        this._initKeyHooks();
    }

    _initSocketIO() {
        // TODO remove me
        let randomId = '';
        const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        for (let i = 0; i < 7; i++) {
            randomId += characters.charAt(Math.floor(Math.random() * characters.length));
        }
        // !TODO

        this._socket = io('http://localhost:4242', {
            query: {
                "player_id": randomId, // TODO use client account primary key
            },
        });

        this._socket.on('connect', () => {
            console.log('connection established');
        });

        this._socket.on('disconnect', () => {
            console.log('disconnected from server');
        });

        this._socket.on('debug', (message) => {
            console.log('Server debug message: ', message);
        });

        this._socket.on("scene", async (sceneData) => {
            console.log("scene data received");
            this._scene = new Scene(sceneData);
        });

        this._socket.on("update_player_movement", (data) => {
            this._scene.updatePlayerMovement(data);
        });

        this._socket.connect();
    }

    _initRenderer() {
        this._renderer = new THREE.WebGLRenderer({antialias: true});

        this._renderer.shadowMap.enabled = true;
        this._renderer.shadowMap.type = THREE.PCFSoftShadowMap;

        this._renderer.setPixelRatio(window.devicePixelRatio);
        this._renderer.setSize(window.innerWidth, window.innerHeight);

        document.body.appendChild(this._renderer.domElement);
        RectAreaLightUniformsLib.init();
    }

    _initCamera() {
        this._camera = new THREE.PerspectiveCamera(90,
            window.innerWidth / window.innerHeight,
            0.1,
            1000);
        this._camera.position.set(0, 0, 50);
        this._defaultCameraDirection = new THREE.Vector3(0, 0, -1);
        this._camera.lookAt(this._defaultCameraDirection.x,
            this._defaultCameraDirection.y,
            this._defaultCameraDirection.z);
    }

    _onWindowResize() {
        this._renderer.setSize(window.innerWidth, window.innerHeight);

        this._camera.aspect = window.innerWidth / window.innerHeight;
        this._camera.updateProjectionMatrix();
    }

    _initKeyHooks() {
        window.addEventListener('keydown', async () => {
            await this._onKeyPress(event)
        }, false);
        window.addEventListener('keyup', async () => {
            await this._onKeyRelease(event);
        }, false);
    }

    async _onKeyPress(event) {
        if (event.repeat === true) {
            return;
        }

        switch (event.key) {
            case 'w':
                await this._socket.emit("move_up_pressed", "");
                return;

            case 's':
                await this._socket.emit("move_down_pressed", "");
                return;

            default:
                return;
        }
    }

    async _onKeyRelease(event) {
        switch (event.key) {
            case 'w':
                await this._socket.emit("move_up_released", "");
                return;

            case 's':
                await this._socket.emit("move_down_released", "");
                return;

            default:
                return;
        }
    }

    renderFrame() {
        this._renderer.render(this._scene.getThreeJSScene(), this._camera);
    }

    getScene() {
        return this._scene;
    }
}
