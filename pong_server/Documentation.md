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
  >>     'json_web_token': The client's Json Web Token,  
  >> }
  >> ```
  >
  >> On success:  
  >>
  >> Accepts the connection
  >
  >> On failure:
  >>
  >> Event `error` is sent to the client
  >
  > If the client fails to disconnect on his own after receiving `error`, they
  > will be kicked from the server