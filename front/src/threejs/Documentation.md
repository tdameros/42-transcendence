# Pong Client

## Events when connected to the redirection server:
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
- ### `debug`:
  >> Argument:
  >> ```
  >> debug_message: str
  >> ```
  >
  >> Prints debug_message on `console.warn`

- ### `scene`:
  > As this will likely change I will not write documentation yet

- ### `update_player_movement`:
  > As this will likely change I will not write documentation yet
