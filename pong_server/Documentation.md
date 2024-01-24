# Redirection Server (deprecated)

Whenever you see 'Event `event_name` is sent to the client', you can find details for the event in PROJECT/front/src/threejs/Documentation.md

## Events:
- ### `connect`:  
  >> Query string:  
  >> ```
  >> {  
  >>     'json_web_token': The client's Json Web Token,  
  >>     'game_id': game id of the game the client is trying to join (string)  
  >> }
  >> ```
  > 
  >> On success:
  >> 
  >> Event `game_server_uri` is sent to the client  
  >
  >> On failure:
  >>
  >> Event `error` is sent to the client
  >
  > If the client fails to disconnect on his own after receiving `error` or
  > `game_server_uri`, they will be kicked from the server


# Game Server

## Events:
- ### `connect`:
  >> Query string:
  >> ```
  >> {  
  >>     'json_web_token': The client's Json Web Token
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

- ### `update_player`:
  >> Argument:
  >> ```
  >> {
  >>     'client_player_position': float[3],
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