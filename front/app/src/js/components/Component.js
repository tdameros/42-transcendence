export class Component extends HTMLElement {
  #componentEventListeners;
  #rendered;

  constructor() {
    super();
    this.#rendered = false;
    this.#componentEventListeners = [];
  }

  connectedCallback() {
    if (!this.#rendered) {
      const render = this.render();
      if (render === false) {
        return;
      }
      this.innerHTML = render + this.style();
      this.#rendered = true;
      this.postRender();
    }
  }

  disconnectedCallback() {
    this.removeAllComponentEventListeners();
  }

  attributeChangedCallback(name, oldValue, newValue) {
    this.update();
  }

  addComponentEventListener(element, event, callback) {
    if (!element) {
      return;
    }
    if (!this.#componentEventListeners[event]) {
      this.#componentEventListeners[event] = [];
    }
    const eventCallback = callback.bind(this);
    this.#componentEventListeners[event].push({element, eventCallback});
    element.addEventListener(event, eventCallback);
  }

  removeComponentEventListener(element, event) {
    const eventListeners = this.#componentEventListeners[event];

    if (eventListeners) {
      for (const eventListener of eventListeners) {
        if (eventListener.element === element) {
          element.removeEventListener(event, eventListener.eventCallback);
          eventListeners.splice(eventListeners.indexOf(eventListener), 1);
        }
      }
    }
  }

  removeAllComponentEventListeners() {
    for (const event in this.#componentEventListeners) {
      if (this.#componentEventListeners.hasOwnProperty(event)) {
        const eventListeners = this.#componentEventListeners[event];
        for (const eventListener of eventListeners) {
          eventListener.element.removeEventListener(event,
              eventListener.eventCallback);
        }
      }
    }
    this.#componentEventListeners = [];
  }

  render() {
    return '';
  }

  update() {
    this.innerHTML = this.render() + this.style();
  }

  style() {
    return '<style></style>';
  }

  postRender() {
  }
}
