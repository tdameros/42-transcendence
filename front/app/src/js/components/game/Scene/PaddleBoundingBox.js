export class PaddleBoundingBox {
  #y_min;
  #y_max;

  constructor(player1Json) {
    const boardSize = player1Json['board']['size'];
    const paddleSize = player1Json['paddle']['size'];
    this.#y_max = boardSize['y'] * 0.5 - paddleSize['y'] * 0.5;
    this.#y_min = -this.#y_max;
  }

  get y_min() {
    return this.#y_min;
  }

  get y_max() {
    return this.#y_max;
  }
}
