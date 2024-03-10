export class PaddleBoundingBox {
  #y_min;
  #y_max;

  constructor(boardHeight, paddleHeight) {
    this.#y_max = boardHeight * 0.5 - paddleHeight * 0.5;
    this.#y_min = -this.#y_max;
  }

  get y_min() {
    return this.#y_min;
  }

  get y_max() {
    return this.#y_max;
  }
}
