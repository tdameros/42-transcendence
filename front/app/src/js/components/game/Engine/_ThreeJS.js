import * as THREE from 'three';
import {RectAreaLightUniformsLib} from 'three/addons';

export class _ThreeJS {
  #renderer;
  #camera;
  #engine;

  constructor(engine) {
    this.#initRenderer();
    this.#initCamera();
    this.#engine = engine;
    window.addEventListener('resize', () => {
      this.#onWindowResize();
      this.#engine.resizeHandler();
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
    this.#camera = new THREE.PerspectiveCamera(59,
        window.innerWidth / window.innerHeight,
        0.1,
        1000);

    this.#camera.position.set(0., 0., 70.);
    this.#camera.lookAt(0., 0., -1.);
  }

  #onWindowResize() {
    this.#renderer.setSize(window.innerWidth, window.innerHeight);

    this.#camera.aspect = window.innerWidth / window.innerHeight;
    this.#camera.updateProjectionMatrix();
  }

  setCameraPosition(position) {
    this.#camera.position.set(position.x, position.y, position.z);
  }

  setCameraLookAt(position) {
    this.#camera.lookAt(position.x, position.y, position.z);
  }

  getCameraVerticalFOVRadian() {
    return this.#camera.fov * Math.PI / 180.;
  }

  getCameraHorizontalFOVRadian() {
    const vFOV = this.getCameraVerticalFOVRadian();
    const aspect = window.innerWidth / window.innerHeight;
    return 2. * Math.atan(Math.tan(vFOV / 2.) * aspect);
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
