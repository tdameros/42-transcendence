import * as THREE from 'three';
import TWEEN from '@tweenjs/tween.js';


import {Match} from './Match';
import {PlayerLocation} from './PlayerLocation';
import {Player} from './Player/Player';
import {jsonToVector3} from '@components/game/jsonToVector3.js';
import {PaddleBoundingBox} from './PaddleBoundingBox.js';
import {SceneSky} from './SceneSky.js';

export class Scene {
  #engine;
  #threeJSScene = new THREE.Scene();
  #matches = [];
  #matches_map = {};
  #currentPlayerLocation;
  #loosers = [];
  #paddleBoundingBox;
  #isLooserCamera = false;
  #matchesMiddleX;
  #matchesMiddleY;
  #matchHalfWidth;
  #matchHalfHeight;
  #matchesXOffset;
  #matchesYOffset;
  #sky;
  #pointsToWinMatch;
  #boardSize;

  constructor() {}

  async init(engine, sceneJson, playerLocationJson) {
    this.#engine = engine;

    this.#pointsToWinMatch = sceneJson['points_to_win_match'];
    const matchesJson = sceneJson['matches'];
    for (const matchJson of matchesJson) {
      const newMatch = new Match();
      await newMatch.init(matchJson, true, this.#pointsToWinMatch);
      this.#matches.push(newMatch);
      this.#addMatchToMatchMap(newMatch, matchJson['location']);
      this.#threeJSScene.add(newMatch.threeJSGroup);
    }

    const loosersJson = sceneJson['loosers'];
    for (const looserJson of loosersJson) {
      const newLooser = new Player();
      await newLooser.init(looserJson);
      this.#loosers.push(newLooser);
      this.#threeJSScene.add(newLooser.threeJSGroup);
    }

    this.#sky = new SceneSky();
    this.#threeJSScene.add(this.#sky.sky);
    const light = new THREE.AmbientLight(0xffffff, 0.2);
    this.#threeJSScene.add(light);

    this.#currentPlayerLocation = new PlayerLocation(playerLocationJson);

    const playerJson = matchesJson[0]['players'][0];
    this.#paddleBoundingBox = new PaddleBoundingBox(playerJson);
    this.#boardSize = jsonToVector3(playerJson['board']['size']);

    this.#matchesMiddleX = sceneJson['matches_middle']['x'];
    this.#matchesMiddleY = sceneJson['matches_middle']['y'];
    this.#matchHalfWidth = sceneJson['match_half_width'];
    this.#matchHalfHeight = sceneJson['match_half_height'];
    this.#matchesXOffset = sceneJson['matches_x_offset'];
    this.#matchesYOffset = sceneJson['matches_y_offset'];
    this.#engine.threeJS.controls.target.set(30, 25, 0);
  }

  setLightTheme() {
    this.#sky.setLightTheme();
  }

  setDarkTheme() {
    this.#sky.setDarkTheme();
  }

  updateFrame(timeDelta) {
    const currentTime = Date.now();
    for (const match of this.#matches) {
      match.updateFrame(
          timeDelta,
          currentTime,
          this.#paddleBoundingBox,
          this.#boardSize,
      );
    }

    for (const looser of this.#loosers) {
      looser.updateFrame(timeDelta, this.#paddleBoundingBox);
    }
  }

  removeLooserFromMatch(matchLocationJson, looserIndex) {
    const match = this.getMatchFromLocation(matchLocationJson);
    const looser = match.players[looserIndex];
    if (this.#currentPlayerLocation.getPlayerFromScene(this) === looser) {
      this.#currentPlayerLocation = new PlayerLocation({
        'is_looser': true,
        'match_location': {'game_round': -1, 'match': -1},
        'player_index': this.#loosers.length,
      });
      this.#engine.component.loadEndGameCard('eliminated', 0, 0);
    }
    match.removePlayer(looserIndex);

    looser.getPosition().add(match.getPosition());
    this.#threeJSScene.add(looser.threeJSGroup);
    this.#loosers.push(looser);
  }

  addWinnerToMatch(matchLocationJson, winner, winnerIndex, newWinnerIndex) {
    if (this.#currentPlayerLocation.getPlayerFromScene(this) === winner) {
      this.#currentPlayerLocation = new PlayerLocation({
        'is_looser': false,
        'match_location': matchLocationJson,
        'player_index': newWinnerIndex,
      });
    }

    if (winnerIndex !== newWinnerIndex) {
      winner.changeSide();
    }
    const match = this.getMatchFromLocation(matchLocationJson);
    match.addPlayer(winner, newWinnerIndex);
  }

  removeBallFromMatch(matchLocationJson) {
    const match = this.getMatchFromLocation(matchLocationJson);
    match.ball.removeBall();
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
    const yHeight = (this.#matchHalfHeight + this.#matchesXOffset * .5) /
      Math.tan(this.#engine.threeJS.getCameraVerticalFOVRadian() * .5);
    const cameraHeight = Math.max(xHeight, yHeight);

    const cameraPosition = new THREE.Vector3(
        currentPlayerGamePosition.x,
        currentPlayerGamePosition.y,
        cameraHeight - 10,
    );
    const cameraLookAt = currentPlayerGamePosition.clone();
    this.#engine.updateCamera(cameraPosition, cameraLookAt);

    const newCameraPosition = new THREE.Vector3(
        currentPlayerGamePosition.x, currentPlayerGamePosition.y, cameraHeight,
    );

    new TWEEN.Tween(cameraPosition)
        .to(newCameraPosition, 3000)
        .easing(TWEEN.Easing.Quadratic.InOut)
        .onUpdate(() => {
          this.#engine.updateCamera(cameraPosition, cameraLookAt);
        })
        .start();
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
    return this.getMatchFromKey(Scene.convertMatchLocationToKey(locationJson));
  }

  deleteMatch(locationJson) {
    const key = Scene.convertMatchLocationToKey(locationJson);
    const match = this.getMatchFromKey(key);

    this.#matches.splice(this.#matches.indexOf(match), 1);
    delete this.#matches_map[key];

    this.#threeJSScene.remove(match.threeJSGroup);
  }

  async createMatchIfDoesntExist(matchJson) {
    const key = Scene.convertMatchLocationToKey(matchJson['location']);
    let match = this.getMatchFromKey(key);
    if (match !== undefined) {
      return;
    }

    match = new Match();
    await match.init(matchJson, false, this.#pointsToWinMatch);
    this.#matches.push(match);
    this.#matches_map[key] = match;
    this.#threeJSScene.add(match.threeJSGroup);
  }

  get matches() {
    return this.#matches;
  }

  get currentPlayerLocation() {
    return this.#currentPlayerLocation;
  }

  get threeJSScene() {
    return this.#threeJSScene;
  }

  get loosers() {
    return this.#loosers;
  }

  get boardSize() {
    return this.#boardSize;
  }
}
