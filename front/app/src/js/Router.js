export class Router {
  #routes;
  #app;
  #appendSlash;

  constructor(app, routes = [], appendSlash=true) {
    if (Router.instance) {
      return Router.instance;
    }
    Router.instance = this;
    this.#routes = [];
    this.#appendSlash = appendSlash;
    Object.assign(this.#routes, routes);
    this.#app = app;
    window.addEventListener('popstate', (event) => {
      this.#popstateHandler(event);
    });
  }

  addRoute(path, customElement) {
    this.#routes.push(new Route(path, customElement));
  }

  navigate(newPath) {
    const newPathWithoutQuery = newPath.split('?')[0];
    const {route, parametersValues} = this.#findMatchingRoute(
        newPathWithoutQuery,
    );
    if (route === null) {
      console.error(`Route not found`);
      return null;
    }
    if (window.location.pathname !== newPath) {
      window.history.pushState({}, '', newPath);
    }
    return this.#loadRoute(route, parametersValues);
  }

  init() {
    const URI = this.#getURIWithSlash(document.location.pathname);
    const {route, parametersValues} = this.#findMatchingRoute(URI);
    if (route === null) {
      console.error(`Route not found`);
      return null;
    }
    window.history.replaceState({}, '', URI + window.location.search);
    return this.#loadRoute(route, parametersValues);
  }

  redirect(newPath) {
    const newPathWithoutQuery = newPath.split('?')[0];
    window.history.replaceState({}, '', newPath);
    const {route, parametersValues} = this.#findMatchingRoute(
        newPathWithoutQuery,
    );
    if (route === null) {
      console.error(`Route not found`);
      return null;
    }
    return this.#loadRoute(route, parametersValues);
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

  #loadRoute(route, parametersValues) {
    const customElement = document.createElement(route.customElement);
    Router.#setParametersInElement(customElement, route.pathParameters,
        parametersValues);
    this.#app.innerHTML = '';
    this.#app.appendChild(customElement);
    return customElement;
  }

  #popstateHandler(event) {
    const {route, parametersValues} = this.#findMatchingRoute(
        document.location.pathname,
    );
    if (route === null) {
      console.error(`Route not found`);
      return null;
    }
    this.#loadRoute(route, parametersValues);
  }

  #getURIWithSlash(URI) {
    if (this.#appendSlash && !URI.endsWith('/')) {
      return URI + '/';
    }
    return URI;
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

export function getRouter() {
  return Router.instance;
}
