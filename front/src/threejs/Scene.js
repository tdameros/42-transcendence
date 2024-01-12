import * as THREE from "three";
import {Ball} from "./Ball";
import {Player} from "./Player";
import {jsonToVector3} from "./Engine/jsonToVector3";

export class Scene {
    constructor(boards, balls, players, players_speed, current_player_index) {
        this._threeJSScene = new THREE.Scene();
        this._boards = [];
        this._balls = [];
        this._players = [];
        this._players_speed = players_speed;
        this._current_player_index = current_player_index;

        this._loadBoards(boards);
        this._loadBalls(balls);
        this._loadPlayers(players);
    }

    _loadBoards(boards) {
        for (let jsonBoard of boards) {
            const position = jsonToVector3(jsonBoard["position"]);
            let board = this._addBoard(position);
            this._boards.push(board);
        }
    }

    _addBoard(position) {
        let board = new THREE.Mesh(new THREE.PlaneGeometry(40, 27.5),
                                   new THREE.MeshStandardMaterial({color: 0x222277}));
        board.position.set(position.x, position.y, position.z);
        board.castShadow = false;
        board.receiveShadow = true;
        this._threeJSScene.add(board);
        return board;
    }

    _loadBalls(balls) {
        for (let jsonBall of balls) {
            const position = jsonToVector3(jsonBall["position"]);
            let ball = this._addBall(position);
            let light = this._addBallLight(position);

            this._balls.push(new Ball(ball, light, jsonBall["move_direction"]));
        }
    }

    _addBall(position) {
        let ball = new THREE.Mesh(new THREE.SphereGeometry(1., 10, 10),
                                  new THREE.MeshStandardMaterial({color: 0xFFFFFF,
                                                                  emissive: 0xFFFFFF}));
        ball.position.set(position.x, position.y, position.z);
        ball.castShadow = false;
        ball.receiveShadow = false;
        this._threeJSScene.add(ball);
        return ball;
    }

    _addBallLight(position) {
        let light = new THREE.PointLight(0xFFFFFF, 500.0, 25);
        light.position.set(position.x, position.y, position.z);
        light.castShadow = true;
        this._threeJSScene.add(light);
        return light;
    }

    _loadPlayers(players) {
        let i = 0;
        for (let jsonPlayer of players) {
            const playerObject = this._createPlayer(jsonPlayer, i);

            this._threeJSScene.add(playerObject);
            this._players.push(new Player(playerObject,
                                          jsonPlayer["move_direction"]));
            i++;
        }
    }

    _createPlayer(jsonPlayer, i) {
        const group = new THREE.Group();

        const color = i % 2 === 0 ? new THREE.Color(0x00ff00) : new THREE.Color(0xff0000);
        const player = this._createPlayerBox(color);
        const light = this._createPlayerLight(color, i);

        group.add(player)
        group.add(light)

        const position = jsonToVector3(jsonPlayer["position"]);
        group.position.set(position.x, position.y, position.z)

        return group;
    }

    _createPlayerBox(color) {
        let player = new THREE.Mesh(new THREE.BoxGeometry(1, 5, 1),
                                    new THREE.MeshStandardMaterial({color: color,
                                                                    emissive: color}));
        player.position.set(0., 0., 0.);
        player.castShadow = true;
        player.receiveShadow = false;
        return player;
    }

    _createPlayerLight(color, i) {
        let light = new THREE.RectAreaLight(color, 100, 1, 5);

        const stupidHighNumber = 999999999999999.;
        if (i % 2 === 0) {
            light.position.set(0.5, 0., 0.);
            light.lookAt(stupidHighNumber, 0., 0.);
        } else {
            light.position.set(-0.5, 0., 0.);
            light.lookAt(-stupidHighNumber, 0., 0.);
        }
        return light;
    }

    updateObjectsPositions(time_ratio) {
        for (let player of this._players) {
            player.updatePosition(time_ratio);
        }

        for (let ball of this._balls) {
            ball.updatePosition(time_ratio);
        }
    }

    updateOtherPlayerMovement(player_index, direction) {
        if (direction === 'up')
            this._players[player_index].updateDirection(this._players_speed);
        else if (direction === 'down')
            this._players[player_index].updateDirection(-this._players_speed);
        else
            this._players[player_index].updateDirection(0.);
    }

    updateOtherPlayerPosition(player_index, player_position_json) {
        this._players[player_index].setPosition(player_position_json)
    }

    currentPlayerMovesUp() {
        this._players[this._current_player_index].updateDirection(this._players_speed);
    }

    currentPlayerMovesDown() {
        this._players[this._current_player_index].updateDirection(-this._players_speed);
    }

    currentPlayerStopsMoving() {
        this._players[this._current_player_index].updateDirection(0.);
    }

    getCurrentPlayerPositionAsArray() {
        const position = this._players[this._current_player_index].getPosition();

        return [position.x, position.y, position.z];
    }

    getThreeJSScene() {
        return this._threeJSScene;
    }
}