import * as THREE from 'three';
import WebGL from 'three/addons/capabilities/WebGL.js';

import {Engine} from './Engine.js'
import {initScene} from './initScene.js'

main();

function main() {
    if (!WebGL.isWebGLAvailable()) {
        const warning = WebGL.getWebGLErrorMessage();
        document.getElementById('container').appendChild(warning);
        return;
    }

    const engine = new Engine();

    let {scene, objects} = initScene();

    const boardBounds = getBoardBounds(objects.board, objects.cube1);

    let cube1Direction = new THREE.Vector3(0.3, -0.3, 0);
    let cube2Direction = new THREE.Vector3(-0.3, 0.3, 0);
    let clock = new THREE.Clock();
    function animate() {
        const delta = clock.getDelta();
        // engine.handlePressedKeys()
        updateCubePosition(objects.cube1, cube1Direction, boardBounds);
        updateCubePosition(objects.cube2, cube2Direction, boardBounds);

        requestAnimationFrame(animate);
        engine._controls.update(delta);
        window.dispatchEvent(new MouseEvent('mousemove',
                                            {clientX: window.innerWidth / 2,
                                             clientY: window.innerHeight / 2}));
        engine._renderer.render(scene, engine._camera);
    }
    animate()
}

function getBoardBounds(board, cube) {
    let boundingBox = new THREE.Box3().setFromObject(board);
    const boardSize = new THREE.Vector3();
    boundingBox.getSize(boardSize);

    boundingBox.setFromObject(cube);
    const cubeSize = new THREE.Vector3();
    boundingBox.getSize(cubeSize);

    return {
        ceiling: board.position.y + boardSize.y / 2. - cubeSize.y / 2.,
        floor: board.position.y - boardSize.y / 2. + cubeSize.y / 2.,

        leftWall: board.position.x - boardSize.x / 2. + cubeSize.z / 2.,
        rightWall: board.position.x + boardSize.x / 2. - cubeSize.z / 2.
    };
}

function updateCubePosition(cube, cubeDirection, boardBounds) {
    cube.position.set(cube.position.x + cubeDirection.x,
                        cube.position.y + cubeDirection.y,
                        cube.position.z + cubeDirection.z);

    const moduloValue = .4;
    const bias = .8;
    if (cube.position.x < boardBounds.leftWall) {
        cube.position.x = boardBounds.leftWall;
        cubeDirection.x *= -(Math.random() % moduloValue + bias)
    }
    else if (cube.position.x > boardBounds.rightWall) {
        cube.position.x = boardBounds.rightWall;
        cubeDirection.x *= -(Math.random() % moduloValue + bias)
    }

    if (cube.position.y < boardBounds.floor) {
        cube.position.y = boardBounds.floor;
        cubeDirection.y *= -(Math.random() % moduloValue + bias)
    }
    else if (cube.position.y > boardBounds.ceiling) {
        cube.position.y = boardBounds.ceiling;
        cubeDirection.y *= -(Math.random() % moduloValue + bias)
    }
}
