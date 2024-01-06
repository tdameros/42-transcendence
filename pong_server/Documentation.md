# Redirection Server

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
  >>
  >> The client is expected to disconnect from the server when this event is received
  >
  >> On failure:
  >>
  >> Event `error` is sent to the client
  >>
  >> The client is expected to disconnect from the server when this event is received
  >
  > If the client fails to disconnect on his own after receiving `error` or
  > `game_server_uri`, they will be kicked from the server


# Game Server

## Events:
- ### `connect`:  
  > Will always accept the connection (for now)