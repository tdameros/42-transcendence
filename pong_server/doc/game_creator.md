# Game Creator API documentation

----------------------------------------------------------------------------------------------------------------------------------------

## `/game_creator/create_game/`

<details>
 <summary><code>POST</code></summary>


### Request

#### Header

> | name            | type   | description   | requirement |
> |-----------------|--------|---------------|-------------|
> | `Authorization` | String | Service token | Required    |

#### Body

> | name             | type                | description                                                                                                                                                                                                                                                                                                                                                                       | requirement |
> |------------------|---------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------|
> | `request_issuer` | str                 | Either 'tournament' or 'matchmaking'                                                                                                                                                                                                                                                                                                                                              | Required    |
> | `game_id`        | int                 | ID of the created game                                                                                                                                                                                                                                                                                                                                                            | Required    |
> | `players`        | list[Optional[int]] | ID of the players in the game or None when the player doesn't have an opponent in the first round:<br/> <br/> index 0 vs index 1 (At least 1 isn't None)<br/> index 2 vs index 3 (At least 1 isn't None)<br/> ...<br/> <br/> Need at least 2 players (null does not count as a player)<br/> len(players) needs to be a power of 2<br/> A player can only be in one game at a time | Required    |

### Response

#### Status code

> | status code | content-type       | response                                                                                     | example                                                                                    |
> |-------------|--------------------|----------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
> | `201`       | `application/json` | {'port': int}                                                                                | {'port': 60000}                                                                            |
> | `400`       | `application/json` | {'errors': list[str]}                                                                        | {'errors': ['game_id field is missing', 'players[1] is not an Optional[int]']}             |
> | `409`       | `application/json` | {'errors': ['Some player(s) are already in a game'], 'players_already_in_a_game': list[int]} | {'errors': ['Some player(s) are already in a game'], 'players_already_in_a_game': [2, 56]} |
> | `500`       | `application/json` | {'errors': list[str]}                                                                        | {'errors': ['Error creating game server: reason']}                                         |

----------------------------------------------------------------------------------------------------------------------------------------

</details>

## `/game_creator/create_private_game/`

<details>
 <summary><code>POST</code></summary>

### Request

#### Header

> | name            | type   | description       | requirement |
> |-----------------|--------|-------------------|-------------|
> | `Authorization` | String | User access token | Required    |

#### Body

> | name          | type | description | requirement |
> |---------------|------|-------------|-------------|
> | `opponent_id` | int  | Opponent ID | Required    |

### Response

#### Status code

> | status code | content-type       | response              | example                                            |
> |-------------|--------------------|-----------------------|----------------------------------------------------|
> | `201`       | `application/json` | {'port': int}         | {'port': 60000}                                    |
> | `400`       | `application/json` | {'errors': list[str]} | {'errors': ['opponent field is missing']}          |
> | `500`       | `application/json` | {'errors': list[str]} | {'errors': ['Error creating game server: reason']} |

</details>

## `/game_creator/remove_players_current_game/`

<details>
 <summary><code>DELETE</code></summary>

### Info
> This should only be used by game_server

### Request

#### Header

> | name            | type   | description   | requirement |
> |-----------------|--------|---------------|-------------|
> | `Authorization` | String | Service token | Required    |

#### Body

> | name             | type      | description                                   | requirement |
> |------------------|-----------|-----------------------------------------------|-------------|
> | `players`        | list[int] | ID of the players who are no longer in a game | Required    |

### Response

#### Status code

> | status code | content-type       | response              | example                                  |
> |-------------|--------------------|-----------------------|------------------------------------------|
> | `204`       | `application/json` | {}                    | {}                                       |
> | `400`       | `application/json` | {'errors': list[str]} | {'errors': ['players[1] is not an int']} |

----------------------------------------------------------------------------------------------------------------------------------------
</details>
