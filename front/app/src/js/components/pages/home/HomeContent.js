import {Component} from '@components';
import * as THREE from 'three';
import WebGL from 'three/addons/capabilities/WebGL.js';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {NavbarUtils} from '@utils/NavbarUtils.js';
import {Theme} from '@js/Theme.js';
import {userManagementClient} from '../../../utils/api/index.js';

export class HomeContent extends Component {
  constructor() {
    super();
  }
  render() {
    const theme = Theme.get();
    return (`
      <div id="container" class="m-2 rounded ${theme === 'light' ? 'light-background': 'dark-background'}">
        <div id="text" class="d-flex flex-column position-absolute">
        </div>
      </div>
    `);
  }
  style() {
    return (`
      <style>
      .light-background {
          background: linear-gradient(to bottom, #57c1eb 0%, #246fa8 100%);
      }
      
      .dark-background {
          background: linear-gradient(to bottom, #020111 10%, #3a3a52 100%);
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
      
      
      @keyframes title-animation {
          from {
              opacity: 0;
              transform: translateY(-20px);
          }
          to {
              opacity: 1;
              transform: translateY(0);
          }
      }
      
      .title {
          animation: title-animation 0.5s ease forwards;
      }
      
      @keyframes description-animation {
          from {
              opacity: 0;
              transform: translateX(+40px);
          }
          to {
              opacity: 1;
              transform: translateX(0);
          }
      }
      
      .description {
          animation: description-animation 1.5s ease forwards;
      }
      
      @keyframes action-button-animation {
          from {
              opacity: 0;
          }
          to {
              opacity: 1;
          }
      }
      
      .action-button {
          animation: action-button-animation 2s ease forwards;
      }
      </style>
    `);
  }
  async postRender() {
    this.container = document.querySelector('#container');
    if (!WebGL.isWebGLAvailable()) {
      this.container.appendChild(WebGL.getWebGLErrorMessage());
      return;
    }

    await this.initIslandScene();
    this.renderer = this.initRenderer();
    this.container.appendChild(this.renderer.domElement);
    this.camera = this.initCamera(this.island, this.size);

    this.renderer.setAnimationLoop(() => {
      this.renderer.render(this.scene, this.camera);
      this.island.rotation.y += 0.0005;
    });

    super.addComponentEventListener(window, 'resize', this.resizeEvent);
    super.addComponentEventListener(document, Theme.event, this.themeEvent);
    this.generateText();
  }

  resizeEvent(event) {
    this.renderer.setSize(
        this.getContainerWidth(),
        this.getContainerHeight(),
    );

    this.camera.aspect = this.getContainerWidth() / this.getContainerHeight();
    this.camera.updateProjectionMatrix();
    this.setCameraPosition(this.camera, this.island, this.size);
  }

  async themeEvent(event) {
    const rotation = this.island.rotation.y;
    this.scene.remove(this.island);
    if (Theme.get() === 'dark') {
      this.container.classList.remove('light-background');
      this.container.classList.add('dark-background');
    } else {
      this.container.classList.remove('dark-background');
      this.container.classList.add('light-background');
    }
    await this.initIslandScene();
    this.island.rotation.y = rotation;
  }

  async initIslandScene() {
    this.scene = new THREE.Scene();
    if (Theme.get() === 'light') {
      this.island = await this.getGLTFObject('/assets/models/island_light.glb');
    } else {
      this.island = await this.getGLTFObject('/assets/models/island_dark.glb');
    }
    this.island.castShadow = true;
    this.island.receiveShadow = true;
    this.setObjectPosition(this.island);
    this.setLights(this.island);
    this.scene.add(this.island);
  }

  initRenderer() {
    const renderer = new THREE.WebGLRenderer({antialias: true});

    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;

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

  setObjectPosition(object) {
    this.boundingBox = new THREE.Box3().setFromObject(this.island);
    this.size = new THREE.Vector3();
    this.boundingBox.getSize(this.size);
    this.boundingBoxCenter = new THREE.Vector3();
    this.boundingBox.getCenter(this.boundingBoxCenter);
    const offset = new THREE.Vector3()
        .copy(object.position)
        .sub(this.boundingBoxCenter);

    object.position.add(offset);
  }

  setLights(object) {
    if (Theme.get() === 'light') {
      this.#addSunLight(object);
    } else {
      this.#addMoonLight(object);
    }
    this.hemisphereLight = new THREE.HemisphereLight(0xFFFFFF, 0x000010, 0.5);
    this.scene.add(this.hemisphereLight);
  }

  #addSunLight(object) {
    this.sunLight = new THREE.DirectionalLight(0xFFFFFF, 2.0);
    this.sunLight.position.set(
        this.size.x, this.size.y, this.size.z,
    );
    this.sunLight.target.position.set(
        object.position.x, object.position.y, object.position.z,
    );
    this.sunLight.castShadow = true;
    this.sunLight.intensity = 2;
    this.sunLight.castShadow = true;
    this.sunLight.shadow.bias = -0.001;
    this.sunLight.shadow.mapSize.width = 2048;
    this.sunLight.shadow.mapSize.height = 2048;
    this.sunLight.shadow.camera.near = 0.1;
    this.sunLight.shadow.camera.far = 20.;
    this.sunLight.shadow.camera.left = .5;
    this.sunLight.shadow.camera.right = -.5;
    this.sunLight.shadow.camera.top = .5;
    this.sunLight.shadow.camera.bottom = -.5;
    object.add(this.sunLight);
  }

  #addMoonLight(object) {
    this.moonLight = new THREE.PointLight(0xFFFF00, 0.25);
    this.moonLight.position.set(-0.15, 1.20, -0.28);
    this.moonLight.castShadow = true;
    this.moonLight.shadow.bias = -0.001;
    this.moonLight.shadow.mapSize.width = 2048;
    this.moonLight.shadow.mapSize.height = 2048;
    this.moonLight.shadow.camera.near = 0.1;
    this.moonLight.shadow.camera.far = 1.;
    this.moonLight.shadow.camera.left = .5;
    this.moonLight.shadow.camera.right = -.5;
    this.moonLight.shadow.camera.top = .5;
    this.moonLight.shadow.camera.bottom = -.5;
    object.add(this.moonLight);
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

  loadGLTFModel(path) {
    const loader = new GLTFLoader();

    return new Promise((resolve, reject) => {
      loader.load(path, (gltf) => {
        gltf.scene.traverse(function(node ) {
          if ( node.type === 'Mesh' ) {
            node.castShadow = true;
            node.receiveShadow = true;
          }
        });
        resolve(gltf);
      }, undefined, reject);
    });
  }

  generateText() {
    this.querySelector('#text').innerHTML = this.renderText();
  }
  renderText() {
    return (`
      <h1 class="fw-bolder text-light title">The Pong Battle Ground!</h1>
      <p class="fw-light text-light description">Challenge your friends or face off against players from around the globe in fast-paced, head-to-head battles</p>
      ${this.renderButton()}
    `);
  }

  renderButton() {
    if (userManagementClient.isAuth()) {
      return (`
          <multiplayer-button-component class="action-button"></multiplayer-button-component>
      `);
    }
    return (`
        <div>
            <button class="btn btn-primary btn-lg action-button" onclick="window.router.navigate('/signin/')">Sign in</button>
        </div>
    `);
  }
}
