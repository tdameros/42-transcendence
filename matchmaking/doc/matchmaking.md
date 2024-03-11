# Matchmaking

## Events sent by the client:
- ### `queue_join`:
  >> Argument:  
  >> ```
  >> user_id: int
  >> elo: int
  >> ``` 
  > 
  >> Add the user to the queue

- ### `queue_info`:
  >> Argument:
  >> ```
  >> None
  >> ```
  >
  >> Request information about the queue

## Events sent by the server:
- ### `match`
  >> Argument:
  >> ```
  >> Array [ { user_id: str, elo: int }, { user_id: str, elo: int } ]
  >> ``` 
  >
  >> Send the user_id and elo of the two matched players

- ### `queue_info`:
  >> Argument:
  >> ```
  >> Array [ {...}, {...}, ... ]
  >> ```
  >
  >> Send the queue array with useful information about the players in the queue
