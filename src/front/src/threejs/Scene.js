import * as THREE from "three";
import {Ball} from "./Ball";
import {Player} from "./Player";
import {RectAreaLightHelper} from "three/addons";

export class Scene {
    constructor(jsonScene) {
        this._threeJSScene = new THREE.Scene();
        this._boards = [];
        this._balls = [];
        this._players = [];

        const light = new THREE.AmbientLight(0xffffff, 0);
        this._threeJSScene.add(light);

        this._loadBoards(jsonScene["boards"]);
        this._loadBalls(jsonScene["balls"]);
        this._loadPlayers(jsonScene["players"]);
    }

    _loadBoards(boards) {
        for (let jsonBoard of boards) {
            const position = Scene.jsonToVector3(jsonBoard["position"]);
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
            const position = Scene.jsonToVector3(jsonBall["position"]);
            let ball = this._addBall(position);
            let light = this._addBallLight(position);

            this._balls.push(new Ball(ball, light, jsonBall["move_direction"]));
        }
    }

    _addBall(position) {
        let ball = new THREE.Mesh(new THREE.SphereGeometry(1., 10, 10),
            new THREE.MeshStandardMaterial({color: 0xFFFFFF, emissive: 0xFFFFFF}));
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
            const position = Scene.jsonToVector3(jsonPlayer["position"]);
            const color = i % 2 === 0 ? new THREE.Color(0x00ff00) : new THREE.Color(0xff0000);
            const matchBoardPosition = this._boards.at(i / 2).position;
            let player = this._addPlayer(position, color);
            let light = this._addPlayerLight(position, color, i, matchBoardPosition);

            this._players.push(new Player(player, light, jsonPlayer["move_direction"], matchBoardPosition));
            i++;
        }
    }

    _addPlayer(position, color) {
        let player = new THREE.Mesh(new THREE.BoxGeometry(1, 5, 1),
            new THREE.MeshStandardMaterial({color: color, emissive: color}));
        player.position.set(position.x, position.y, position.z);
        player.castShadow = true;
        player.receiveShadow = false;
        this._threeJSScene.add(player);
        return player;
    }

    _addPlayerLight(position, color, i, matchBoardPosition) {
        let light = new THREE.RectAreaLight(color, 100, 1, 5);
        if (i % 2 === 0) {
            light.position.set(position.x + 0.5, position.y, position.z);
        } else {
            light.position.set(position.x - 0.5, position.y, position.z);
        }

        light.lookAt(matchBoardPosition.x,
            matchBoardPosition.y,
            matchBoardPosition.z + position.z);
        this._threeJSScene.add(light);

        return light;
    }

    static jsonToVector3(dictionary) {
        return new THREE.Vector3(dictionary["x"], dictionary["y"], dictionary["z"]);
    }

    updateObjectsPositions(time_ratio) {
        for (let player of this._players) {
            player.updatePosition(time_ratio);
        }

        for (let ball of this._balls) {
            ball.updatePosition(time_ratio);
        }
    }

    updatePlayerMovement(data) {
        this._players[data["player_index"]].updateDirection(data["move_direction"]);
    }

    getThreeJSScene() {
        return this._threeJSScene;
    }
}