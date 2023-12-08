import * as THREE from 'three';

export function initScene() {
    const scene = new THREE.Scene();

    let light = new THREE.DirectionalLight(0xFFFFFF, 10.0);
    light.position.set(20, 5, 10);
    light.target.position.set(0, 0, 0);
    light.castShadow = true;
    light.shadow.bias = -0.001;
    light.shadow.mapSize.width = 2048;
    light.shadow.mapSize.height = 2048;
    light.shadow.camera.near = 0.1;
    light.shadow.camera.far = 50.0;
    light.shadow.camera.left = 25;
    light.shadow.camera.right = -25;
    light.shadow.camera.top = 25;
    light.shadow.camera.bottom = -25;
    scene.add(light);
    //Create a helper for the shadow camera (optional)
//    const helper = new THREE.CameraHelper( light.shadow.camera );
//    scene.add( helper );

    light = new THREE.AmbientLight(0x101010, 0);
    scene.add(light);
    
    const cubeGeometry = new THREE.BoxGeometry(1, 1, 1);
    let cube1 = new THREE.Mesh(cubeGeometry,
                               new THREE.MeshStandardMaterial({color: 0x00ff00}));
    cube1.position.set(-17, 0, 0.5);
    cube1.castShadow = true;
    cube1.receiveShadow = true;
    scene.add(cube1);
    
    let cube2 = new THREE.Mesh(cubeGeometry,
                               new THREE.MeshStandardMaterial({color: 0xff0000}));
    cube2.position.set(17, 0, 0.5);
    cube2.castShadow = true;
    cube2.receiveShadow = true;
    scene.add(cube2);


    let board = new THREE.Mesh(new THREE.PlaneGeometry(40, 20),
                               new THREE.MeshStandardMaterial({color: 0x0000ff}));
    board.position.set(0, 0, 0);
    board.castShadow = false;
    board.receiveShadow = true;
    scene.add(board);

    return {
        scene: scene,
        objects: {
            cube1: cube1,
            cube2: cube2,
            board: board
        }
    };
}
