import * as THREE from 'three';

export function initThreeJS() {
    const renderer = initRenderer();
    const camera = initCamera(new THREE.Vector3(0, 0, 20),
                              new THREE.Vector3(0, 0, -1))
    let pressedKeys = []

    addResizeEventListener(renderer, camera);
    window.addEventListener('keydown', handleKeyDown.bind(null, pressedKeys));
    window.addEventListener('keyup', handleKeyUp.bind(null, pressedKeys));

    return {
        renderer: renderer,
        camera: camera,
        pressedKeys: pressedKeys
    };
}

function initRenderer() {
    const renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);
    return renderer;
}

function initCamera(position, lookAt) {
    const camera = new THREE.PerspectiveCamera(90,
        window.innerWidth / window.innerHeight,
        0.1,
        1000);
    camera.position.set(position.x, position.y, position.z);
    camera.lookAt(lookAt.x, lookAt.y, lookAt.z);
    return camera;
}


function addResizeEventListener(renderer, camera) {
    window.addEventListener('resize', function() {
        renderer.setSize(window.innerWidth, window.innerHeight);

        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
    });
}

function handleKeyDown(pressedKeys, event) {
    if (pressedKeys.includes(event.key.toLowerCase())) return;

    pressedKeys.push(event.key.toLowerCase());
}

function handleKeyUp(pressedKeys, event) {
    let keyToRemove = event.key.toLowerCase();
    let i = 0;
    while (i < pressedKeys.length) {
        if (pressedKeys[i] === keyToRemove) {
            pressedKeys.splice(i, 1);
            continue;
        }
        ++i;
    }
}
