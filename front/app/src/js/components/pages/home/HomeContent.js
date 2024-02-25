import {Component} from '@components';
import * as THREE from 'three';
import WebGL from 'three/addons/capabilities/WebGL.js';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {NavbarUtils} from '@utils/NavbarUtils.js';

export class HomeContent extends Component {
  constructor() {
    super();
  }
  render() {
    return (`
      <div id="container" class="m-2 card">
        <div id="text" class="flex-column position-absolute">
          <h1 class="fw-bolder">The Pong Battle Ground!</h1>
          <p>Challenge the elite</p>
          <p>Rise though the ranks</p>
          <p>Dominate the pong arena</p>
          <multiplayer-content-component></multiplayer-content-component>
        </div>
      </div>
    `);
  }
  style() {
    return (`
      <style>
        #container {
            background: linear-gradient(90deg, rgba(114,151,255,1) 0%, rgba(85,118,227,1) 30%, rgba(40,43,232,1) 100%);
        }
        @media only screen and (min-aspect-ratio: 1/1) {
            #text {
                top: 50%;
                left: 75%;
                transform: translateX(-50%) translateY(-50%);
            }
        }
        @media only screen and (max-aspect-ratio: 1/1) {
            #text {
                top: 10%;
                left: 50%;
                transform: translateX(-50%);
            }
        }
      </style>
    `);
  }
  async postRender() {
    this.container = document.querySelector('#container');

    await this.init();
    this.container.appendChild(this.renderer.domElement);

    this.renderer.setAnimationLoop(() => {
      this.renderer.render(this.scene, this.camera);
      this.island.rotation.y += 0.0005;
    });

    super.addComponentEventListener(window, 'resize', this.resizeEvent);
  }

  async init() {
    if (!WebGL.isWebGLAvailable()) {
      this.container.appendChild(WebGL.getWebGLErrorMessage());
      return;
    }
    this.scene = new THREE.Scene();
    this.island = await this.getGLTFObject('/assets/models/transcendence.glb');
    this.boundingBox = new THREE.Box3().setFromObject(this.island);
    this.size = new THREE.Vector3();
    this.boundingBox.getSize(this.size);
    this.setObjectPosition(this.island);
    this.camera = this.initCamera(this.island, this.size);
    this.renderer = this.initRenderer();
    this.scene.add(this.island);
    this.setLights(this.scene, this.island);
  }

  resizeEvent(event) {
    this.renderer.setSize(
        this.getContainerWidth(),
        this.getContainerHeight(),
    );

    this.camera.aspect = this.getContainerWidth() / (this.getContainerHeight());
    this.camera.updateProjectionMatrix();
    this.setCameraPosition(this.camera, this.island, this.size);
  }

  initRenderer() {
    const renderer = new THREE.WebGLRenderer({antialias: true});

    renderer.setSize(
        this.getContainerWidth(),
        this.getContainerHeight(),
    );
    renderer.autoClear = false;
    return renderer;
  }

  initCamera(object, size) {
    const camera = new THREE.PerspectiveCamera(
        75,
        this.getContainerWidth() / this.getContainerHeight(),
        0.1,
        1000,
    );

    this.setCameraPosition(camera, object, size);
    return camera;
  }

  getContainerHeight() {
    const style = window.getComputedStyle(this.container);
    const marginTop = style.getPropertyValue('margin-top');
    const marginBottom = style.getPropertyValue('margin-bottom');
    return window.innerHeight - NavbarUtils.height -
        parseInt(marginTop) - parseInt(marginBottom) - 2;
  }

  getContainerWidth() {
    const style = window.getComputedStyle(this.container);
    const marginLeft = style.getPropertyValue('margin-left');
    const marginRight = style.getPropertyValue('margin-right');
    return window.innerWidth - parseInt(marginLeft) - parseInt(marginRight);
  }

  setCameraPosition(camera, object, size) {
    camera.position.y = object.position.y + size.y;
    camera.position.z = object.position.z + size.z;
    camera.position.x = 0;
    camera.lookAt(0, 0, 0);
    if (window.innerWidth > window.innerHeight) {
      camera.position.x -= window.innerHeight / window.innerWidth - 1;
    } else {
      camera.position.y -= window.innerWidth / window.innerHeight - 1;
    }
  }

  async getGLTFObject(path) {
    const gltf = await this.loadGLTFModel(path);
    return gltf.scene;
  }

  setObjectPosition(object) {
    const boundingBoxCenter = new THREE.Vector3();
    this.boundingBox.getCenter(boundingBoxCenter);
    const offset = new THREE.Vector3()
        .copy(object.position)
        .sub(boundingBoxCenter);

    object.position.add(offset);
  }

  setLights(scene, object) {
    const hemisphereLight = new THREE.HemisphereLight(0xFFFFFF, 0x000010);
    const directionalLight = new THREE.DirectionalLight(0xFFFFFF, 2.0);

    directionalLight.position.set(
        object.position.x + this.size.x,
        object.position.y + this.size.y,
        object.position.z + this.size.z,
    );
    directionalLight.target.position.set(
        object.position.x,
        object.position.y,
        object.position.z,
    );
    directionalLight.castShadow = true;
    scene.add(directionalLight);
    scene.add(hemisphereLight);
  }

  loadGLTFModel(path) {
    const loader = new GLTFLoader();

    return new Promise((resolve, reject) => {
      loader.load(path, (gltf) => {
        resolve(gltf);
      }, undefined, reject);
    });
  }
}
