import * as THREE from 'three';

import {Match} from './Match';
import {PlayerLocation} from './PlayerLocation';
import {Player} from './Player/Player';
import {BallBoundingBox, PaddleBoundingBox} from './boundingBoxes';

export class Scene {
  #threeJSScene = new THREE.Scene();
  #matches = [];
  #matches_map = {};
  #currentPlayerLocation;
  #loosers = [];
  #ballBoundingBox;
  #paddleBoundingBox;

  constructor(sceneJson, playerLocationJson) {
    const matchesJson = sceneJson['matches'];
    for (const matchJson of matchesJson) {
      const newMatch = new Match(matchJson);
      this.#matches.push(newMatch);
      this.#addMatchToMatchMap(newMatch, matchJson['location']);
      this.#threeJSScene.add(newMatch.threeJSGroup);
    }

    const loosersJson = sceneJson['loosers'];
    for (const looserJson of loosersJson) {
      const newLooser = new Player(looserJson);
      this.#loosers.push(newLooser);
      this.#threeJSScene.add(newLooser.threeJSGroup);
    }

    this.#currentPlayerLocation = new PlayerLocation(playerLocationJson);

    const playerJson = matchesJson[0]['players'][0];
    this.#ballBoundingBox = new BallBoundingBox(
        playerJson, matchesJson[0]['ball']['radius'],
    );
    this.#paddleBoundingBox = new PaddleBoundingBox(playerJson);
  }

  updateFrame(timeDelta) {
    const currentTime = Date.now();
    for (const match of this.#matches) {
      match.updateFrame(
          timeDelta,
          currentTime,
          this.#paddleBoundingBox,
          this.#ballBoundingBox,
      );
    }

    for (const looser of this.#loosers) {
      looser.updateFrame(timeDelta, this.#paddleBoundingBox);
    }
  }

  removeLooserFromMatch(matchLocationJson, looserIndex) {
    const match = this.getMatchFromLocation(matchLocationJson);
    const looser = match.popPlayer(looserIndex);
    if (looser === null) {
      return;
    }

    if (this.#currentPlayerLocation.getPlayerFromScene(this) === looser) {
      this.#currentPlayerLocation = new PlayerLocation({
        'looser': true,
        'match_location': {'game_round': -1, 'match': -1},
        'player_index': this.#loosers.length,
      });
    }

    looser.getPosition().add(match.getPosition());
    this.#threeJSScene.add(looser.threeJSGroup);
    this.#loosers.push(looser);
  }

  addWinnerToMatch(matchLocationJson, winner, winnerIndex) {
    if (this.#currentPlayerLocation.getPlayerFromScene(this) === winner) {
      this.#currentPlayerLocation = new PlayerLocation({
        'looser': true,
        'match_location': matchLocationJson,
        'player_index': winnerIndex,
      });
    }

    const match = this.getMatchFromLocation(matchLocationJson);
    match.addPlayer(winner, winnerIndex);
  }

  getCurrentPlayerPaddlePositionY() {
    return this.#currentPlayerLocation.getPlayerFromScene(this)
        .paddle.getPosition().y;
  }

  setCurrentPlayerPaddleDirection(direction) {
    this.#currentPlayerLocation.getPlayerFromScene(this)
        .paddle.setDirection(direction);
  }

  static convertMatchLocationToKey(matchLocationJson) {
    return matchLocationJson['game_round'] + ';' + matchLocationJson['match'];
  }

  #addMatchToMatchMap(match, locationJson) {
    const key = Scene.convertMatchLocationToKey(locationJson);
    this.#matches_map[key] = match;
  }

  getMatchFromKey(key) {
    return this.#matches_map[key];
  }

  getMatchFromLocation(locationJson) {
    const key = Scene.convertMatchLocationToKey(locationJson);
    return this.getMatchFromKey(key);
  }

  deleteMatch(locationJson) {
    const key = Scene.convertMatchLocationToKey(locationJson);
    const match = this.getMatchFromKey(key);

    this.#matches.splice(this.#matches.indexOf(match), 1);
    delete this.#matches_map[key];

    this.#threeJSScene.remove(match.threeJSGroup);
  }

  createMatchIfDoesntExist(matchJson) {
    const key = Scene.convertMatchLocationToKey(matchJson['location']);
    let match = this.getMatchFromKey(key);
    if (match !== undefined) {
      return;
    }

    match = new Match(matchJson);
    this.#matches.push(match);
    this.#matches_map[key] = match;
    this.#threeJSScene.add(match.threeJSGroup);
  }

  get matches() {
    return this.#matches;
  }

  get threeJSScene() {
    return this.#threeJSScene;
  }

  get loosers() {
    return this.#loosers;
  }
}
