# User-stats API documentation

--------------------------------------------------------------------------------

## `/user/{id}`

### General user statistics

<details>
 <summary><code>GET</code> <code><b>/user/{id}</b></code></summary>

### Request

#### Header

> | name            | type   | description  | type     |
> |-----------------|--------|--------------|----------|
> | `Authorization` | String | Access token | Required |

### Response

#### Status code

> | status code | content-type       | response          |
> |-------------|--------------------|-------------------|
> | `200`       | `application/json` | {...}             |
> | `400`       | `application/json` | {"errors": [...]} |
> | `404`       | `application/json` | {"errors": [...]} |

#### Body

> | name           | type | description            |
> |----------------|------|------------------------|
> | `elo`          | int  | User elo               |
> | `games_played` | int  | Number of games played |
> | `games_won`    | int  | Number of games won    |
> | `games_lost`   | int  | Number of games lost   |
> | `win_rate`     | int  | Win rate               |
> | `friends`      | int  | Number of friends      |

</details>

<details>
 <summary><code>POST</code> <code><b>/user/{id}</b></code></summary>

### Request

#### Header (not implemented)

> | name            | type   | description   | type     |
> |-----------------|--------|---------------|----------|
> | `Authorization` | String | Service token | Required |
 
#### Body 

> | name           | type | description            |
> |----------------|------|------------------------|
> | `elo`          | int  | User elo               |
> | `games_played` | int  | Number of games played |
> | `games_won`    | int  | Number of games won    |
> | `games_lost`   | int  | Number of games lost   |
> | `win_rate`     | int  | Win rate               |
> | `friends`      | int  | Number of friends      |

### Response

#### Status code

> | status code | content-type       | response          |
> |-------------|--------------------|-------------------|
> | `201`       | `application/json` | {...}             |
> | `400`       | `application/json` | {"errors": [...]} |
> | `404`       | `application/json` | {"errors": [...]} |

</details>

<details>
 <summary><code>PATCH</code> <code><b>/user/{id}</b></code></summary>

### Request

#### Header (not implemented)

> | name            | type   | description   | type     |
> |-----------------|--------|---------------|----------|
> | `Authorization` | String | Service token | Required |

#### Body

> | name           | type | description            |
> |----------------|------|------------------------|
> | `elo`          | int  | User elo               |
> | `games_played` | int  | Number of games played |
> | `games_won`    | int  | Number of games won    |
> | `games_lost`   | int  | Number of games lost   |
> | `win_rate`     | int  | Win rate               |
> | `friends`      | int  | Number of friends      |

### Response

#### Body

> | name           | type | description            |
> |----------------|------|------------------------|
> | `elo`          | int  | User elo               |
> | `games_played` | int  | Number of games played |
> | `games_won`    | int  | Number of games won    |
> | `games_lost`   | int  | Number of games lost   |
> | `win_rate`     | int  | Win rate               |
> | `friends`      | int  | Number of friends      |

#### Status code

> | status code | content-type       | response          |
> |-------------|--------------------|-------------------|
> | `200`       | `application/json` | {...}             |
> | `400`       | `application/json` | {"errors": [...]} |
> | `404`       | `application/json` | {"errors": [...]} |

</details>

--------------------------------------------------------------------------------

## `/user/{id}/games/`

### User game history

<details>
 <summary><code>GET</code> <code><b>/user/{id}/games/</b></code></summary>

</details>

--------------------------------------------------------------------------------

## `/user/{id}/progress/`

### Weekly user progression

<details>
 <summary><code>GET</code> <code><b>/user/{id}/progress/</b></code></summary>

</details>

--------------------------------------------------------------------------------

## `/user/{id}/graph/`

### User game history

<details>
 <summary><code>GET</code> <code><b>/user/{id}/graph/</b></code></summary>

</details>
