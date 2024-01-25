import WebGL from 'three/addons/capabilities/WebGL.js';

import {Engine} from './Engine/Engine.js'
import * as THREE from "three";

main();

function main() {
    if (!WebGL.isWebGLAvailable()) {
        document.querySelector('#container')
                .appendChild(WebGL.getWebGLErrorMessage());
        return;
    }

    const engine = new Engine();

    displayScene(engine);
    engine.connectToServer();
}

function displayScene(engine) {
    let clock = new THREE.Clock();

    engine.setAnimationLoop(() => {
        const delta = clock.getDelta();
        engine.scene.updateFrame(delta);

        engine.renderFrame();
    });
}