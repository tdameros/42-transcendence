# User-stats API documentation

--------------------------------------------------------------------------------

## `/statistics/user/{id}/`

### General user statistics

<details>
 <summary><code>GET</code> <code><b>/statistics/user/{id}/</b></code></summary>

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
 <summary><code>POST</code> <code><b>/statistics/user/{id}/</b></code></summary>

### Request

#### Header

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
 <summary><code>PATCH</code> <code><b>/statistics/user/{id}/</b></code></summary>

### Request

#### Header

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

## `/statistics/user/{id}/history/`

### User match history

<details>
 <summary><code>GET</code> <code><b>/statistics/user/{id}/history/</b></code></summary>

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

> | name          | type        | description              |
> |---------------|-------------|--------------------------|
> | `history`     | list[Match] | Matches history          |
> | `total_pages` | int         | The total number of page |

#### Match

> | name              | type       | description            |
> |-------------------|------------|------------------------|
> | `id`              | int        | Match id               |
> | `opponent_id`     | int / None | Opponent id            |
> | `date`            | Date       | Match date             |
> | `result`          | String     | Match result           |
> | `user_score`      | int        | User score             |
> | `opponent_score`  | int        | Opponent score         |
> | `elo_delta`       | int        | Elo won / lost         |
> | `expected_result` | int        | Probability of winning |

#### Status code

> | status code | content-type       | response          |
> |-------------|--------------------|-------------------|
> | `200`       | `application/json` | {...}             |
> | `400`       | `application/json` | {"errors": [...]} |
> | `404`       | `application/json` | {"errors": [...]} |

</details>

--------------------------------------------------------------------------------

## `/statistics/user/{id}/progress/`

### Weekly user progression

<details>
 <summary><code>GET</code> <code><b>/statistics/user/{id}/progress/</b></code></summary>

### Request

#### Header

> | name            | type   | description   | requirement |
> |-----------------|--------|---------------|-------------|
> | `Authorization` | String | Service token | Required    |

#### Query

> | name   | type   | default | description | requirement |
> |--------|--------|---------|-------------|-------------|
> | `days` | int    | 7       | Days span   | Optional    |

### Response

#### Body

> | name             | type | description                |
> |------------------|------|----------------------------|
> | `elo`            | int  | Elo progression            |
> | `win_rate`       | int  | Win rate progression       |
> | `matches_played` | int  | Matches played progression |
> | `friends`        | int  | Friends progression        |

#### Status code

> | status code | content-type       | response          |
> |-------------|--------------------|-------------------|
> | `200`       | `application/json` | {...}             |
> | `400`       | `application/json` | {"errors": [...]} |
> | `404`       | `application/json` | {"errors": [...]} |
> | `500`       | `application/json` | {"errors": [...]} |

</details>

--------------------------------------------------------------------------------

## `/statistics/user/{id}/graph/`

### User graph data

<details>
 <summary><code>GET</code> <code><b>/statistics/user/{id}/graph/.../</b></code></summary>

 <code>GET</code> <code><b>/statistics/user/{id}/graph/elo/</b></code>

 <code>GET</code> <code><b>/statistics/user/{id}/graph/win_rate/</b></code>

 <code>GET</code> <code><b>/statistics/user/{id}/graph/matches_played/</b></code>

### Request

#### Header

> | name            | type   | description  | requirement |
> |-----------------|--------|--------------|-------------|
> | `Authorization` | String | Access token | Required    |

#### Query

> | name         | type | default | description                               | requirement |
> |--------------|------|---------|-------------------------------------------|-------------|
> | `start`      | date | none    | iso 8061 formatted date                   | required    |
> | `end`        | date | none    | iso 8061 formatted date                   | required    |
> | `max_points` | int  | None    | The maximum number of values in the graph | Required    |

### Response

#### Body

> | name         | type        | description                   |
> |--------------|-------------|-------------------------------|
> | `graph`      | list[Graph] | Graph data                    |
> | `num_points` | int         | Number of points in the graph |

#### Graph

> | name    | type | description |
> |---------|------|-------------|
> | `date`  | Date | Date        |
> | `value` | int  | Value       |

#### Status code

> | status code | content-type       | response          |
> |-------------|--------------------|-------------------|
> | `200`       | `application/json` | {...}             |
> | `400`       | `application/json` | {"errors": [...]} |
> | `404`       | `application/json` | {"errors": [...]} |
> | `500`       | `application/json` | {"errors": [...]} |

</details>

--------------------------------------------------------------------------------

## `/statistics/user/{id}/friends/`

### Friends history

<details>
 <summary><code>POST</code> <code><b>/statistics/user/{id}/friends</b></code></summary>

### Request

#### Header

> | name            | type   | description   | requirement |
> |-----------------|--------|---------------|-------------|
> | `Authorization` | String | Service token | Required    |

#### Body

> | name        | type | default | description                   | requirement |
> |-------------|------|---------|-------------------------------|-------------|
> | `increment` | bool | None    | Addition/Deletion of a friend | Required    |

### Response

#### Body

> | name        | type  | description              |
> |-------------|-------|--------------------------|
> | `new_entry` | dict  | New FriendsHistory entry |

#### Status code

> | status code | content-type       | response          |
> |-------------|--------------------|-------------------|
> | `200`       | `application/json` | {...}             |
> | `400`       | `application/json` | {"errors": [...]} |
> | `401`       | `application/json` | {"errors": [...]} |
> | `500`       | `application/json` | {"errors": [...]} |

</details>

--------------------------------------------------------------------------------

## `/statistics/match/`

### General matches data

<details>
 <summary><code>POST</code> <code><b>/statistics/match/</b></code></summary>

### Request

#### Header

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
> | `date`         | String | None    | ISO 8601 formatted date | Optional    |

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

--------------------------------------------------------------------------------

## `/statistics/ranking/`

### User ranking

<details>
 <summary><code>GET</code> <code><b>/statistics/ranking/</b></code></summary>

### Request

#### Header

> | name            | type   | description  | requirement |
> |-----------------|--------|--------------|-------------|
> | `Authorization` | String | Access token | Required    |

#### Query

> | name        | type   | default | description              | requirement |
> |-------------|--------|---------|--------------------------|-------------|
> | `page`      | int    | 1       | Page index               | Optional    |
> | `page_size` | int    | 100     | Numbers of user per page | Optional    |

### Response

#### Body

> | name          | type       | description              |
> |---------------|------------|--------------------------|
> | `ranking`     | list[User] | User ranking             |
> | `total_pages` | int        | The total number of page |

#### User

> | name             | type | description              |
> |------------------|------|--------------------------|
> | `id`             | int  | User id                  |
> | `elo`            | int  | User elo                 |
> | `matches_played` | int  | Number of matches played |
> | `win_rate`       | int  | User win rate            |
 
#### Status code

> | status code | content-type       | response          |
> |-------------|--------------------|-------------------|
> | `200`       | `application/json` | {...}             |
> | `400`       | `application/json` | {"errors": [...]} |
> | `500`       | `application/json` | {"errors": [...]} |

</details>
