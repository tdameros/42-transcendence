import * as THREE from 'three';
import {RectAreaLightUniformsLib} from 'three/addons';

export class _ThreeJS {
    constructor() {
        this._initRenderer();
        this._initCamera();
        window.addEventListener('resize', () => {
            this._onWindowResize();
        }, false);
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

        this._camera.position.set(0., 0., 50.);
        this._defaultCameraDirection = new THREE.Vector3(0., 0., -1.);
        this._camera.lookAt(this._defaultCameraDirection.x,
                            this._defaultCameraDirection.y,
                            this._defaultCameraDirection.z);
    }

    _onWindowResize() {
        this._renderer.setSize(window.innerWidth, window.innerHeight);

        this._camera.aspect = window.innerWidth / window.innerHeight;
        this._camera.updateProjectionMatrix();
    }

    setCameraPosition(position) {
        this._camera.position.set(position.x, position.y, position.z);
    }

    setAnimationLoop(loopFunction) {
        this._renderer.setAnimationLoop(loopFunction);
    }

    stopAnimationLoop() {
        this._renderer.setAnimationLoop(null);
    }

    renderFrame(scene) {
        this._renderer.render(scene, this._camera);
    }
}