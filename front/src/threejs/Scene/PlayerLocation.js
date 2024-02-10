import {Scene} from './Scene';

export class PlayerLocation {
  #isLooser;
  #matchKey;
  #playerIndex;

  constructor(playerLocationJson) {
    this.#isLooser = playerLocationJson['is_looser'];
    this.#matchKey = Scene.convertMatchLocationToKey(playerLocationJson['match_location']);
    this.#playerIndex = playerLocationJson['player_index'];
  }

  getPlayerFromScene(scene) {
    if (this.#isLooser === true) {
      return scene.loosers[this.#playerIndex];
    }
    return scene.getMatchFromKey(this.#matchKey).players[this.#playerIndex];
  }
}
