export class ServerTime {
  static #isTimeSynced = false;

  // Used to account for when the client and server do not have the same
  // system date
  static #timeOffsetSum = 0.;
  static #offsetDivider = 0.;
  static #timeOffsetsSize = 20;
  static #timeOffsets = Array(ServerTime.#timeOffsetsSize).fill(0.);
  static #timeOffsetsIndex = 0;
  static #averageTimeOffset = 0.;

  // Used to account for latency
  static #latencySum = 0.;
  static #latencyDivider = 0.;
  static #latenciesSize = 20;
  static #latencies = Array(ServerTime.#latenciesSize).fill(0.);
  static #latenciesIndex = 0;
  static #averageLatency = 0.;

  static syncServerTime(timeData) {
    const clientCurrentTime = Number(Date.now());
    const clientTimeAtRequestEmit = Number(timeData['time1']);
    const serverTimeAtRequestReceive = this.#secondsToMs(timeData['time2']);

    const latency = (clientCurrentTime - clientTimeAtRequestEmit) / 2.;
    const timeOffset = clientCurrentTime - serverTimeAtRequestReceive - latency;

    this.#updateLatency(latency);
    this.#updateTimeOffset(timeOffset);

    this.#isTimeSynced = true;
  }

  static fixServerTime(serverTime) {
    return this.#secondsToMs(serverTime) + this.#averageTimeOffset;
  }

  static get latency() {
    return this.#averageLatency;
  }

  static get isTimeSynced() {
    return this.#isTimeSynced;
  }

  static #secondsToMs(serverTime) {
    return serverTime * 1000.;
  }

  static #updateLatency(latency) {
    this.#latencySum += latency;
    this.#latencySum -= this.#latencies[this.#latenciesIndex];
    this.#latencies[this.#latenciesIndex] = latency;
    this.#latenciesIndex = (this.#latenciesIndex + 1) %
      this.#timeOffsetsSize;

    this.#latencyDivider = Math.min(
        this.#latencyDivider + 1, this.#latenciesSize);
    this.#averageLatency = this.#latencySum / this.#latencyDivider;
  }

  static #updateTimeOffset(timeOffset) {
    this.#timeOffsetSum += timeOffset;
    this.#timeOffsetSum -= this.#timeOffsets[this.#timeOffsetsIndex];
    this.#timeOffsets[this.#timeOffsetsIndex] = timeOffset;
    this.#timeOffsetsIndex = (this.#timeOffsetsIndex + 1) %
      this.#timeOffsetsSize;

    this.#offsetDivider = Math.min(
        this.#offsetDivider + 1, this.#timeOffsetsSize);
    this.#averageTimeOffset = this.#timeOffsetSum / this.#offsetDivider;
  }
}
