import {Sky} from 'three/addons/objects/Sky.js';
import {Theme} from '@js/Theme.js';
import * as THREE from 'three';

export class SceneSky {
  #sky;
  #sun;

  constructor() {
    this.#sky = new Sky();
    this.#sun = new THREE.Vector3();
    this.#sky.scale.setScalar(45000);
    const uniforms = this.#sky.material.uniforms;
    uniforms.sunPosition.value.copy(this.#sun);
    uniforms.turbidity.value = 10;
    uniforms.rayleigh.value = 3;
    uniforms.mieCoefficient.value = 0.005;
    uniforms.mieDirectionalG.value = 0.7;
    if (Theme.get() === 'light') {
      this.setLightTheme();
    } else {
      this.setDarkTheme();
    }
    this.#sky.material.uniforms.up.value.set(0, 0, 1);
  }

  setLightTheme() {
    this.#sun.setFromSphericalCoords(1, THREE.MathUtils.degToRad(0), 0);
    const uniforms = this.#sky.material.uniforms;
    uniforms.sunPosition.value.copy(this.#sun);
  }

  setDarkTheme() {
    this.#sun.setFromSphericalCoords(1, THREE.MathUtils.degToRad(-5), 0);
    const uniforms = this.#sky.material.uniforms;
    uniforms.sunPosition.value.copy(this.#sun);
  }

  get sky() {
    return this.#sky;
  }
}
