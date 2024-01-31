# User-stats API documentation

--------------------------------------------------------------------------------

## `/user/{id}/`

### General user statistics

<details>
 <summary><code>GET</code> <code><b>/user/{id}/</b></code></summary>

### Request

#### Header

> | name            | type   | description  | requirement |
> |-----------------|--------|--------------|-------------|
> | `Authorization` | String | Access token | Required    |

### Response

#### Status code

> | status code | content-type       | response          |
> |-------------|--------------------|-------------------|
> | `200`       | `application/json` | {...}             |
> | `400`       | `application/json` | {"errors": [...]} |
> | `404`       | `application/json` | {"errors": [...]} |
> | `500`       | `application/json` | {"errors": [...]} |

#### Body

> | name             | type | description              |
> |------------------|------|--------------------------|
> | `elo`            | int  | User elo                 |
> | `matches_played` | int  | Number of matches played |
> | `matches_won`    | int  | Number of matches won    |
> | `matches_lost`   | int  | Number of matches lost   |
> | `win_rate`       | int  | Win rate                 |
> | `friends`        | int  | Number of friends        |

</details>

<details>
 <summary><code>POST</code> <code><b>/user/{id}/</b></code></summary>

### Request

#### Header (not implemented)

> | name            | type   | description   | requirement |
> |-----------------|--------|---------------|-------------|
> | `Authorization` | String | Service token | Required    |
 
#### Body 

> | name             | type | description              | requirement |
> |------------------|------|--------------------------|-------------|
> | `elo`            | int  | User elo                 | Optional    |
> | `matches_played` | int  | Number of matches played | Optional    |
> | `matches_won`    | int  | Number of matches won    | Optional    |
> | `matches_lost`   | int  | Number of matches lost   | Optional    |
> | `win_rate`       | int  | Win rate                 | Optional    |
> | `friends`        | int  | Number of friends        | Optional    |

### Response

#### Status code

> | status code | content-type       | response          |
> |-------------|--------------------|-------------------|
> | `201`       | `application/json` | {...}             |
> | `400`       | `application/json` | {"errors": [...]} |
> | `404`       | `application/json` | {"errors": [...]} |
> | `500`       | `application/json` | {"errors": [...]} |

</details>

<details>
 <summary><code>PATCH</code> <code><b>/user/{id}/</b></code></summary>

### Request

#### Header (not implemented)

> | name            | type   | description   | requirement |
> |-----------------|--------|---------------|-------------|
> | `Authorization` | String | Service token | Required    |

#### Body

> | name             | type | description              | requirement |
> |------------------|------|--------------------------|-------------|
> | `elo`            | int  | User elo                 | Optional    |
> | `matches_played` | int  | Number of matches played | Optional    |
> | `matches_won`    | int  | Number of matches won    | Optional    |
> | `matches_lost`   | int  | Number of matches lost   | Optional    |
> | `win_rate`       | int  | Win rate                 | Optional    |
> | `friends`        | int  | Number of friends        | Optional    |

### Response

#### Body

> | name             | type | description              |
> |------------------|------|--------------------------|
> | `elo`            | int  | User elo                 |
> | `matches_played` | int  | Number of matches played |
> | `matches_won`    | int  | Number of matches won    |
> | `matches_lost`   | int  | Number of matches lost   |
> | `win_rate`       | int  | Win rate                 |
> | `friends`        | int  | Number of friends        |

#### Status code

> | status code | content-type       | response          |
> |-------------|--------------------|-------------------|
> | `200`       | `application/json` | {...}             |
> | `400`       | `application/json` | {"errors": [...]} |
> | `404`       | `application/json` | {"errors": [...]} |
> | `500`       | `application/json` | {"errors": [...]} |

</details>

--------------------------------------------------------------------------------

## `/user/{id}/history/`

### User match history

<details>
 <summary><code>GET</code> <code><b>/user/{id}/history/</b></code></summary>

### Request

#### Header

> | name            | type   | description  | requirement |
> |-----------------|--------|--------------|-------------|
> | `Authorization` | String | Access token | Required    |

#### Query

> | name        | type | default | description              | requirement |
> |-------------|------|---------|--------------------------|-------------|
> | `page`      | int  | 1       | Page index               | Optional    |
> | `page_size` | int  | 10      | Number of games per page | Optional    |

### Response

#### Body

> | name      | type        | description     |
> |-----------|-------------|-----------------|
> | `history` | list[Match] | Matches history |

#### Match

> | name              | type   | description            |
> |-------------------|--------|------------------------|
> | `id`              | int    | Match id               |
> | `opponent_id`     | int    | Opponent id            |
> | `date`            | Date   | Match date             |
> | `result`          | String | Match result           |
> | `user_score`      | int    | User score             |
> | `opponent_score`  | int    | Opponent score         |
> | `elo_delta`       | int    | Elo won / lost         |
> | `expected_result` | int    | Probability of winning |

#### Status code

> | status code | content-type       | response          |
> |-------------|--------------------|-------------------|
> | `200`       | `application/json` | {...}             |
> | `400`       | `application/json` | {"errors": [...]} |
> | `404`       | `application/json` | {"errors": [...]} |

</details>

--------------------------------------------------------------------------------

## `/user/{id}/progress/`

### Weekly user progression

<details>
 <summary><code>GET</code> <code><b>/user/{id}/progress/</b></code></summary>

</details>

--------------------------------------------------------------------------------

## `/user/{id}/graph/`

### User graph data

<details>
 <summary><code>GET</code> <code><b>/user/{id}/graph/</b></code></summary>

</details>

--------------------------------------------------------------------------------

## `/match/`

### General matches data

<details>
 <summary><code>POST</code> <code><b>/match/</b></code></summary>

### Request

#### Header (not implemented)

> | name            | type   | description   | requirement |
> |-----------------|--------|---------------|-------------|
> | `Authorization` | String | Service token | Required    |

#### Body

> | name           | type   | default | description             | requirement |
> |----------------|--------|---------|-------------------------|-------------|
> | `winner_id`    | int    | None    | Winner id               | Required    |
> | `loser_id`     | int    | None    | Loser id                | Required    |
> | `winner_score` | int    | None    | Winner score            | Required    |
> | `loser_score`  | int    | None    | Loser score             | Required    |
> | `date`         | String | None    | ISO 8601 formatted date | Required    |

### Response

#### Body

> | name              | type | description       |
> |-------------------|------|-------------------|
> | `winner_match_id` | int  | Winner's match id |
> | `loser_match_id`  | int  | Loser's match id  |

#### Status code

> | status code | content-type       | response          |
> |-------------|--------------------|-------------------|
> | `200`       | `application/json` | {...}             |
> | `400`       | `application/json` | {"errors": [...]} |
> | `404`       | `application/json` | {"errors": [...]} |
> | `500`       | `application/json` | {"errors": [...]} |

</details>
