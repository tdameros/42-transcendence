import * as THREE from 'three';
import WebGL from 'three/addons/capabilities/WebGL.js';

import {initThreeJS} from './initThreeJS.js'
import {initScene} from './initScene.js'

main();

function main() {
    if (!WebGL.isWebGLAvailable()) {
        const warning = WebGL.getWebGLErrorMessage();
        document.getElementById('container').appendChild(warning);
        return;
    }

    const {renderer, camera} = initThreeJS();

    let {scene, objects} = initScene();

    const boardBounds = getBoardBounds(objects.board, objects.player1);

    let player1Direction = new THREE.Vector3(0.3, -0.3, 0);
    let player2Direction = new THREE.Vector3(-0.3, 0.3, 0);
    function animate() {
        updatePlayerPosition(objects.player1, player1Direction, boardBounds);
        updatePlayerPosition(objects.player2, player2Direction, boardBounds);

        requestAnimationFrame(animate);
        renderer.render(scene, camera);
    }
    animate()
}

function getBoardBounds(board, player) {
    let boundingBox = new THREE.Box3().setFromObject(board);
    const boardSize = new THREE.Vector3();
    boundingBox.getSize(boardSize);

    boundingBox.setFromObject(player);
    const playerSize = new THREE.Vector3();
    boundingBox.getSize(playerSize);

    return {
        ceiling: board.position.y + boardSize.y / 2 - playerSize.y,
        floor: board.position.y - boardSize.y / 2  + playerSize.y,

        leftWall: board.position.x - boardSize.x / 2 + playerSize.z,
        rightWall: board.position.x + boardSize.x / 2 - playerSize.z
    };
}

function updatePlayerPosition(player, playerDirection, boardBounds) {
    player.position.set(player.position.x + playerDirection.x,
                        player.position.y + playerDirection.y,
                        player.position.z + playerDirection.z);

    const moduloValue = .4;
    const bias = .8;
    if (player.position.x < boardBounds.leftWall) {
        player.position.x = boardBounds.leftWall;
        playerDirection.x *= -(Math.random() % moduloValue + bias)
    }
    else if (player.position.x > boardBounds.rightWall) {
        player.position.x = boardBounds.rightWall;
        playerDirection.x *= -(Math.random() % moduloValue + bias)
    }

    if (player.position.y < boardBounds.floor) {
        player.position.y = boardBounds.floor;
        playerDirection.y *= -(Math.random() % moduloValue + bias)
    }
    else if (player.position.y > boardBounds.ceiling) {
        player.position.y = boardBounds.ceiling;
        playerDirection.y *= -(Math.random() % moduloValue + bias)
    }
}
