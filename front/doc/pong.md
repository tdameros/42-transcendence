# Pong Client

## Events:
- ### `fatal_error`
  >> Argument:
  >> ```
  >> {
  >>     'error_message': str,   
  >> }
  >> ``` 
  >
  >> Prints error_message on `console.error`
  >> Closes the game

- ### `debug`:
  >> Argument:
  >> ```
  >> debug_message: str
  >> ```
  >
  >> Prints debug_message on `console.log`

- ### `time_sync`:
  >> Argument:
  >> ```
  >> {
  >>     'time1': time1 (value sent during `request_time_sync` event),
  >>     'time2': float (Seconds since the Epoch on server side)
  >> }
  >> ``` 
  >
  >> Allows the client to adapt to latency

- ### `scene`:
  >> Argument:
  >> ```
  >> {
  >>     'scene': {
  >>         'matches': [
  >>             {
  >>                 'location': {
  >>                     'game_round': int,
  >>                     'match': int
  >>                 },
  >>                 'position': {'x': float, 'y': float, 'z': float},
  >>                 'players': [
  >>                     {
  >>                         'position': {'x': float, 'y': float, 'z': float}, // Relative to the match
  >>                         'destination': {'x': float, 'y': float, 'z': float}, // Relative to the match
  >>                         'is_animating': bool,
  >>                         'animation_start_time': float (Seconds since the Epoch),
  >>                         'animation_end_time': float (Seconds since the Epoch),
  >>                         'is_changing_side': bool,
  >>                         'board': {
  >>                             // Position is [0, 0, 0] relative to the player
  >>                             'size': {'x': float, 'y': float, 'z': float}
  >>                         },
  >>                         'paddle': {
  >>                             'size': {'x': float, 'y': float, 'z': float},
  >>                             'position': {'x': float, 'y': float, 'z': float}, // Relative to the player
  >>                             'movement': {'x': float, 'y': float, 'z': float},
  >>                             'move_speed': float
  >>                         }
  >>                     },
  >>                     ... second player
  >>                     (Players can be null if the match is not full yet)
  >>                 ],
  >>                 'ball': {
  >>                     'position': {'x': float, 'y': float, 'z': float}, // Relative to the match
  >>                     'movement': {'x': float, 'y': float, 'z': float},
  >>                     'radius': float,
  >>                     'acceleration': float
  >>                 },
  >>                 'ball_is_waiting': bool,
  >>                 'ball_start_time': Optinal[float] (Seconds since the Epoch)
  >>                 'points': [int, int], // [player1_score, player2_score]
  >>             }
  >>         ],
  >> 
  >>         'loosers': [
  >>             {
  >>                 'position': {'x': float, 'y': float, 'z': float}, // Global
  >>                 'board': {
  >>                     // Position is [0, 0, 0] relative to the player
  >>                     'size': {'x': float, 'y': float, 'z': float}
  >>                 },
  >>                 'paddle': {
  >>                     'size': {'x': float, 'y': float, 'z': float},
  >>                     'position': {'x': float, 'y': float, 'z': float}, // Relative to the player
  >>                     'movement': {'x': float, 'y': float, 'z': float},
  >>                     'move_speed': float
  >>                 }
  >>                 'index_when_lost_match': int (0 (left) | 1 (right)),
  >>             },
  >>         ],
  >> 
  >>         'matches_middle': {
  >>             'x': float,
  >>             'y': float,
  >>         },
  >>         'match_half_width': float,
  >>         'match_half_height': float,
  >>         'matches_x_offset': float,
  >>         'matches_y_offset': float,
  >>
  >>         'points_to_win_match': int,
  >> 
  >>         'paddle_height': float,
  >>         'board_size': {'x': float, 'y': float, 'z': float},
  >>     },
  >>
  >>     'player_location': { // Location of current client
  >>         'is_looser': bool,
  >>         'match_location': {
  >>             'game_round': int,
  >>             'match': int
  >>         },
  >>         'player_index': int,
  >>     },
  >>     'game_has_started': bool,
  >> }
  >> ```
  >
  >> Replaces current scene with received scene

- ### `update_paddle`:
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
  >>     'y_position': float,
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
  >>     'movement': {'x': float, 'y': float, 'z': float},
  >>     'time_at_update': float (Seconds since the Epoch),
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
  >>     'animation_start_time': float (Seconds since the Epoch),
  >>     'animation_end_time': float (Seconds since the Epoch),
  >> }
  >> ```
  >
  >> If it doesn't exist, creates a new match with the `new_match_json`  
  >> Adds the player at [winner_index] to the match to the new match  
  >> Adds the player at [1 - winner_index] to the loosers list

- ### `player_scored_a_point`:
  >> Argument:
  >> ```
  >> {
  >>     'player_location': {
  >>         'is_looser': False,
  >>         'match_location': {
  >>             'game_round': int,
  >>             'match': int
  >>         },
  >>         'player_index': int
  >>     }
  >> }
  >> ```
  >
  >> Should be sent when a player scores a point without winning the match
  >> Adds a point to the player on the screen 

- ### `game_over`:
  >> Argument:
  >> ```
  >> 'winner_index': int
  >> ```
  >
  >> Adds a point to the winner
  >> Removes the ball from the scene
  >> Displays a game over message
