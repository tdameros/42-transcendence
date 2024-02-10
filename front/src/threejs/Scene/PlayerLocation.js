import {Scene} from './Scene';

export class PlayerLocation {
  #looser;
  #matchKey;
  #playerIndex;

  constructor(playerLocationJson) {
    this.#looser = playerLocationJson['looser'];
    this.#matchKey = Scene.convertMatchLocationToKey(playerLocationJson['match_location']);
    this.#playerIndex = playerLocationJson['player_index'];
  }

  getPlayerFromScene(scene) {
    if (this.#looser) {
      return scene.loosers[this.#playerIndex];
    }
    return scene.getMatchFromKey(this.#matchKey).players[this.#playerIndex];
  }
}
