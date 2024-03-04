# Game Server

## Events:
- ### `connect`:
  >> auth:
  >> ```
  >> {  
  >>     'token': The client's access Json Web Token
  >> }
  >> ```
  >
  >> On success:  
  >>
  >> Accepts the connection  
  >> Event `scene` is sent to the client if the game has started
  >
  >> On failure:
  >>
  >> The connection is refused and an error message is sent to be received by
  >> the connect_error event on the client

- ### `player_is_ready`:
  > Must be sent once the scene is loaded by the client

- ### `update_player`:
  >> Argument:
  >> ```
  >> {
  >>     'client_paddle_position': float (y position),
  >>     'direction': str ('up' | 'down' | 'none')
  >> }
  >> ``` 
  >
  >> Position is bad (due to latency or cheating):
  >>
  >> The position on server side is sent to all clients as well as the new direction
  >
  >> Position is OK:
  >>
  >> Server side position is set to the client side position  
  >> The position sent by the client as well as the new direction is sent to all clients
  >> except the client that sent the update player event
  >
  > The new position and direction are sent using the client `update_player` event
