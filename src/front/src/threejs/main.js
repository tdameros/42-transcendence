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

    const {scene, objects} = initScene();

    function animate() {
        const currentTime = new Date().getTime() % 0.025;
    
        objects.cubes.cube1.rotation.x += currentTime;
        objects.cubes.cube1.rotation.y += Math.abs(Math.sin(currentTime)) / 1.5;
        
        objects.cubes.cube2.rotation.x = -objects.cubes.cube1.rotation.x
        objects.cubes.cube2.rotation.y = -objects.cubes.cube1.rotation.y
    
        objects.cubes.group.rotation.x = objects.cubes.cube1.rotation.x;
        objects.cubes.group.rotation.z = objects.cubes.cube1.rotation.y;
        objects.cubes.group.rotation.y = (objects.cubes.cube1.rotation.x
                                         + objects.cubes.cube1.rotation.y) / 2;
    
        requestAnimationFrame(animate);
        renderer.render(scene, camera);
    }
    animate()
}
