import * as THREE from "three";

export class _Board {
    #threeJsonBoard;

    constructor(boardJson) {
        const size = boardJson['size'];
        this.#threeJsonBoard = new THREE.Mesh(new THREE.PlaneGeometry(size['x'], size['y']),
                                              new THREE.MeshStandardMaterial({color: 0x222277}));
        this.#threeJsonBoard.position.set(0., 0., 0.);
        this.#threeJsonBoard.castShadow = false;
        this.#threeJsonBoard.receiveShadow = true;
    }

    updateFrame(timeDelta) {
        return;
    }

    get threeJSBoard() {
        return this.#threeJsonBoard;
    }


}