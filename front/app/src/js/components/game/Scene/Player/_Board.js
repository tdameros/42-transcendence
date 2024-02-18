import * as THREE from 'three';

export class _Board {
  #threeJSBoard;

  constructor(boardJson) {
    const size = boardJson['size'];
    this.#threeJSBoard = new THREE.Mesh(
        new THREE.PlaneGeometry(size['x'], size['y']),
        new THREE.MeshStandardMaterial({
          color: 0x000044,
          side: THREE.DoubleSide,
        }),
    );
    this.#threeJSBoard.position.set(0., 0., 0.);
    this.#threeJSBoard.castShadow = false;
    this.#threeJSBoard.receiveShadow = true;
  }

  updateFrame(timeDelta) {
    return;
  }

  get threeJSBoard() {
    return this.#threeJSBoard;
  }
}
