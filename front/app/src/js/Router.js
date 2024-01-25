export class Router {
  #routes;
  #app;

  constructor(app, routes= [] ) {
    this.#routes = [];
    Object.assign(this.#routes, routes);
    this.#app = app;
    window.addEventListener('popstate', (event) => {
      this.#loadRoute(document.location.pathname);
    });
    this.#loadRoute(document.location.pathname);
  }

  addRoute(path, customElement) {
    this.#routes.push(new Route(path, customElement));
  }

  navigate(newPath) {
    const result = this.#loadRoute(newPath);
    if (result !== null && window.location.pathname !== newPath) {
      window.history.pushState({}, '', newPath);
    }
    return result;
  }

  #findMatchingRoute(path) {
    let defaultRoute = null;
    for (const route of this.#routes) {
      const parametersValues = path.match(route.pathRegex);
      if (parametersValues) {
        parametersValues.shift();
        return {route, parametersValues};
      }
      if (defaultRoute === null && route.path.length === 0) {
        defaultRoute = route;
      }
    }
    return {route: defaultRoute, parametersValues: []};
  }

  #loadRoute(path) {
    const {route, parametersValues} = this.#findMatchingRoute(path);
    if (route === null) {
      console.error(`Route not found`);
      return null;
    }
    const customElement = document.createElement(route.customElement);
    Router.#setParametersInElement(customElement, route.pathParameters,
        parametersValues);
    this.#app.innerHTML = '';
    this.#app.appendChild(customElement);
    return customElement;
  }

  static #setParametersInElement(element, parameters, values) {
    for (let i = 0; i < parameters.length; i++) {
      element.setAttribute(parameters[i], values[i]);
    }
    return element;
  }
}

export class Route {
  constructor(path, customElement) {
    this.path = path;
    this.customElement = customElement;
    this.#setPathParameters();
    this.#setPathRegex();
  }

  #setPathParameters() {
    const matchParameters = this.path.match(/:[a-zA-Z]+/g);
    if (matchParameters === null) {
      this.pathParameters = [];
    } else {
      this.pathParameters = matchParameters.map((param) => param.slice(1));
    }
  }

  #setPathRegex() {
    const parsedPath = this.path.replace(/:[a-zA-Z]+/g, '([a-zA-Z0-9-]+)');
    this.pathRegex = new RegExp(`^${parsedPath}$`);
  }
}

export default {Router, Route};
