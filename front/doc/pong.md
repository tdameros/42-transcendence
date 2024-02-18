# Pong Client

## Events:
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

- ### `player_won_match`:
  >> Argument:
  >> ```
  >> {
  >>     'finished_match_location': {
  >>         'game_round': int,
  >>         'match': int
  >>     },
  >>     'winner_index': int,
  >>     'new_match_json': (Same as the match in the scene but without the 'players' field)
  >> }
  >> ```
  >
  >> If it doesn't exist, creates a new match with the `new_match_json`  
  >> Adds the player at [winner_index] to the match to the new match  
  >> Adds the player at [1 - winner_index] to the loosers list
 
- ### `game_over`:
  >> ```
  >> {
  >>     'winner_index': int
  >> }
  >> ```
  >
  >> Work in progress
