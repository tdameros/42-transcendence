# `Router`

--------------------------------------------------------------------------------

The Router class is a class designed to facilitate client-side routing in web
applications.
It allows to define routes and associated custom elements,
enabling seamless navigation within a single-page application (SPA).

The router automatically manages page history in the browser.

--------------------------------------------------------------------------------

## Instantiation

To use the Router class, instantiate it with the following parameters:

```javascript
const app = document.querySelector('#app'); // Replace '#app' with the selector of your application container
const router = new Router(app, [
  // Define your routes here using the Route class
]);
```

### Parameters

> | name     | data type   | description            | type     |
> |----------|-------------|------------------------|----------|
> | `app`    | HTMLElement | Application container  | Required |
> | `routes` | Array       | Array of route objects | Optional |


## init

Initialize the router by loading the route corresponding to the current URI
without adding it to the history.

```javascript
const app = document.querySelector('#app'); // Replace '#app' with the selector of your application container
const router = new Router(app, [
  new Route('/signin/', 'signin-component'),
  new Route('/', 'home-component'),
]);
router.init();
```

## addRoute


Add a new route to the router.
Each route consists of a path and a custom element associated with that path.

```javascript
router.addRoute('/example/', 'example-component');
```

#### Route Parameters

Routes can include parameters denoted by :param in the path.
These parameters are captured and passed to the associated custom element.

```javascript
router.addRoute('/users/:id/', 'user-profile-component');
```

#### Default Route

If no routes match the current path, a default route (with an empty path) is
used.
This is useful for defining a home page or fallback route.

```javascript
router.addRoute('', 'home-component');
```

### Parameters

> | name            | data type | description                       | type     |
> |-----------------|-----------|-----------------------------------|----------|
> | `path`          | String    | Route path                        | Required |
> | `customElement` | String    | Name of custom element to display | Required |

## navigate

Navigate between routes by specifying the new path.

```javascript
router.navigate('/example/');
```

### Parameters

> | name             | data type   | description                         | type       |
> |------------------|-------------|-------------------------------------|------------|
> | `newPath`        | String      | New path to navigate                | Required   |

### Return

> | data type   | value       | description             |
> |-------------|-------------|-------------------------|
> | null        | null        | Error, path not found   |
> | HTMLElement | HTMLElement | Custom element instance |


## redirect

Redirect to a new path, replacing the current path with the new one.

```javascript
router.redirect('/example/');
```

### Parameters

> | name             | data type   | description                         | type       |
> |------------------|-------------|-------------------------------------|------------|
> | `newPath`        | String      | New path to navigate                | Required   |

### Return

> | data type   | value       | description             |
> |-------------|-------------|-------------------------|
> | null        | null        | Error, path not found   |
> | HTMLElement | HTMLElement | Custom element instance |

--------------------------------------------------------------------------------

## Example

```javascript
const app = document.querySelector('#app');

const router = new Router(app, [
  new Route('/singleplayer/', 'singleplayer-component'),
  new Route('/multiplayer/', 'multiplayer-component'),
  new Route('/tournaments/', 'tournaments-component'),
  new Route('/signin/', 'signin-component'),
  new Route('/signup/', 'signup-component'),
  new Route('', 'home-component'),
]);
router.init();
window.router = router;
```
