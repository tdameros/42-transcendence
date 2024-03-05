import * as THREE from 'three';
import {RectAreaLightUniformsLib} from 'three/addons';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {NavbarUtils} from '@utils/NavbarUtils.js';

export class _ThreeJS {
  #renderer;
  #camera;
  #engine;
  #controls;

  constructor(engine) {
    this.#engine = engine;
    this.#initRenderer();
    this.#initCamera();
    this.#controls = new OrbitControls(this.#camera, this.#renderer.domElement);
    this.#controls.target.set(0, 0, 0);
    this.#engine.component.addComponentEventListener(window, 'resize',
        () => {
          this.#onWindowResize();
          this.#engine.resizeHandler();
        }, this,
    );
  }

  get width() {
    const style = window.getComputedStyle(this.#engine.component.container);
    const marginLeft = style.getPropertyValue('margin-left');
    const marginRight = style.getPropertyValue('margin-right');
    return window.innerWidth - parseInt(marginLeft) - parseInt(marginRight);
  }

  get height() {
    const style = window.getComputedStyle(this.#engine.component.container);
    const marginTop = style.getPropertyValue('margin-top');
    const marginBottom = style.getPropertyValue('margin-bottom');
    return window.innerHeight - NavbarUtils.height -
      parseInt(marginTop) - parseInt(marginBottom) - 2;
  }

  #initRenderer() {
    this.#renderer = new THREE.WebGLRenderer({antialias: false});

    this.#renderer.shadowMap.enabled = true;
    this.#renderer.shadowMap.type = THREE.PCFSoftShadowMap;

    this.#renderer.setPixelRatio(window.devicePixelRatio * 0.5);
    this.#renderer.setSize(this.width, this.height);

    this.#renderer.domElement.classList.add('rounded');
    this.#engine.component.container.appendChild(this.#renderer.domElement);
    RectAreaLightUniformsLib.init();
  }

  #initCamera() {
    this.#camera = new THREE.PerspectiveCamera(59,
        this.width / this.height,
        0.1,
        1000);

    this.#camera.position.set(15, -52, 17);
    this.#camera.lookAt(0., 0., -1.);
    this.#camera.up.set( 0, 0, 1 );
  }

  #onWindowResize() {
    this.#renderer.setSize(this.width, this.height);

    this.#camera.aspect = this.width / this.height;
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
    const aspect = this.width / this.height;
    return 2. * Math.atan(Math.tan(vFOV / 2.) * aspect);
  }

  setAnimationLoop(loopFunction) {
    this.#renderer.setAnimationLoop(loopFunction);
  }

  stopAnimationLoop() {
    this.#renderer.setAnimationLoop(null);
  }

  updateControls() {
    this.#controls.update();
  }

  renderFrame(scene) {
    this.#renderer.render(scene, this.#camera);
  }

  get controls() {
    return this.#controls;
  }
}
