import * as THREE from "three";
import {FirstPersonControls} from 'three/addons/controls/FirstPersonControls.js';

export class Engine {
    constructor() {
        this._initRenderer();
        this._initCamera();
        window.addEventListener('resize',
                                () => {this._onWindowResize();},
                                false);

        this._controls = new FirstPersonControls(this._camera,
            this._renderer.domElement);
        this._controls.lookSpeed = 0.8;
        this._controls.movementSpeed = 10;
        // this._pressedKeys = [];
        // window.addEventListener('keydown', () => {
        //     this._onKeyDown(event)
        // }, false);
        // window.addEventListener('keyup', () => {
        //     this._onKeyUp(event);
        // }, false);
    }

    _initRenderer() {
        this._renderer = new THREE.WebGLRenderer({antialias: true});

        this._renderer.shadowMap.enabled = true;
        this._renderer.shadowMap.type = THREE.PCFSoftShadowMap;

        this._renderer.setPixelRatio(window.devicePixelRatio);
        this._renderer.setSize(window.innerWidth, window.innerHeight);

        document.body.appendChild(this._renderer.domElement);
    }

    _initCamera() {
        this._camera = new THREE.PerspectiveCamera(90,
            window.innerWidth / window.innerHeight,
            0.1,
            1000);
        this._camera.position.set(0, 0, 20);
        this._defaultCameraDirection = new THREE.Vector3(0, 0, -1);
        this._camera.lookAt(this._defaultCameraDirection.x,
                            this._defaultCameraDirection.y,
                            this._defaultCameraDirection.z);
    }

    _onWindowResize() {
        this._renderer.setSize(window.innerWidth, window.innerHeight);

        this._camera.aspect = window.innerWidth / window.innerHeight;
        this._camera.updateProjectionMatrix();

        this._controls.handleResize();
    }

    // _onKeyDown(event) {
    //     if (this._pressedKeys.includes(event.key.toLowerCase())) return;
    //
    //     this._pressedKeys.push(event.key.toLowerCase());
    // }
    //
    // _onKeyUp(event) {
    //     let keyToRemove = event.key.toLowerCase();
    //     let i = 0;
    //     while (i < this._pressedKeys.length) {
    //         if (this._pressedKeys[i] === keyToRemove) {
    //             this._pressedKeys.splice(i, 1);
    //             continue;
    //         }
    //         ++i;
    //     }
    // }
    //
    // handlePressedKeys() {
    //     for (let i = 0; i < this._pressedKeys.length; ++i) {
    //         switch (this._pressedKeys[i]) {
    //             case 'w':
    //                 this._camera.position.add(this._getCameraDirection());
    //                 break;
    //             case 's':
    //                 this._camera.position.sub(this._getCameraDirection());
    //                 break;
    //             case 'a':
    //                 let left = this._getCameraDirection();
    //                 left.applyAxisAngle(new THREE.Vector3(0, 1, 0), Math.PI / 2);
    //                 this._camera.position.add(left);
    //                 break;
    //             case 'd':
    //                 let right = this._getCameraDirection();
    //                 right.applyAxisAngle(new THREE.Vector3(0, -1, 0), Math.PI / 2);
    //                 this._camera.position.add(right);
    //                 break;
    //             case ' ':
    //                 let up = this._getCameraDirection();
    //                 up.applyAxisAngle(new THREE.Vector3(1, 0, 0), Math.PI / 2);
    //                 this._camera.position.add(up);
    //                 break;
    //             case 'shift':
    //                 let down = this._getCameraDirection();
    //                 down.applyAxisAngle(new THREE.Vector3(-1, 0, 0), Math.PI / 2);
    //                 this._camera.position.add(down);
    //                 break;
    //             case 'arrowup':
    //                 this._camera.rotation.x += 0.1;
    //                 break;
    //             case 'arrowdown':
    //                 this._camera.rotation.x -= 0.1;
    //                 break;
    //             case 'arrowleft':
    //                 this._camera.rotation.y += 0.1;
    //                 break;
    //             case 'arrowright':
    //                 this._camera.rotation.y -= 0.1;
    //                 break;
    //             default:
    //                 break;
    //         }
    //     }
    // }
    //
    // _getCameraDirection() {
    //     let vector = this._defaultCameraDirection.clone();
    //
    //     vector.applyQuaternion(this._camera.quaternion);
    //
    //     vector.normalize();
    //     return vector;
    // }
}
