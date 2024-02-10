import * as THREE from 'three';

export class Segment2 {
  #begin = new THREE.Vector2;
  #end = new THREE.Vector2;

  constructor(begin, end) {
    this.#begin.set(begin.x, begin.y);
    this.#end.set(end.x, end.y);
  }

  intersect(segment2) {
    const t1Top = (segment2.end.x - segment2.begin.x) *
            (this.#begin.y - segment2.begin.y) -
            (segment2.end.y - segment2.begin.y) *
                (this.#begin.x - segment2.begin.x);
    const t2Top = (segment2.begin.y - this.#begin.y) *
            (this.#begin.x - this.#end.x) -
            (segment2.begin.x - this.#begin.x) *
                (this.#begin.y - this.#end.y);
    const bottom = (segment2.end.y - segment2.begin.y) *
            (this.#end.x - this.#begin.x) -
            (segment2.end.x - segment2.begin.x) *
                (this.#end.y - this.#begin.y);

    if (bottom === 0) {
      return {point: null, t: null};
    }

    const t1 = t1Top / bottom;
    if (t1 < 0 || t1 > 1) {
      return {point: null, t: null};
    }

    const t2 = t2Top / bottom;
    if (t2 < 0 || t2 > 1) {
      return {point: null, t: null};
    }

    return {
      point: new THREE.Vector2(this.#begin.x + t1 *
          (this.#end.x - this.#begin.x),
      this.#begin.y + t1 * (this.#end.y - this.#begin.y)),
      t: t1,
    };
  }

  get begin() {
    return this.#begin;
  }

  get end() {
    return this.#end;
  }
}
