import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';

export class _Board {
  #threeJSBoard;
  #gltfScene;

  constructor() {
    // const size = boardJson['size'];
    // this.#threeJSBoard = new THREE.Mesh(
    //     new THREE.PlaneGeometry(size['x'], size['y']),
    //     new THREE.MeshStandardMaterial({
    //       color: 0x000044,
    //       side: THREE.DoubleSide,
    //     }),
    // );
  }

  async init(boardJson, index){
    this.#threeJSBoard = new THREE.Group();
    const boardSize = boardJson['size'];
    boardSize.z = boardSize.x / 20;
    await this.initBoard(boardSize, index);
    await this.initWalls(boardSize);
    this.#threeJSBoard.castShadow = false;
    this.#threeJSBoard.receiveShadow = true;
  }

  async initBoard(boardSize, index) {
    this.#gltfScene = await this.loadGLTFModel('/assets/models/board.glb');
    const board = this.#gltfScene.scene;
    if (index === 1) {
      board.rotateZ(Math.PI);
    }
    const boundingBox = new THREE.Box3().setFromObject(board);
    const size = new THREE.Vector3();
    boundingBox.getSize(size);
    board.position.set(0., 0., 0.);
    board.scale.set(boardSize.x / size.x, boardSize.y / size.y, 10);
    this.#threeJSBoard.add(board);
  }

  async initWalls(boardSize) {
    const wallWidth = 1;
    const wallLeft = await this.initWall(boardSize, wallWidth);
    const wallRight = await this.initWall(boardSize, wallWidth);

    wallLeft.position.set(0, boardSize.y / 2 + wallWidth / 2, 0);
    wallRight.position.set(0, -boardSize.y / 2 - wallWidth / 2, 0);
    wallLeft.rotateZ(Math.PI);
    this.#threeJSBoard.add(wallLeft);
    this.#threeJSBoard.add(wallRight);
  }

  async initWall(boardSize, wallWidth) {
    let wall = await this.loadGLTFModel('/assets/models/wall.glb');
    wall = wall.scene;
    const boundingBox = new THREE.Box3().setFromObject(wall);
    const size = new THREE.Vector3();
    boundingBox.getSize(size);
    wall.scale.set(
        boardSize.x / size.x,
        wallWidth / size.y,
        wallWidth / size.z,
    );
    return wall;
  }

  async asyncConstructor() {
  }

  updateFrame(timeDelta) {
    return;
  }

  get threeJSBoard() {
    return this.#threeJSBoard;
  }

  loadGLTFModel(path) {
    const loader = new GLTFLoader();

    return new Promise((resolve, reject) => {
      loader.load(path,
          // onLoad callback
          (gltf) => {
            console.log("GLTF model loaded successfully:", gltf);
            resolve(gltf);
          },
          // onProgress callback
          (xhr) => {
            console.log((xhr.loaded / xhr.total * 100) + '% loaded');
          },
          // onError callback
          (error) => {
            console.error("An error occurred while loading the GLTF model:", error);
            reject(error);
          }
      );
    });
  }
}
