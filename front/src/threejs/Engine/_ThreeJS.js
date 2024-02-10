import * as THREE from 'three';
import {RectAreaLightUniformsLib} from 'three/addons';

export class _ThreeJS {
  #renderer;
  #camera;
  #defaultCameraDirection;

  constructor() {
    this.#initRenderer();
    this.#initCamera();
    window.addEventListener('resize', () => {
      this.#onWindowResize();
    }, false);
  }

  #initRenderer() {
    this.#renderer = new THREE.WebGLRenderer({antialias: true});

    this.#renderer.shadowMap.enabled = true;
    this.#renderer.shadowMap.type = THREE.PCFSoftShadowMap;

    this.#renderer.setPixelRatio(window.devicePixelRatio);
    this.#renderer.setSize(window.innerWidth, window.innerHeight);

    document.body.appendChild(this.#renderer.domElement);
    RectAreaLightUniformsLib.init();
  }

  #initCamera() {
    this.#camera = new THREE.PerspectiveCamera(90,
        window.innerWidth / window.innerHeight,
        0.1,
        1000);

    this.#camera.position.set(0., 0., 50.);
    this.#defaultCameraDirection = new THREE.Vector3(0., 0., -1.);
    this.#camera.lookAt(this.#defaultCameraDirection.x,
        this.#defaultCameraDirection.y,
        this.#defaultCameraDirection.z);
  }

  #onWindowResize() {
    this.#renderer.setSize(window.innerWidth, window.innerHeight);

    this.#camera.aspect = window.innerWidth / window.innerHeight;
    this.#camera.updateProjectionMatrix();
  }

  setCameraPosition(position) {
    this.#camera.position.set(position.x, position.y, position.z);
  }

  setAnimationLoop(loopFunction) {
    this.#renderer.setAnimationLoop(loopFunction);
  }

  stopAnimationLoop() {
    this.#renderer.setAnimationLoop(null);
  }

  renderFrame(scene) {
    this.#renderer.render(scene, this.#camera);
  }
}
