import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';

export class _Board {
  #threeJSBoard;
  #pointElevation;
  #points = [];
  #delays = [];
  #score = 0;
  #side;
  #pointColor;
  #board;
  #goal;

  static #leftSideColor = 0x00ff00;
  static #rightSideColor = 0xff0000;

  constructor() {}

  async init(boardJson, side, maxScore) {
    this.#side = side;
    this.#pointColor = this.#side ?
        _Board.#rightSideColor : _Board.#leftSideColor;
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
    this.#board = gltf.scene;
    if (this.#side === 1) {
      this.#board.rotateZ(Math.PI);
    }
    const boundingBox = new THREE.Box3().setFromObject(this.#board);
    const size = new THREE.Vector3();
    boundingBox.getSize(size);
    this.#board.position.set(0., 0., 0.);
    this.#board.scale.set(
        boardSize.x / size.x,
        boardSize.y / size.y,
        boardSize.z / size.z,
    );
    this.#threeJSBoard.add(this.#board);
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
    const light = new THREE.PointLight(0xffffff, 250);
    light.position.set(0, 0, 10);
    this.#threeJSBoard.add(light.clone());
  }

  initScore(boardSize, wallWidth, maxScore) {
    let sign = -1;
    if (this.#side === 0) {
      sign = 1;
    }
    const pointRadius = wallWidth / 1.5;
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
    }
  }

  initPointMesh(pointRadius) {
    const material = new THREE.MeshStandardMaterial({
      color: 0xa0a0a0,
    });
    material.flatShading = true;
    return new THREE.Mesh(
        new THREE.IcosahedronGeometry(pointRadius),
        material,
    );
  }

  addPoint() {
    this.#points[this.#score].material.color.set(this.#pointColor);

    this.#score++;
  }

  resetPoints() {
    this.#score = 0;
    for (let i = 0; i < this.#points.length; i++) {
      this.#points[i].material.color.set(0xf0f0f0);
    }
  }

  get score() {
    return this.#score;
  }

  initGoal(boardSize, wallWidth) {
    let sign = 1;
    if (this.#side === 0) {
      sign = -1;
    }
    this.#goal = new THREE.Mesh(
        new THREE.BoxGeometry(
            wallWidth / 2,
            boardSize.y + wallWidth * 2,
            boardSize.z * 2,
        ),
        new THREE.MeshPhysicalMaterial({
          roughness: 0.2,
          metalness: 0.2,
          transmission: 1,
        }),
    );
    this.#goal.position
        .set(sign * boardSize.x / 2 + sign * wallWidth / 4, 0, 0);
    this.#threeJSBoard.add(this.#goal);
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

  changeSide() {
    this.#side = 1 - this.#side;
    this.#pointColor = this.#side ?
        _Board.#rightSideColor : _Board.#leftSideColor;
    this.#board.rotateZ(Math.PI);
    for (const point of this.#points) {
      point.position.x *= -1;
    }
    this.#goal.position.x *= -1;
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
