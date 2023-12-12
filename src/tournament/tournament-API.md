# Tournament API

## Index:

### 1. Tournament:

| Method   | Endpoint                           | Description                                  |
|----------|------------------------------------|----------------------------------------------|
| `GET`    | `/tournament`                      | Retrieve list of available public tournament |
| `POST`   | `/tournament`                      | Create a new tournament                      |
| `GET`    | `/tournament/{id}`                 | Retrieve details of specific tournament      |
| `DELETE` | `/tournament/{id}`                 | Delete a tournament                          | 
| `PATCH`  | `/tournament/{id}/start`           | Start a tournament                           |
| `PATCH`  | `/tournament/{id}/update-settings` | Update tournament settings                   |

### 2. Players:

| Method | Endpoint                              | Description                                   |
|--------|---------------------------------------|-----------------------------------------------|
| `GET`  | `/tournament/{id}/players`            | Retrieve the list of players for a tournament |
| `POST` | `/tournament/{id}/players`            | Add a player to a specific tournament         |
| `POST` | `/tournament/{id}/regenerate-matches` | Regenerates matches for a tournament          |

### 3. Matches:

| Method  | Endpoint                                    | Description                                   |
|---------|---------------------------------------------|-----------------------------------------------|
| `GET`   | `/tournament/{id}/matches`                  | Retrieve the list of matches for a tournament |
| `GET`   | `/tournament/{id}/matches/{match-id}`       | Retrieve details of a match for a tournament  |
| `PATCH` | `/tournament/{id}/matches/{match-id}/start` | Start a match                                 |
| `PATCH` | `/tournament/{id}/matches/{match-id}/end`   | End a match                                   |
