export class PlayerLocation {
  #isInAMatch;
  #matchIndex;
  #playerIndex;

  constructor(playerLocationJson) {
    this.#isInAMatch = playerLocationJson['is_in_a_match'];
    this.#matchIndex = playerLocationJson['match_index'];
    this.#playerIndex = playerLocationJson['player_index'];
  }

  getPlayerFromScene(scene) {
    return scene.matches[this.#matchIndex].players[this.#playerIndex];
  }
}
