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
  >> Prints debug_message on `console.warn`

- ### `scene`:
  >> Argument:
  >> ```
  >> {
  >>     'scene': {
  >>         'matches': [
  >>             {
  >>                 'position': {'x': float, 'y': float, 'z': float},
  >>                 'players': [
  >>                     {
  >>                         'position': {'x': float, 'y': float, 'z': float},
  >>                         'move_speed': float,
  >>                         'board': {
  >>                             'size': {'x': float, 'y': float, 'z': float}
  >>                         },
  >>                         'paddle': {
  >>                             'size': {'x': float, 'y': float, 'z': float},
  >>                             'position': {'x': float, 'y': float, 'z': float},
  >>                             'movement': {'x': float, 'y': float, 'z': float},
  >>                             'move_speed': float
  >>                         }
  >>                     },
  >>                     ... (Should have 2 players)
  >>                 ],
  >>                 'ball': {
  >>                     'position': {'x': float, 'y': float, 'z': float},
  >>                     'movement': {'x': float, 'y': float, 'z': float},
  >>                     'radius': float
  >>                 }
  >>             }
  >>         ]
  >>     },
  >> 
  >>     'player_location': { // Location of current client
  >>         'is_in_a_match': bool,
  >>         'match_index': int,
  >>         'player_index': int
  >>     }
  >> }
  >> ```
  >
  >>  Replaces current scene with received scene

- ### `update_player`:
  >> Argument:
  >> ```
  >> {
  >>     'player_location': {
  >>         'is_in_a_match': bool,
  >>         'match_index': int,
  >>         'player_index': int
  >>     },
  >>     'direction': str ('up' | 'down' | 'none'),
  >>     'position': {'x': float, 'y': float, 'z': float}
  >> }
  >> ```
  >
  >> Updates the position and direction of the player at index player_index 
