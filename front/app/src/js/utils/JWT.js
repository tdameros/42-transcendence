export class JWT {
  #jwt;
  #payload;
  #header;
  #signature;
  #isValidSyntax;

  constructor(jwt) {
    this.#jwt = jwt;
    this.#payload = null;
    this.#header = null;
    this.#signature = null;
    this.#isValidSyntax = null;
    this.#decode();
  }

  getTimeRemainingInSeconds() {
    if (!this.payload.hasOwnProperty('exp')) {
      return Infinity;
    }
    const now = Math.floor(Date.now() / 1000);
    return this.payload.exp - now;
  }

  isValid(requiredRemainingTimeInSeconds = 60) {
    return this.#isValidSyntax &&
      this.getTimeRemainingInSeconds() > requiredRemainingTimeInSeconds;
  }

  get jwt() {
    return this.#jwt;
  }

  #decode() {
    if (!this.#jwt) {
      this.#isValidSyntax = false;
      return;
    }
    const [header, payload, signature] = this.#jwt.split('.');
    if (!header || !payload || !signature) {
      this.#isValidSyntax = false;
      return;
    }
    try {
      this.payload = JWT.base64ToJSON(payload);
      this.header = JWT.base64ToJSON(header);
    } catch (error) {
      this.#isValidSyntax = false;
    }
    this.signature = signature;
    this.#isValidSyntax = true;
  }

  static base64ToJSON(base64) {
    return JSON.parse(atob(base64));
  }
}
