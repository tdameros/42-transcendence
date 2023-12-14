# Tournament API documentation

--------------------------------------------------------------------------------

## `/tournament`

### Create / retrieve tournament

<details>
 <summary><code>GET</code> <code><b>/tournament</b></code></summary>

#### Retrieve list of available public tournament

</details>

<details>
 <summary><code>POST</code> <code><b>/tournament</b></code></summary>

#### Create a new tournament

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
