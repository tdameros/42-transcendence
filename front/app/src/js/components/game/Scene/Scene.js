import * as THREE from 'three';
import TWEEN from '@tweenjs/tween.js';


import {Match} from './Match';
import {PlayerLocation} from './PlayerLocation';
import {Player} from './Player/Player';
import {BallBoundingBox, PaddleBoundingBox} from './boundingBoxes';
import {Sky} from 'three/addons/objects/Sky.js';
import {Theme} from '@js/Theme.js';

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
  #sky;
  #sun;

  constructor() {}

  async init(engine, sceneJson, playerLocationJson) {
    this.#engine = engine;

    const matchesJson = sceneJson['matches'];
    for (const matchJson of matchesJson) {
      const newMatch = new Match();
      await newMatch.init(matchJson, true);
      this.#matches.push(newMatch);
      this.#addMatchToMatchMap(newMatch, matchJson['location']);
      this.#threeJSScene.add(newMatch.threeJSGroup);
    }

    const loosersJson = sceneJson['loosers'];
    for (const looserJson of loosersJson) {
      const newLooser = new Player();
      await newLooser.init(loosersJson);
      this.#loosers.push(newLooser);
      this.#threeJSScene.add(newLooser.threeJSGroup);
    }

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
    
    
    // TODO rename me
    let junk = new THREE.Vector3(0, 1, 0);
    const axis = new THREE.Vector3(1, 0, 0);
    const angle = Math.PI / 2;

    junk.applyAxisAngle( axis, angle );



    this.#sky.material.uniforms.up.value.set( junk.x, junk.y, junk.z);
    //this.#sky.rotation.set(Math.PI / 2, 0, 0);
    this.#threeJSScene.add(this.#sky);
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

  setLightTheme() {
    this.#sun.setFromSphericalCoords(1, THREE.MathUtils.degToRad(0), 0);
    const uniforms = this.#sky.material.uniforms;
    uniforms.sunPosition.value.copy(this.#sun);
  }

  setDarkTheme() {
    this.#sun.setFromSphericalCoords(1, THREE.MathUtils.degToRad(-2), 0);
    const uniforms = this.#sky.material.uniforms;
    uniforms.sunPosition.value.copy(this.#sun);
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
    const looser = match.players[looserIndex];
    if (this.#currentPlayerLocation.getPlayerFromScene(this) === looser) {
      this.#currentPlayerLocation = new PlayerLocation({
        'is_looser': true,
        'match_location': {'game_round': -1, 'match': -1},
        'player_index': this.#loosers.length,
      });
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
        // currentPlayerGamePosition.x, cameraHeight, currentPlayerGamePosition.z,
        currentPlayerGamePosition.x, currentPlayerGamePosition.y, cameraHeight - 20,
    );
    const cameraLookAt = currentPlayerGamePosition.clone();
    this.#engine.updateCamera(cameraPosition, cameraLookAt);

    // Ancienne position de la caméra
    const oldCameraPosition = cameraPosition;

    // Nouvelle position de la caméra (zoomée)
    const newCameraPosition = new THREE.Vector3(
        currentPlayerGamePosition.x, currentPlayerGamePosition.y, cameraHeight,
        // currentPlayerGamePosition.x, cameraHeight + 20, currentPlayerGamePosition.z,
    );

    // Créer un tween pour animer la position de la caméra
    new TWEEN.Tween(oldCameraPosition)
        .to(newCameraPosition, 3000) // Durée de l'animation (en millisecondes)
        .easing(TWEEN.Easing.Quadratic.InOut) // Type d'interpolation pour une transition fluide
        .onUpdate(() => {
            // Mise à jour de la position de la caméra à chaque étape de l'animation
            this.#engine.updateCamera(oldCameraPosition, cameraLookAt);
        })
        .start(); // Démarrer l'animation
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

  createMatchIfDoesntExist(matchJson) {
    const key = Scene.convertMatchLocationToKey(matchJson['location']);
    let match = this.getMatchFromKey(key);
    if (match !== undefined) {
      return;
    }

    match = new Match();
    match.init(matchJson, false);
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
