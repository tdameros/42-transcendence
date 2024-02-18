import * as THREE from 'three';

import {Match} from './Match';
import {PlayerLocation} from './PlayerLocation';
import {Player} from './Player/Player';
import {BallBoundingBox, PaddleBoundingBox} from './boundingBoxes';

export class Scene {
  #engine;
  #threeJSScene = new THREE.Scene();
  #matches = [];
  #matches_map = {};
  #currentPlayerLocation;
  #loosers = [];
  #ballBoundingBox;
  #paddleBoundingBox;
  #isLooserCamera = false;
  #matchesMiddleX;
  #matchesMiddleY;
  #matchHalfWidth;
  #matchHalfHeight;
  #matchesXOffset;
  #matchesYOffset;

  constructor(engine, sceneJson, playerLocationJson) {
    this.#engine = engine;

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

    const light = new THREE.AmbientLight(0xffffff, 0.2);
    this.#threeJSScene.add(light);

    this.#currentPlayerLocation = new PlayerLocation(playerLocationJson);

    const playerJson = matchesJson[0]['players'][0];
    this.#ballBoundingBox = new BallBoundingBox(
        playerJson, matchesJson[0]['ball']['radius'],
    );
    this.#paddleBoundingBox = new PaddleBoundingBox(playerJson);

    this.#matchesMiddleX = sceneJson['matches_middle']['x'];
    this.#matchesMiddleY = sceneJson['matches_middle']['y'];
    this.#matchHalfWidth = sceneJson['match_half_width'];
    this.#matchHalfHeight = sceneJson['match_half_height'];
    this.#matchesXOffset = sceneJson['matches_x_offset'];
    this.#matchesYOffset = sceneJson['matches_y_offset'];
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

  updateCamera() {
    if (this.#isLooserCamera) {
      return;
    }

    const currentPlayerMatch = this.#currentPlayerLocation.
        getPlayerMatchFromScene(this);

    if (currentPlayerMatch === null) {
      this.#setSpectatorCameraSettings();
    } else {
      this.#setMatchCameraSettings(currentPlayerMatch);
    }
  }

  #setSpectatorCameraSettings() {
    console.log('setSpectatorCameraSettings'); // TODO delete me
    const xHeight = this.#matchesMiddleX /
      Math.tan(this.#engine.threeJS.getCameraHorizontalFOVRadian() * .5);
    const yHeight = this.#matchesMiddleY /
      Math.tan(this.#engine.threeJS.getCameraVerticalFOVRadian() * .5);
    const cameraHeight = Math.max(xHeight, yHeight);

    const cameraPosition = new THREE.Vector3(
        this.#matchesMiddleX, this.#matchesMiddleY, cameraHeight,
    );

    const cameraLookAt = new THREE.Vector3(this.#matchesMiddleX,
        this.#matchesMiddleY, 0);

    this.#engine.updateCamera(cameraPosition, cameraLookAt);
  }

  #setMatchCameraSettings(match) {
    const currentPlayerGamePosition = match.threeJSGroup.position;
    const xHeight = (this.#matchHalfWidth + this.#matchesXOffset * .5) /
      Math.tan(this.#engine.threeJS.getCameraHorizontalFOVRadian() * .5);
    // Using matchesXOffset again to keep the same offset
    const yHeight = (this.#matchHalfHeight + this.#matchesXOffset * .5) /
      Math.tan(this.#engine.threeJS.getCameraVerticalFOVRadian() * .5);
    const cameraHeight = Math.max(xHeight, yHeight);

    const cameraPosition = new THREE.Vector3(
        currentPlayerGamePosition.x, currentPlayerGamePosition.y, cameraHeight,
    );
    const cameraLookAt = currentPlayerGamePosition.clone();
    this.#engine.updateCamera(cameraPosition, cameraLookAt);
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
