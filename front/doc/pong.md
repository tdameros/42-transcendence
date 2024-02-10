# Pong Client

## Events when connected to the redirection server: (deprecated)
- ### `error`:
  >> Argument:  
  >> ```
  >> error_message: str
  >> ``` 
  > 
  >> Prints error_message on `console.error`  
  >> Disconnects from the server  
  >> 
  >> After this event is received the client will stop trying to connect to
  >> the redirection server and the loading screen will be shown indefinitely

- ### `game_server_uri`:
  >> Argument:
  >> ```
  >> game_server_uri: str
  >> ```
  >
  >> Disconnects the client from the redirection server  
  >> Tries connecting to the game server
  >>
  >> The loading screen will be shown till the game server
  >> sends a `scene` event (or indefinitely if the connection fails)  

## Events when connected to the game server:
- ### `error`
  >> Argument:
  >> ```
  >> error_message: str
  >> ``` 
  >
  >> Prints error_message on `console.error`  

- ### `debug`:
  >> Argument:
  >> ```
  >> debug_message: str
  >> ```
  >
  >> Prints debug_message on `console.log`

  - ### `scene`:
  >>   Argument:
  >>   ```
  >>   {
  >>       'scene': {
  >>           "matches": [
  >>               {
  >>                   "location": {
  >>                       "game_round": int,
  >>                       "match": int
  >>                   },
  >>                   "position": {"x": float, "y": float, "z": float},
  >>                   "players": [
  >>                       {
  >>                           "position": {"x": float, "y": float, "z": float}, // Relative to the match
  >>                           "move_speed": float,
  >>                           "board": {
  >>                               // Position is [0, 0, 0] relative to the player
  >>                               "size": {"x": float, "y": float, "z": float}
  >>                           },
  >>                           "paddle": {
  >>                               "size": {"x": float, "y": float, "z": float},
  >>                               "position": {"x": float, "y": float, "z": float}, // Relative to the player
  >>                               "movement": {"x": float, "y": float, "z": float},
  >>                               "move_speed": float
  >>                           }
  >>                       },
  >>                       ... second player
  >>                       (Players can be null if the match is not full yet)
  >>                   ],
  >>                   "ball": {
  >>                       "position": {"x": float, "y": float, "z": float}, // Relative to the match
  >>                       "movement": {"x": float, "y": float, "z": float},
  >>                       "radius": float,
  >>                       "acceleration": float
  >>                   },
  >>                   "ball_is_waiting": bool,
  >>                   "ball_start_time": Optinal[float] (Seconds since the Epoch)
  >>               }
  >>           ],
  >> 
  >>           "loosers": [
  >>               (List of players with the same structure as the players in the matches exept the position is global)
  >>           ]
  >>       }
  >>
  >>       'player_location': { // Location of current client
  >>           'is_looser': bool,
  >>           'match_location': {
  >>               'game_round': int,
  >>               'match': int
  >>           },
  >>           'player_index': int
  >>       }
  >>   }
  >>   ```
  >
  >>    Replaces current scene with received scene

- ### `update_player`:
  >> Argument:
  >> ```
  >> {
  >>     'player_location': {
  >>         'is_looser': bool,
  >>         'match_location': {
  >>             'game_round': int,
  >>             'match': int
  >>         },
  >>         'player_index': int
  >>     },
  >>     'direction': str ('up' | 'down' | 'none'),
  >>     'position': {'x': float, 'y': float, 'z': float}
  >> }
  >> ```
  >
  >> Updates the position and direction of the player at index player_index 

- ### `prepare_ball_for_match`:
  >> Argument:
  >> ```
  >> {
  >>     'match_location': {
  >>         'game_round': int,
  >>         'match': int
  >>     },
  >>     'ball_movement': {'x': float, 'y': float, 'z': float}
  >>     'ball_start_time': float (Seconds since the Epoch),
  >> }
  >> ```
  >
  >> For the ball at `matches[match_location]`:  
  >> Sets the ball position to `[0., 0., current_position.z]`.  
  >> Sets the ball movement to `'ball_movement'`  
  >> Stops the ball movement till `ball_start_time`

- ### `update_ball`:
  >> Argument:
  >> ```
  >> {
  >>     'match_location': {
  >>         'game_round': int,
  >>         'match': int
  >>     },
  >>     'position': {'x': float, 'y': float, 'z': float},
  >>     'movement': {'x': float, 'y': float, 'z': float}
  >> }
  >> ```
  >
  >> Updates the position and movement of the ball in the match at index match_index