export class BallBoundingBox {
    #y_min;
    #y_max;
    #x_min;
    #x_max;

    constructor(player1Json, ballRadius) {
        const board_size = player1Json['board']['size'];
        const halfRadius = ballRadius * 0.5;
        this.#y_max = board_size['y'] * 0.5 - halfRadius;
        this.#y_min = -this.#y_max;
        this.#x_max = board_size['x'] - halfRadius;
        this.#x_min = -this.#x_max;
    }

    get y_min() {
        return this.#y_min;
    }

    get y_max() {
        return this.#y_max;
    }

    get x_min() {
        return this.#x_min;
    }

    get x_max() {
        return this.#x_max;
    }
}

export class PaddleBoundingBox {
    #y_min;
    #y_max;

    constructor(player1Json) {
        const board_size = player1Json['board']['size'];
        const paddle_size = player1Json['paddle']['size'];
        this.#y_max = board_size['y'] * 0.5 - paddle_size['y'] * 0.5;
        this.#y_min = -this.#y_max;
    }

    get y_min() {
        return this.#y_min;
    }

    get y_max() {
        return this.#y_max;
    }
}