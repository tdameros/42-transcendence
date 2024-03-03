import {Scene} from './Scene';

export class PlayerLocation {
  #isLooser;
  #matchKey;
  #playerIndex;

  constructor(playerLocationJson) {
    this.#isLooser = playerLocationJson['is_looser'];
    this.#matchKey = Scene.convertMatchLocationToKey(
        playerLocationJson['match_location'],
    );
    this.#playerIndex = playerLocationJson['player_index'];
  }

  getPlayerMatchFromScene(scene) {
    if (this.#isLooser === true) {
      return null;
    }
    return scene.getMatchFromKey(this.#matchKey);
  }

  getPlayerFromScene(scene) {
    if (this.#isLooser === true) {
      return scene.loosers[this.#playerIndex];
    }
    return this.getPlayerMatchFromScene(scene).players[this.#playerIndex];
  }

  get playerIndex() {
    return this.#playerIndex;
  }

  get isLooser() {
    return this.#isLooser;
  }
}
