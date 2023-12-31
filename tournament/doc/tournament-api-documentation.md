# Tournament API documentation

--------------------------------------------------------------------------------

## `/tournament`

### Create / retrieve tournament

Retrieve list of available public tournament

<details>
 <summary><code>GET</code> <code><b>/tournament</b></code></summary>

</details>

Create a new tournament

<details>
 <summary><code>POST</code> <code><b>/tournament</b></code></summary>


### Parameters

#### Body

- Tournament name must be between 3 and 20 characters and can only contain alnum and space
- Players must be between 2 and 16 (optional, default = 16 players)
- Registration deadline (optional)
- A boolean that specifies if tournament is private

> ```javascript
> {
>     "name": "World Championship",
>     "max-players": 16,
>     "registration-deadline": "2024-02-17T10:53",
>     "is-private": true
> }
> ```

#### Responses

> | http code | content-type       | response                            |
> |-----------|--------------------|-------------------------------------|
> | `201`     | `application/json` | `{"status": "Created"}`             |
> | `401`     | `application/json` | `{"errors": ["AAA", "BBB", "..."]}` |

errors can be combined
 
> errors can be:
> - Missing name field
> - Tournament name must contain at least 3 characters
> - Tournament name must contain less than 20 characters
> - Tournament name may only contain letters, numbers and spaces
> - Max players must be an integer
> - Tournament must contain less than 16 slots
> - Tournament must contain at least 2 slots
> - Registration deadline not in ISO 8601 date and time format
> - Registration deadline has passed
> - Missing is-private field
> - Is private must be a boolean
> - Missing Authorization header
> - Invalid JSON format in request body

</details>

--------------------------------------------------------------------------------

## `/tournament/{id}`

### Manage a tournament

<details>
 <summary><code>GET</code> <code><b>/tournament/{id}</b></code></summary>

#### Retrieve details of specific tournament

</details>

<details>
 <summary><code>DELETE</code> <code><b>/tournament/{id}</b></code></summary>

#### Delete a tournament

</details>

<details>
 <summary><code>PATCH</code> <code><b>/tournament/{id}/start</b></code></summary>

#### Start a tournament

</details>

<details>
 <summary><code>PATCH</code> <code><b>/tournament/{id}/update-settings</b></code></summary>

#### Update tournament settings

</details>

--------------------------------------------------------------------------------

## `/tournament/{id}/players`

### Manage players of a tournament

<details>
 <summary><code>GET</code> <code><b>/tournament/{id}/players</b></code></summary>

#### Retrieve the lis of players for a tournament

</details>

<details>
 <summary><code>POST</code> <code><b>/tournament/{id}/players</b></code></summary>

#### Add a player to a specific tournament

</details>

--------------------------------------------------------------------------------

## `/tournament/{id}/matches`

### Manage matches of a tournament

<details>
 <summary><code>GET</code> <code><b>/tournament/{id}/matches</b></code></summary>

#### Retrieve the list of matches for a tournament

</details>

<details>
 <summary><code>GET</code> <code><b>/tournament/{id}/matches/{match-id}</b></code></summary>

#### Retrieve details of a match for a tournament

</details>

<details>
 <summary><code>PATCH</code> <code><b>/tournament/{id}/matches/{match-id}/start</b></code></summary>

#### Start a match

</details>

<details>
 <summary><code>PATCH</code> <code><b>/tournament/{id}/matches/{match-id}/end</b></code></summary>

#### End a match

</details>

<details>
 <summary><code>POST</code> <code><b>/tournament/{id}/matches/regenerate</b></code></summary>

#### Regenerates matches for a tournament

</details>
