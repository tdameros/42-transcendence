import {Component} from '@components';
import * as THREE from 'three';
import WebGL from 'three/addons/capabilities/WebGL.js';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';

export class HomeContent extends Component {
  constructor() {
    super();
  }
  render() {
    return (`
      <navbar-component nav-active="home"></navbar-component>
      <div id="container">
        <div id="text" class="flex-column position-absolute">
          <h1 class="fw-bolder">The Pong Battle Ground!</h1>
          <p>Challenge the elite</p>
          <p>Rise though the ranks</p>
          <p>Dominate the pong arena</p>
          <multiplayer-component></multiplayer-component>
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
    this.navbar_height = document.querySelector('.navbar').offsetHeight;
    const container = document.querySelector('#container');
    if (!WebGL.isWebGLAvailable()) {
      container.appendChild(WebGL.getWebGLErrorMessage());
      return;
    }
    const scene = new THREE.Scene();
    const island = await this.getGLTFObject('/assets/models/transcendence.glb');
    const boundingBox = new THREE.Box3().setFromObject(island);
    const size = new THREE.Vector3();
    boundingBox.getSize(size);
    const camera = this.initCamera(island, size);
    const renderer = this.initRenderer();
    scene.add(island);
    this.setLights(scene, island);

    container.appendChild(renderer.domElement);

    renderer.setAnimationLoop(() => {
      renderer.render(scene, camera);
      island.rotation.y += 0.0005;
    });

    window.addEventListener('resize', () => {
      renderer.setSize(
          window.innerWidth,
          window.innerHeight - this.navbar_height,
      );

      camera.aspect = window.innerWidth / (
        window.innerHeight - this.navbar_height
      );
      camera.updateProjectionMatrix();
      this.setCameraPosition(camera, island, size);
    }, false);
  }

  initRenderer() {
    const renderer = new THREE.WebGLRenderer({antialias: true});

    renderer.setSize(
        window.innerWidth,
        window.innerHeight - this.navbar_height,
    );
    renderer.autoClear = false;
    return renderer;
  }

  initCamera(object, size) {
    const camera = new THREE.PerspectiveCamera(
        75,
        window.innerWidth / (window.innerHeight - this.navbar_height),
        0.1,
        1000,
    );

    this.setCameraPosition(camera, object, size);
    return camera;
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
    const object = gltf.scene;
    const boundingBox = new THREE.Box3().setFromObject(object);
    const boundingBoxCenter = new THREE.Vector3();
    boundingBox.getCenter(boundingBoxCenter);
    const offset = new THREE.Vector3()
        .copy(object.position)
        .sub(boundingBoxCenter);

    object.position.add(offset);
    return object;
  }

  setLights(scene, object) {
    const hemisphereLight = new THREE.HemisphereLight(0xFFFFFF, 0x000010);
    const directionalLight = new THREE.DirectionalLight(0xFFFFFF, 2.0);

    const boundingBox = new THREE.Box3().setFromObject(object);
    const size = new THREE.Vector3();
    boundingBox.getSize(size);
    directionalLight.position.set(
        object.position.x + size.x,
        object.position.y + size.y,
        object.position.z + size.z,
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
