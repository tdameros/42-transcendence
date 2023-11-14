import * as THREE from 'three';

export function initScene() {
    const scene = new THREE.Scene();
    
    const playerGeometry = new THREE.BoxGeometry(1, 1, 1);
    let player1 = new THREE.Mesh(playerGeometry,
                                   new THREE.MeshBasicMaterial({color: 0x00ff00}));
    player1.position.set(-17, 0, 0);
    scene.add(player1);
    
    let player2 = new THREE.Mesh(playerGeometry,
                                   new THREE.MeshBasicMaterial({color: 0xff0000}));
    player2.position.set(17, 0, 0);
    scene.add(player2);


    let board = new THREE.Mesh(new THREE.PlaneGeometry(40, 20),
                                 new THREE.MeshBasicMaterial({color: 0x0000ff}));
    board.position.set(0, 0, -1);
    scene.add(board);

    return {
        scene: scene,
        objects: {
            player1: player1,
            player2: player2,
            board: board
        }
    };
}
