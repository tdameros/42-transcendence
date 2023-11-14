import * as THREE from 'three';

export function initScene() {
    const scene = new THREE.Scene();
    
    const group = new THREE.Group();
    scene.add(group);
    
    const geometry = new THREE.BoxGeometry(1, 1, 1);
    const material = new THREE.MeshBasicMaterial({color: 0x00ff00});
    const cube1 = new THREE.Mesh(geometry, material);
    cube1.position.set(0, 1.5, 0);
    group.add(cube1);
    
    const cube2 = new THREE.Mesh(geometry, material);
    cube2.position.set(0, -1.5, 0);
    group.add(cube2);
    
    group.position.set(0, 0, 0);

    return {
        scene: scene,
        objects: {
            cubes: {
                group: group,
                cube1: cube1,
                cube2: cube2
            }
        }
    };
}
