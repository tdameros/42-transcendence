export class ServerTimeFixer {
  static #timeOffsetSum = 0.;
  static #divider = 0.;
  static #timeOffsetsSize = 20;
  static #timeOffsets = Array(ServerTimeFixer.#timeOffsetsSize).fill(0.);
  static #timeOffsetsIndex = 0;
  static #averageTimeOffset = 0.;

  static updateServerLatency(serverCurrentTime) {
    const currentTimeOffset = Date.now() -
        ServerTimeFixer.#convertTime(serverCurrentTime);

    this.#timeOffsetSum += currentTimeOffset;
    this.#timeOffsetSum -= this.#timeOffsets[this.#timeOffsetsIndex];
    this.#timeOffsets[this.#timeOffsetsIndex] = currentTimeOffset;
    this.#timeOffsetsIndex = (this.#timeOffsetsIndex + 1) %
        this.#timeOffsetsSize;

    this.#divider = Math.min(this.#divider + 1, this.#timeOffsetsSize);
    this.#averageTimeOffset = this.#timeOffsetSum / this.#divider;
  }

  static fixServerTime(serverTime) {
    return this.#convertTime(serverTime) + this.#averageTimeOffset;
  }

  static #convertTime(serverTime) {
    return serverTime * 1000.;
  }
}
