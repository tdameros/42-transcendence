import * as THREE from "three";
import {Ball} from "./Ball";
import {Player} from "./Player";
import {jsonToVector3} from "./Engine/jsonToVector3";

export class Scene {
    #threeJSScene;
    #boards = [];
    #balls = [];
    #players = [];
    #players_speed;
    #current_player_index;

    constructor(boards, balls, players, players_speed, current_player_index) {
        this.#threeJSScene = new THREE.Scene();
        this.#players_speed = players_speed;
        this.#current_player_index = current_player_index;

        this.#loadBoards(boards);
        this.#loadBalls(balls);
        this.#loadPlayers(players);
    }

    #loadBoards(boards) {
        for (let jsonBoard of boards) {
            const position = jsonToVector3(jsonBoard["position"]);
            let board = this.#addBoard(position);
            this.#boards.push(board);
        }
    }

    #addBoard(position) {
        let board = new THREE.Mesh(new THREE.PlaneGeometry(40, 27.5),
                                   new THREE.MeshStandardMaterial({color: 0x222277}));
        board.position.set(position.x, position.y, position.z);
        board.castShadow = false;
        board.receiveShadow = true;
        this.#threeJSScene.add(board);
        return board;
    }

    #loadBalls(balls) {
        for (let jsonBall of balls) {
            const position = jsonToVector3(jsonBall["position"]);
            let ball = this.#addBall(position);
            let light = this.#addBallLight(position);

            this.#balls.push(new Ball(ball, light, jsonBall["move_direction"]));
        }
    }

    #addBall(position) {
        let ball = new THREE.Mesh(new THREE.SphereGeometry(1., 10, 10),
                                  new THREE.MeshStandardMaterial({color: 0xFFFFFF,
                                                                  emissive: 0xFFFFFF}));
        ball.position.set(position.x, position.y, position.z);
        ball.castShadow = false;
        ball.receiveShadow = false;
        this.#threeJSScene.add(ball);
        return ball;
    }

    #addBallLight(position) {
        let light = new THREE.PointLight(0xFFFFFF, 500.0, 25);
        light.position.set(position.x, position.y, position.z);
        light.castShadow = true;
        this.#threeJSScene.add(light);
        return light;
    }

    #loadPlayers(players) {
        let i = 0;
        for (let jsonPlayer of players) {
            const playerObject = this.#createPlayer(jsonPlayer, i);

            this.#threeJSScene.add(playerObject);
            this.#players.push(new Player(playerObject,
                                          jsonPlayer["move_direction"]));
            i++;
        }
    }

    #createPlayer(jsonPlayer, i) {
        const group = new THREE.Group();

        const color = i % 2 === 0 ? new THREE.Color(0x00ff00) : new THREE.Color(0xff0000);
        const player = this.#createPlayerBox(color);
        const light = this.#createPlayerLight(color, i);

        group.add(player)
        group.add(light)

        const position = jsonToVector3(jsonPlayer["position"]);
        group.position.set(position.x, position.y, position.z)

        return group;
    }

    #createPlayerBox(color) {
        let player = new THREE.Mesh(new THREE.BoxGeometry(1, 5, 1),
                                    new THREE.MeshStandardMaterial({color: color,
                                                                    emissive: color}));
        player.position.set(0., 0., 0.);
        player.castShadow = true;
        player.receiveShadow = false;
        return player;
    }

    #createPlayerLight(color, i) {
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
        for (let player of this.#players) {
            player.updatePosition(time_ratio);
        }

        for (let ball of this.#balls) {
            ball.updatePosition(time_ratio);
        }
    }

    updateOtherPlayerMovement(player_index, direction) {
        if (direction === 'up')
            this.#players[player_index].updateDirection(this.#players_speed);
        else if (direction === 'down')
            this.#players[player_index].updateDirection(-this.#players_speed);
        else
            this.#players[player_index].updateDirection(0.);
    }

    updateOtherPlayerPosition(player_index, player_position_json) {
        this.#players[player_index].position = jsonToVector3(player_position_json);
    }

    currentPlayerMovesUp() {
        this.#players[this.#current_player_index].updateDirection(this.#players_speed);
    }

    currentPlayerMovesDown() {
        this.#players[this.#current_player_index].updateDirection(-this.#players_speed);
    }

    currentPlayerStopsMoving() {
        this.#players[this.#current_player_index].updateDirection(0.);
    }

    getCurrentPlayerPositionAsArray() {
        const position = this.#players[this.#current_player_index].position;

        return [position.x, position.y, position.z];
    }

    get threeJSScene() {
        return this.#threeJSScene;
    }
}