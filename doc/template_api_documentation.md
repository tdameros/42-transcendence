# Template API documentation

--------------------------------------------------------------------------------

## `/template`

### Create / retrieve template

<details>
 <summary><code>GET</code> <code><b>/template</b></code></summary>

### Parameters

#### Query

> | name    | data type | description | type                |
> |---------|-----------|-------------|---------------------|
> | `id`    | String    | N/A         | Optional / Required |
> | `...`   | String    | N/A         | Optional / Required |

#### Header

> | name             | data type | description                    | type      |
> |------------------|-----------|--------------------------------|-----------|
> | `Authorization`  | String    | Token for user authentication  | Required  |

#### Cookie

> | name       | data type | description                    | type      |
> |------------|-----------|--------------------------------|-----------|
> | `refresh`  | String    | Token for user authentication  | Required  |

#### Responses

> | http code | content-type               | response                     |
> |-----------|----------------------------|------------------------------|
> | `201`     | `application/json`         | `{"message": "Created"}`     |
> | `401`     | `application/json`         | `{"errors":["Invalid JWT"]}` |

</details>

<details>
 <summary><code>POST</code> <code><b>/template</b></code></summary>

### Parameters

#### Query

> | name    | data type | description | type                |
> |---------|-----------|-------------|---------------------|
> | `id`    | String    | N/A         | Optional / Required |
> | `...`   | String    | N/A         | Optional / Required |

#### Header

> | name             | data type | description                    | type      |
> |------------------|-----------|--------------------------------|-----------|
> | `Authorization`  | String    | Token for user authentication  | Required  |

#### Cookie

> | name       | data type | description                    | type      |
> |------------|-----------|--------------------------------|-----------|
> | `refresh`  | String    | Token for user authentication  | Required  |

#### Body

> ``` javascript
> {
>   "username": "template",
>   "password": "abc1234"
> }
> ```

#### Responses

> | http code | content-type               | response                     |
> |-----------|----------------------------|------------------------------|
> | `201`     | `application/json`         | `{"message": "Created"}`     |
> | `401`     | `application/json`         | `{"errors":["Invalid JWT"]}` |

</details>

--------------------------------------------------------------------------------

## `/template/{id}`

### Retrieve information from a specific template

<details>
 <summary><code>GET</code> <code><b>/template</b></code></summary>

### Parameters

#### Query

> | name    | data type | description | type                |
> |---------|-----------|-------------|---------------------|
> | `id`    | String    | N/A         | Optional / Required |
> | `...`   | String    | N/A         | Optional / Required |

#### Header

> | name             | data type | description                    | type      |
> |------------------|-----------|--------------------------------|-----------|
> | `Authorization`  | String    | Token for user authentication  | Required  |

#### Cookie

> | name       | data type | description                    | type      |
> |------------|-----------|--------------------------------|-----------|
> | `refresh`  | String    | Token for user authentication  | Required  |

#### Responses

> | http code | content-type               | response                     |
> |-----------|----------------------------|------------------------------|
> | `201`     | `application/json`         | `{"message": "Created"}`     |
> | `401`     | `application/json`         | `{"errors":["Invalid JWT"]}` |

</details>
