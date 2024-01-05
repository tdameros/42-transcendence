# Front documentation

--------------------------------------------------------------------------------

The front-end microservice operates without a database and is solely used to
construct our single-page application using a component-based architecture. The
constraints of the 42 subjects require us not to use any front-end frameworks,
which is why we've developed our own system to easily load components without
requiring extensive JavaScript.

## `loadComponent`

### Load a component from JS Vanilla without reload the page

```async function loadComponent(uri, parentId, setState = true)```

### Parameters

> | name       | data type | description                                                   | type                    |
> |------------|-----------|---------------------------------------------------------------|-------------------------|
> | `uri`      | String    | Component URI                                                 | Required                |
> | `parentId` | String    | Identifier of the parent where the component will be inserted | Required                |
> | `setState` | Boolean   | Add component to browser history                              | Optional (default=true) |

#### Return

> | data type | value | description                          |
> |-----------|-------|--------------------------------------|
> | Boolean   | false | error, component could not be loaded |
> | Boolean   | true  | component successfully loaded        |

--------------------------------------------------------------------------------

