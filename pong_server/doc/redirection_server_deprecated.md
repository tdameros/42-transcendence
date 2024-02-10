# Redirection Server (deprecated)

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
