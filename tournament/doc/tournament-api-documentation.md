# Tournament API documentation

--------------------------------------------------------------------------------

## `/tournament`

### Create / retrieve tournament

Retrieve list of available public tournament

<details>
 <summary><code>GET</code> <code><b>/tournament</b></code></summary>


### Parameters

#### Query

> | name                | value type | description                                              | type      |
> |---------------------|------------|----------------------------------------------------------|-----------|
> | `page`              | Integer    | the current page                                         | Optional  |
> | `page-size`         | Integer    | the number of items per page, defaults to 10, maximum 50 | Optional  |
> | `display-private`   | none       | display private tournament                               | Optional  |
> | `display-completed` | none       | display completed tournament                             | Optional  |

### Responses

> | http code | content-type               | response                                     |
> |-----------|----------------------------|----------------------------------------------|
> | `200`     | `application/json`         | `{"public-tournaments": [tournament1, ...]}` |
> | `401`     | `application/json`         | `{"errors":["AAA", ...]}`                    |

</details>

Create a new tournament

<details>
 <summary><code>POST</code> <code><b>/tournament</b></code></summary>


### Parameters

#### Body

- Tournament name must be between 3 and 20 characters and can only contain alnum and space
- Players must be between 2 and 16 (optional, default = 16 players)
- Registration deadline (optional)
- Nickname for the tournament (optional)
- A boolean that specifies if tournament is private
- A password for the tournament (if is-private is true)

> ```javascript
> {
>     "name": "World Championship",
>     "max-players": 16,
>     "registration-deadline": "2024-02-17T10:53",
>     "is-private": true,
>     "password": "Password1%"
>     "nickname": "Player"
> }
> ```

### Responses

> | http code     | content-type       | response                               |
> |---------------|--------------------|----------------------------------------|
> | `201`         | `application/json` | `{"id": 1, "name": "Tournament", ...}` |
> | `400` / `401` | `application/json` | `{"errors": ["AAA", "BBB", "..."]}`    |

</details>

Delete all tournaments created by the user (with status `created`)

<details>
 <summary><code>DELETE</code> <code><b>/tournament</b></code></summary>

### Parameters

None

### Responses

> | http code | content-type       | response                                                            |
> |-----------|--------------------|---------------------------------------------------------------------|
> | `200`     | `application/json` | `{"message": "tournaments created by this user have been deleted"}` |
> | `401`     | `application/json` | `{"errors": ["error message", ...]}`                                |


</details>

--------------------------------------------------------------------------------

## `/tournament/{id}`

### Manage a tournament

Retrieve details of specific tournament

<details>
 <summary><code>GET</code> <code><b>/tournament/{id}</b></code></summary>

### Parameters

None

### Responses

Body

> ```javascript
> {
>       "id": 1,
>       "name": "Tournament",
>       "max-players": 16,
>       "nb-players": 1,
>       "players": [
>          {
>             "nickname": "Player",
>             "user_id": 2
>           }
>       ],
>       "registration-deadline": "2024-02-17T10:53",
>       "is-private": true,
>       "status": "created",
>       "admin": "edelage",
> 

> | http code | content-type       | response                               |
> |-----------|--------------------|----------------------------------------|
> | `200`     | `application/json` | `{"id": 1, "name": "Tournament", ...}` |
> | `404`     | `application/json` | `{"errors": ["error message", ...]}`   |

</details>

Delete a tournament

<details>
 <summary><code>DELETE</code> <code><b>/tournament/{id}</b></code></summary>

### Parameters

None

### Responses

> | http code                     | content-type       | response                                         |
> |-------------------------------|--------------------|--------------------------------------------------|
> | `200`                         | `application/json` | `{"message": "tournament successfully deleted"}` |
> | `400` / `401` / `403` / `404` | `application/json` | `{"errors": ["error message", ...]}`             |

</details>

Update tournament settings

<details>
 <summary><code>PATCH</code> <code><b>/tournament/{id}</b></code></summary>

### Parameters

#### Body

- Tournament name must be between 3 and 20 characters and can only contain alnum and space (optional)
- Players must be between 2 and 16 (optional)
- Registration deadline (optional)
- A boolean that specifies if tournament is private (optional)
- A password for the tournament (optional)

> ```javascript
> {
>   "name": "World Championship",
>   "max-players": 16,
>   "registration-deadline": "2024-02-17T10:53",
>   "is-private": true,
>   "password": "Password1%"
> }

### Responses

> | http code      | content-type       | response                               |
> |----------------|--------------------|----------------------------------------|
> | `200`          | `application/json` | `{"id": 1, "name": "Tournament", ...}` |
> | `400` / `403`  | `application/json` | `{"errors": ["AAA", "BBB", "..."]}`    |

</details>

Start a tournament

<details>
 <summary><code>PATCH</code> <code><b>/tournament/{id}/start</b></code></summary>

### Parameters

None

### Responses

> | http code | content-type       | response                            |
> |-----------|--------------------|-------------------------------------|
> | `200`     | `application/json` | `{"message": "..."}`                |
> | `400`     | `application/json` | `{"errors": ["AAA", "BBB", "..."]}` |

</details>

--------------------------------------------------------------------------------

## `/tournament/{id}/players`

### Manage players of a tournament

Retrieve the list of players for a tournament

<details>
 <summary><code>GET</code> <code><b>/tournament/{id}/players</b></code></summary>

### Responses

#### Body

> ```javascript
>   {
>       "max-players": 16,
>       "players": [
>           {
>               "nickname": "Player",
>               "user_id": 2
>           }     
>       ] 
>   }
> ```

> | http code | content-type       | response                                          |
> |-----------|--------------------|---------------------------------------------------|
> | `200`     | `application/json` | `{"players": [{"nickname": "Player", ...}, ...]}` |
> | `404`     | `application/json` | `{"errors": ["AAA", ...]}`                        |

</details>

Add a player to a specific tournament

<details>
 <summary><code>POST</code> <code><b>/tournament/{id}/players</b></code></summary>

### Parameters

#### Body

- Nickname for the tournament
- The tournament password (if tournament is private)

> ```javascript
> {
>     "nickname": "Player"
> }
> ```

### Responses

> | http code              | content-type       | response                                        |
> |------------------------|--------------------|-------------------------------------------------|
> | `201`                  | `application/json` | `{"id": 1, "nickname": "Player", "user_id": 2}` |
> | `400` / `403` / `404`  | `application/json` | `{"errors": ["AAA", "BBB", "..."]}`             |

</details>

--------------------------------------------------------------------------------

## `/tournament/player`

Anonymizes a user's nicknames

<details>
 <summary><code>POST</code> <code><b>/tournament/player/anonymize</b></code></summary>

### Parameters

None

### Responses

> | http code | content-type       | response                                        |
> |-----------|--------------------|-------------------------------------------------|
> | `200`     | `application/json` | `{"message": "player successfully anonymized"}` |

</details>

--------------------------------------------------------------------------------

## `/tournament/{id}/matches`

### Manage matches of a tournament

Retrieve the list of matches for a tournament

<details>
 <summary><code>GET</code> <code><b>/tournament/{id}/matches</b></code></summary>

### Parameters

None

### Responses

> Example:
> ```javascript
> {
>  "nb-matches": 14,
>   "matches": [
>       {
>           "id": 1,
>           "status": "Finished",
>           "player1": "Player1",
>           "player2": "Player2",
>           "player_1_score": 2,
>           "player_2_score": 1,
>           "winner": "Player1"
>       },
>       {
>           ...
>       }
> ]
> }
> ```

</details>

Generate matches for a tournament

<details>
 <summary><code>POST</code> <code><b>/tournament/{id}/matches/generate</b></code></summary>

### Parameters

#### Body

- Randomly generate matches (optional, default = false)

> ```javascript
> {
>   "random": true
> }

### Responses

> | http code | content-type       | response                               |
> |-----------|--------------------|----------------------------------------|
> | `200`     | `application/json` | `{"nb-matches": 14, "matches": [...]}` |
> | `404`     | `application/json` | `{"errors": ["AAA", ...]}`             |

</details>

--------------------------------------------------------------------------------

## `/tournament/{id}/match`

### Manage match of a tournament

Retrieve details of a match

<details>
 <summary><code>GET</code> <code><b>/tournament/{id}/match/{match-id}</b></code></summary>

### Parameters

None

### Responses

> Example:
> ```javascript
> {
>   "id": 1,
>   "status": "Finished",
>   "player1": "Player1",
>   "player2": "Player2",
>   "player_1_score": 2,
>   "player_2_score": 1,
>   "winner": "Player1"
> }
> ```

> | http code | content-type       | response                                   |
> |-----------|--------------------|--------------------------------------------|
> | `200`     | `application/json` | `{"id": 1, "status": "In-progress", ...}`  |
> | `404`     | `application/json` | `{"errors": ["AAA", ...]}`                 |

</details>

Start a match

<details>
 <summary><code>POST</code> <code><b>/tournament/{id}/match/{match-id}/start</b></code></summary>

### Parameters

#### Body

All fields are optional

- The status of the match
- The first player
- The second player

> ```javascript
> {
>   "player1": 1,
>   "player2": 2
> }

### Responses

> | http code | content-type       | response                                  |
> |-----------|--------------------|-------------------------------------------|
> | `200`     | `application/json` | `{"id": 1, "status": "In-progress", ...}` |
> | `400`     | `application/json` | `{"errors": ["AAA", "BBB", "..."]}`       |

</details>

Add one point to a player

<details>
 <summary><code>POST</code> <code><b>/tournament/{id}/match/{match-id}/add-point</b></code></summary>

### Parameters

#### Body

- The player to add a point

> ```javascript
> {
>   "player": 1
> }
> ```

### Responses

> | http code | content-type       | response                                  |
> |-----------|--------------------|-------------------------------------------|
> | `200`     | `application/json` | `{"id": 1, "status": "In-progress", ...}` |
> | `400`     | `application/json` | `{"errors": ["AAA", "BBB", "..."]}`       |

</details>

End a match

<details>
 <summary><code>POST</code> <code><b>/tournament/{id}/match/{match-id}/end</b></code></summary>

### Parameters

#### Body

- Winner of the match

> ```javascript
> {
>   "winner": 2
> }
> ```

### Responses

> | http code | content-type       | response                               |
> |-----------|--------------------|----------------------------------------|
> | `200`     | `application/json` | `{"id": 1, "status": "Finished", ...}` |
> | `400`     | `application/json` | `{"errors": ["AAA", "BBB", "..."]}`    |

</details>
