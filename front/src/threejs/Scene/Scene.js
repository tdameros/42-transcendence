import * as THREE from 'three';

import {Match} from './Match';
import {PlayerLocation} from './PlayerLocation';

export class Scene {
  #threeJSScene = new THREE.Scene();
  #matches = [];
  #currentPlayerLocation;

  constructor(matchesJson, playerLocationJson) {
    for (const matchJson of matchesJson) {
      const newMatch = new Match(matchJson);
      this.#matches.push(newMatch);
      this.#threeJSScene.add(newMatch.threeJSGroup);
    }

    this.#currentPlayerLocation = new PlayerLocation(playerLocationJson);
  }

  updateFrame(timeDelta) {
    const currentTime = Date.now();
    for (const match of this.#matches) {
      match.updateFrame(timeDelta, currentTime);
    }
  }

  setPlayerPaddleDirection(playerLocationJson, direction) {
    new PlayerLocation(playerLocationJson).getPlayerFromScene(this)
        .setPaddleDirection(direction);
  }

  setPlayerPaddlePosition(playerLocationJson, positionJson) {
    new PlayerLocation(playerLocationJson).getPlayerFromScene(this)
        .setPaddlePosition(positionJson);
  }

  getCurrentPlayerPaddlePositionAsArray() {
    const position = this.#currentPlayerLocation.getPlayerFromScene(this)
        .getPaddlePosition();
    return [position.x, position.y, position.z];
  }

  setCurrentPlayerPaddleDirection(direction) {
    this.#currentPlayerLocation.getPlayerFromScene(this)
        .setPaddleDirection(direction);
  }

  get matches() {
    return this.#matches;
  }

  get threeJSScene() {
    return this.#threeJSScene;
  }
}
