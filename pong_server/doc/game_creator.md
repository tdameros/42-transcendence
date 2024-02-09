# Game Creator API documentation

----------------------------------------------------------------------------------------------------------------------------------------

## `POST /create_game/`

### Request

#### Header (not implemented)

> | name            | type   | description   | requirement |
> |-----------------|--------|---------------|-------------|
> | `Authorization` | String | Service token | Required    |

#### Body

> | name             | type                | description                                                                                                                                                                                                                                                                                                                       | requirement |
> |------------------|---------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------|
> | `request_issuer` | str                 | Either 'tournament' or 'matchmaking'                                                                                                                                                                                                                                                                                              | Required    |
> | `game_id`        | int                 | ID of the created game                                                                                                                                                                                                                                                                                                            | Required    |
> | `players`        | list[Optional[int]] | ID of the players in the game or None when the player doesn't have an opponent in the first round:<br/> <br/> index 0 vs index 1 (At least 1 isn't None)<br/> index 2 vs index 3 (At least 1 isn't None)<br/> ...<br/> <br/> Need at least 2 players (null does not count as a player)<br/> len(players) needs to be a power of 2 | Required    |

### Responseˀ

#### Status code

> | status code | content-type       | response                 | example                                                                        |
> |-------------|--------------------|--------------------------|--------------------------------------------------------------------------------|
> | `201`       | `application/json` | {'game_server_uri': str} | {'game_server_uri': 'http://localhost:60000'}                                  |
> | `400`       | `application/json` | {'errors': list[str]}    | {'errors': ['game_id field is missing', 'players[1] is not an Optional[int]']} |
> | `500`       | `application/json` | {'errors': list[str]}    | {'errors': ['Error creating game server: reason']}                             |
