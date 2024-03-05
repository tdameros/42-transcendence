import * as THREE from 'three';

export class LoadingScreenScene {
  #threeJSScene = new THREE.Scene();
  #ball1;
  #ball2;
  #ball1Direction = new THREE.Vector3(0.3, -0.3, 0.);
  #ball2Direction = new THREE.Vector3(-0.3, 0.3, 0.);
  #board;
  #boardBounds;

  constructor(matchesJson) {
    const ballGeometry = new THREE.BoxGeometry(1., 1., 1.);

    this.#ball1 = new THREE.Mesh(ballGeometry,
        new THREE.MeshStandardMaterial({color: 0x00ff00}));
    this.#ball1.position.set(-17., 0., 1);
    this.#ball1.castShadow = true;
    this.#ball1.receiveShadow = true;
    this.#threeJSScene.add(this.#ball1);

    this.#ball2 = new THREE.Mesh(ballGeometry,
        new THREE.MeshStandardMaterial({color: 0xff0000}));
    this.#ball2.position.set(17., 0., 1);
    this.#ball2.castShadow = true;
    this.#ball2.receiveShadow = true;
    this.#threeJSScene.add(this.#ball2);


    this.#board = new THREE.Mesh(
        new THREE.BoxGeometry(30, 20., 1.),
        new THREE.MeshStandardMaterial({color: 0x246FA8}),
    );
    this.#board.position.set(0., 0., 0.);
    this.#board.castShadow = false;
    this.#board.receiveShadow = true;
    this.#threeJSScene.add(this.#board);

    const light = new THREE.DirectionalLight(0xFFFFFF, 10.0);
    light.position.set(20., -5, 10.);
    light.target.position.set(0., 0., 0.);
    light.castShadow = true;
    light.shadow.bias = -0.01;
    light.shadow.camera.near = 0.1;
    light.shadow.camera.far = 50.0;
    light.shadow.camera.left = 25.;
    light.shadow.camera.right = -25.;
    light.shadow.camera.top = 25.;
    light.shadow.camera.bottom = -25.;
    light.shadow.mapSize.width = 2048;
    light.shadow.mapSize.height = 2048;
    this.#threeJSScene.add(light);

    this.#setBoardBounds();
  }

  updateFrame(timeDelta) {
    this.#updateCubePosition(this.#ball1, this.#ball1Direction);
    this.#updateCubePosition(this.#ball2, this.#ball2Direction);
  }

  get threeJSScene() {
    return this.#threeJSScene;
  }

  #setBoardBounds() {
    const boundingBox = new THREE.Box3().setFromObject(this.#board);
    const boardSize = new THREE.Vector3();
    boundingBox.getSize(boardSize);

    boundingBox.setFromObject(this.#ball1);
    const ballSize = new THREE.Vector3();
    boundingBox.getSize(ballSize);

    this.#boardBounds = {
      ceiling: this.#board.position.y + boardSize.y / 2. - ballSize.y / 2.,
      floor: this.#board.position.y - boardSize.y / 2. + ballSize.y / 2.,

      leftWall: this.#board.position.x - boardSize.x / 2. + ballSize.z / 2.,
      rightWall: this.#board.position.x + boardSize.x / 2. - ballSize.z / 2.,
    };
  }

  #updateCubePosition(ball, ballDirection) {
    ball.position.set(ball.position.x + ballDirection.x,
        ball.position.y + ballDirection.y,
        ball.position.z + ballDirection.z);

    const moduloValue = .4;
    const bias = .8;
    if (ball.position.x < this.#boardBounds.leftWall) {
      ball.position.x = this.#boardBounds.leftWall;
      ballDirection.x *= -(Math.random() % moduloValue + bias);
    } else if (ball.position.x > this.#boardBounds.rightWall) {
      ball.position.x = this.#boardBounds.rightWall;
      ballDirection.x *= -(Math.random() % moduloValue + bias);
    }

    if (ball.position.y < this.#boardBounds.floor) {
      ball.position.y = this.#boardBounds.floor;
      ballDirection.y *= -(Math.random() % moduloValue + bias);
    } else if (ball.position.y > this.#boardBounds.ceiling) {
      ball.position.y = this.#boardBounds.ceiling;
      ballDirection.y *= -(Math.random() % moduloValue + bias);
    }
  }
}
