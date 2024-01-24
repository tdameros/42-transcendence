# `Cookies`

--------------------------------------------------------------------------------

The Cookies class provides a simple and convenient way to manage cookies in a
web application. It offers methods for retrieving, adding, and removing cookies
with additional options for security.

It is defined as static, so there's no need to create an instance.

--------------------------------------------------------------------------------

## get

Returns the value of the cookie with the specified name.

```javascript
Cookies.get('username');
```

### Parameters

> | name   | data type | description            | type     |
> |--------|-----------|------------------------|----------|
> | `name` | String    | The name of the cookie | Required |

### Return

> | data type | value                             | description                       |
> |-----------|-----------------------------------|-----------------------------------|
> | null      | null                              | The cookie does not exist         |
> | String    | The value of the specified cookie | The value of the specified cookie |

## add

Adds a new cookie with the given name and value.

```javascript
Cookies.add('username', 'John Doe');
```

### Parameters

> | name    | data type | description             | type     |
> |---------|-----------|-------------------------|----------|
> | `name`  | String    | The name of the cookie  | Required |
> | `value` | String    | The value of the cookie | Required |


## remove

Removes the cookie with the specified name.

```javascript
Cookies.remove('username');
```

### Parameters

> | name   | data type | description            | type     |
> |--------|-----------|------------------------|----------|
> | `name` | String    | The name of the cookie | Required |
