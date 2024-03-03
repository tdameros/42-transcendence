import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';

export class _Board {
  #threeJSBoard;
  #pointElevation;
  #points = [];
  #pointsLight = [];
  #delays = [];
  #score = 0;
  #side;
  #pointColor;

  constructor() {}

  async init(boardJson, side, maxScore, pointColor=0x00ff00) {
    this.#side = side;
    this.#pointColor = pointColor;
    const wallWidth = 1;
    this.#threeJSBoard = new THREE.Group();
    const boardSize = boardJson['size'];
    boardSize.z = 1;
    await this.initBoard(boardSize);
    await this.initWalls(boardSize);
    this.initGoal(boardSize, wallWidth);
    this.initScore(boardSize, wallWidth, maxScore);
    this.initLight(boardSize);
    this.#threeJSBoard.castShadow = false;
    this.#threeJSBoard.receiveShadow = true;
  }

  async initBoard(boardSize) {
    const gltf = await this.loadGLTFModel('/assets/models/board.glb');
    const board = gltf.scene;
    if (this.#side === 1) {
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

  initLight(boardSize) {
    let sign = 1;
    if (this.#side === 0) {
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

  initScore(boardSize, wallWidth, maxScore) {
    let sign = -1;
    if (this.#side === 0) {
      sign = 1;
    }
    const pointRadius = wallWidth /1.5;
    const pointOffset = sign * pointRadius * 3;
    const pointStartPosition = new THREE.Vector3(
        sign * boardSize.x / 2 - sign * boardSize.x / 6,
        boardSize.y / 2 + wallWidth / 2,
        boardSize.z + pointRadius * 2,
    );
    this.#pointElevation = pointStartPosition.z;

    for (let i = 0; i < maxScore; i++) {
      this.#delays.push(Math.random());
      const point = this.initPointMesh(pointRadius);
      point.position.copy(pointStartPosition);
      point.position.x -= (pointOffset * i);
      point.rotation.x = this.#delays[i] * Math.PI;
      point.rotation.y = this.#delays[i] * Math.PI;
      point.rotation.z = this.#delays[i] * Math.PI;
      this.#points.push(point);
      this.#threeJSBoard.add(point);
      this.initPointLight(point.position);
    }
  }

  initPointMesh(pointRadius) {
    const material = new THREE.MeshStandardMaterial({
      color: 0xf0f0f0,
      metalness: 0.8,
      roughness: 0.2,
    });
    material.flatShading = true;
    return new THREE.Mesh(
        new THREE.IcosahedronGeometry(pointRadius),
        material,
    );
  }

  initPointLight(pointPosition) {
    const light = new THREE.PointLight(this.#pointColor, 30, 10);
    light.position.copy(pointPosition);
    light.position.z += 2;
    this.#pointsLight.push(light);
  }

  addPoint() {
    this.#points[this.#score].material.color.set(this.#pointColor);
    this.#threeJSBoard.add(this.#pointsLight[this.#score]);

    this.#score++;
  }

  resetPoints() {
    this.#score = 0;
    for (let i = 0; i < this.#points.length; i++) {
      this.#points[i].material.color.set(0xf0f0f0);
    }
  }

  initGoal(boardSize, wallWidth) {
    let sign = 1;
    if (this.#side === 0) {
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

  updateFrame() {
    const currentTime = Date.now();
    const frequency = 300;
    const amplitude = 0.3;
    this.#points.forEach((point, index) => {
      const delayedTime = currentTime - (frequency / this.#delays[index]);
      const offset = Math.sin(delayedTime / frequency) * amplitude;
      point.position.z = this.#pointElevation + offset;
      point.rotation.x += Math.PI / frequency;
      point.rotation.y += Math.PI / frequency;
      point.rotation.z += Math.PI / frequency;
    });
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
