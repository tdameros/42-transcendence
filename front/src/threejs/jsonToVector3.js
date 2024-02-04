import * as THREE from 'three';

export function jsonToVector3(dictionary) {
  return new THREE.Vector3(dictionary['x'],
      dictionary['y'],
      dictionary['z']);
}
