import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';

export class _Board {
  #threeJSBoard;
  #score = [];
  #points = 0;

  constructor() {}

  async init(boardJson, index, maxScore) {
    const wallWidth = 1;
    this.#threeJSBoard = new THREE.Group();
    const boardSize = boardJson['size'];
    boardSize.z = 1;
    await this.initBoard(boardSize, index);
    await this.initWalls(boardSize);
    this.initGoal(boardSize, wallWidth, index);
    this.initScore(boardSize, wallWidth, index, maxScore);
    this.initLight(boardSize, index);
    this.#threeJSBoard.castShadow = false;
    this.#threeJSBoard.receiveShadow = true;
  }

  async initBoard(boardSize, index) {
    const gltf = await this.loadGLTFModel('/assets/models/board.glb');
    const board = gltf.scene;
    if (index === 1) {
      board.rotateZ(Math.PI);
    }
    const boundingBox = new THREE.Box3().setFromObject(board);
    const size = new THREE.Vector3();
    boundingBox.getSize(size);
    board.position.set(0., 0., 0.);
    board.scale.set(
        boardSize.x / size.x,
        boardSize.y / size.y,
        boardSize.z / size.z,
    );
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
        boardSize.z / size.z * 2,
    );
    return wall;
  }

  initLight(boardSize, index) {
    let sign = 1;
    if (index === 0) {
      sign = -1;
    }
    const light = new THREE.PointLight(0xffffff, 250);
    light.position.set(sign * boardSize['x'] / 2 + sign * 5, boardSize['y'] / 2 + 5, 10);
    this.#threeJSBoard.add(light.clone());
    light.position.set(sign * boardSize['x'] / 2 + sign * 5, -boardSize['y'] / 2 - 5, 10);
    this.#threeJSBoard.add(light.clone());
    if (sign === 1) {
      light.position.set(-sign * boardSize['x'] / 2, boardSize['y'] / 2 + 5, 10);
      this.#threeJSBoard.add(light.clone());
      light.position.set(-sign * boardSize['x'] / 2, -boardSize['y'] / 2 - 5, 10);
      this.#threeJSBoard.add(light.clone());
    }
  }

  initScore(boardSize, wallWidth, index, maxScore) {
    let sign = -1;
    if (index === 0) {
      sign = 1;
    }
    const pointRadius = wallWidth / 3;
    const pointOffset = sign * pointRadius * 3;
    const pointStartPosition = new THREE.Vector3(
        sign * boardSize.x / 2 - sign * boardSize.x / 6,
        boardSize.y / 2 + wallWidth / 2,
        boardSize.z,
    );

    for (let i = 0; i < maxScore; i++) {
      const point = this.initScorePoint(pointRadius);
      point.position.copy(pointStartPosition);
      point.position.x -= (pointOffset * i);
      this.#score.push(point);
      this.#threeJSBoard.add(point);
    }
  }

  initScorePoint(pointRadius) {
    const material = new THREE.MeshStandardMaterial({
      color: 0xf0f0f0,
      metalness: 0.5,
    });
    material.flatShading = true;
    return new THREE.Mesh(
        new THREE.IcosahedronGeometry(pointRadius),
        material,
    );
  }

  addPoint(score, color) {
    this.#score[this.#points].material.color.set(color);
    this.#points++;
  }

  resetPoints() {
    this.#points = 0;
    for (let i = 0; i < this.#score.length; i++) {
      this.#score[i].material.color.set(0xf0f0f0);
    }
  }

  initGoal(boardSize, wallWidth, index) {
    let sign = 1;
    if (index === 0) {
      sign = -1;
    }
    const goal = new THREE.Mesh(
        new THREE.BoxGeometry(wallWidth / 2, boardSize.y + wallWidth * 2, boardSize.z * 2),
        new THREE.MeshPhysicalMaterial({
          roughness: 0.2,
          metalness: 0.2,
          transmission: 1,
        }),
    );
    goal.position.set(sign * boardSize.x / 2 + sign * wallWidth / 4, 0, 0);
    this.#threeJSBoard.add(goal);
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
          (gltf) => {
            resolve(gltf);
          },
          undefined,
          (error) => {
            reject(error);
          },
      );
    });
  }
}
