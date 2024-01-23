# `Component`

--------------------------------------------------------------------------------

The Component class is a custom HTML element that extends the HTMLElement class.
It provides a foundation for creating reusable and customizable web components.

This class is an abstract class, and must not be instantiated.

--------------------------------------------------------------------------------

# Methods to be redefined

## render

Returns the HTML content to be rendered inside the component.

```javascript
render() {
  const message = 'Hello World!'
  return `
    <div>
      <h1>${message}</h1>
    </div>
    `;
}
```

## style

Returns the specific CSS content to be rendered inside the component.

```javascript
style() {
  return `
    <style>
      h1 {
        color: red;
      }
    </style>
    `;
}
```

## postRender

Executed after the component has been rendered.

```javascript
postRender() {
  this.title = this.querySelector('h1');
  super.addComponentEventListener('click', this.handleClick);
}
```

## update

Executed when the component is updated.

```javascript
update() {
  this.title.textContent = 'updated!';
}
```

--------------------------------------------------------------------------------

# Inherited Methods

## addComponentEventListener

Adds an event listener to the component.

Component event listener ensures that the "this" instance in the
callback is always defined as the instance of the component. Additionally, this
system prevents event listener leaks even when the callbacks are anonymous
functions.

```javascript
this.username = this.querySelector('#username');
super.addComponentEventListener(this.username, 'input', this.#usernameHandler);
```

### Parameters

> | name       | data type   | description                                                       | type       |
> |------------|-------------|-------------------------------------------------------------------|------------|
> | `element`  | HTMLElement | Selected HTMLElement                                              | Required   |
> | `event`    | String      | A case-sensitive string representing the event type to listen for | Required   |
> | `callback` | Function    | Function call when an event is trigger                            | Required   |

## removeComponentEventListener

Removes an event listener from the component.

```javascript
super.removeComponentEventListener(this.username, 'input');
```

### Parameters

> | name       | data type   | description                                                                       | type       |
> |------------|-------------|-----------------------------------------------------------------------------------|------------|
> | `element`  | HTMLElement | Selected HTMLElement                                                              | Required   |
> | `event`    | String      | A string which specifies the type of event for which to remove an event listener  | Required   |


## removeAllComponentEventListeners

Removes all event listeners from the component.

Automatically called when a component is removed from the DOM.

```javascript
super.removeAllComponentEventListeners();
```
