import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import TWEEN from '@tweenjs/tween.js'


let canva = document.getElementById("rendererCanvas");
const renderer = new THREE.WebGLRenderer({antialias: true, canvas: canva});
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 10000);
camera.position.set(0, 20, 100);

const controls = new OrbitControls(camera, renderer.domElement);
controls.update();

const loader = new GLTFLoader();
const ambientLight = new THREE.AmbientLight(0xFFFFFF, 0.1);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
directionalLight.position.set(0, 1, 0);
scene.add(directionalLight);
loader.load(
    './pokemon_arena/scene.gltf',
    (gltf) => {
        const model = gltf.scene;
        const material = new THREE.MeshBasicMaterial({color: 0xff0000});
        model.position.set(0, 0, -10);
        model.scale.set(50, 50, 50);
        scene.add(model);
        // Optionnel : ajuster la position, l'échelle ou la rotation du modèle
        animate(); // Lancer l'animation après le chargement du modèle
    },
    undefined,
    (error) => {
        console.error('Erreur de chargement du modèle', error);
    }
);

// Création d'une animation de déplacement de la caméra
let initialCameraPosition = {x: 0, y: 10, z: 5}; // Position initiale de la caméra
let targetCameraPosition = {x: -10, y: 100, z: 8}; // Position vers laquelle déplacer la caméra

let tween = new TWEEN.Tween(initialCameraPosition)
    .to(targetCameraPosition, 5000) // Durée de l'animation en millisecondes
    .easing(TWEEN.Easing.Quadratic.InOut) // Type d'interpolation pour l'animation
    .onUpdate(() => {
        camera.position.set(initialCameraPosition.x, initialCameraPosition.y, initialCameraPosition.z);
    })
    .start(); // Démarre l'animation

function animate() {
    requestAnimationFrame(animate);
    TWEEN.update();
    controls.update();
    renderer.render(scene, camera);
    const rendererCanvas = document.querySelector('#rendererCanvas'); // Sélectionne le canvas créé par Three.js
    const container = document.querySelector('#container'); // Sélectionne le conteneur div

// Déplace le canvas créé par Three.js dans le conteneur div
    container.appendChild(rendererCanvas);

}

// Gestion du redimensionnement de la fenêtre
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});
