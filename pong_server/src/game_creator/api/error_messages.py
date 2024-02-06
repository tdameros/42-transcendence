BAD_JSON_FORMAT = 'Invalid JSON format in request body'

REQUEST_ISSUER_FIELD_MISSING = 'request_issuer field is missing'
REQUEST_ISSUER_IS_NOT_A_STRING = 'request_issuer field is not a string'
REQUEST_ISSUER_IS_NOT_VALID = "request_issuer field is not 'tournament' or 'matchmaking'"

GAME_ID_FIELD_MISSING = 'game_id field is missing'
GAME_ID_FIELD_IS_NOT_AN_INTEGER = 'game_id field is not an integer'

PLAYERS_FIELD_MISSING = 'players field is missing'
PLAYERS_FIELD_IS_NOT_A_LIST = 'players field is not a list'


def player_is_found_multiple_times(player_id: int) -> str:
    return f'Player id {player_id} is found multiple times'


def player_is_not_an_optional_int(index: int) -> str:
    return f'players[{index}] is not an Optional[int]'


def error_creating_game_server(error: str) -> str:
    return f'Error creating game server: {error}'


def popen_failed_to_run_command(error: str) -> str:
    return f'Failed to run command to start new game server: {error}'
