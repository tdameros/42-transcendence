from tournament import settings

BAD_JSON_FORMAT = 'Invalid JSON format in request body'

NAME_MISSING = 'Missing name field'
NAME_TOO_SHORT = f'Tournament name must contain at least {settings.MIN_TOURNAMENT_NAME_LENGTH} characters'
NAME_TOO_LONG = f'Tournament name must contain less than {settings.MAX_TOURNAMENT_NAME_LENGTH} characters'
NAME_INVALID_CHAR = 'Tournament name may only contain letters, numbers and spaces'

PLAYERS_NOT_INT = 'Tournament name may only contain letters, numbers and spaces'
TOO_MANY_SLOTS = f'Tournament must contain less or equal than {settings.MAX_PLAYERS} slots'
NOT_ENOUGH_SLOTS = f'Tournament must contain at least {settings.MIN_PLAYERS} slots'

NOT_ISO_8601 = 'Registration deadline not in ISO 8601 date and time format'
DEADLINE_PASSED = 'Registration deadline has passed'

IS_PRIVATE_MISSING = 'Missing is-private field'
IS_PRIVATE_NOT_BOOL = 'Is-private must be a boolean'

PASSWORD_MISSING = 'Missing password field'
PASSWORD_NOT_STRING = 'Password must be a string'
PASSWORD_TOO_SHORT = f'Password must contain at least {settings.PASSWORD_MIN_LENGTH} characters'
PASSWORD_TOO_LONG = f'Password must contain less than {settings.PASSWORD_MAX_LENGTH} characters'
PASSWORD_NOT_MATCH = 'Password does not match'

NICKNAME_MISSING = 'Missing nickname field'
NICKNAME_TOO_SHORT = f'Nickname must contain at least {settings.MIN_NICKNAME_LENGTH} characters'
NICKNAME_TOO_LONG = f'Nickname must contain less than {settings.MAX_NICKNAME_LENGTH} characters'
NICKNAME_INVALID_CHAR = 'Nickname may only contain letters, numbers and spaces'

NOT_REGISTERED = 'You are not registered for this tournament'
CANT_LEAVE = 'You can not leave this tournament'

NOT_OWNER = 'You are not the owner of this tournament'
ALREADY_STARTED = 'Tournament has already started'
NOT_ENOUGH_PLAYERS = 'Not enough players to start tournament'

MATCH_FINISHED = 'Match has already finished'
MATCH_STATUS_INVALID = 'Invalid match status'
MATCH_STATUS_NOT_INT = 'Match status must be an integer'
MATCH_PLAYER_NOT_INT = 'Match player must be an integer'
MATCH_PLAYER_NOT_EXIST = 'Match player does not exist'
MATCH_PLAYER_SCORE_NOT_INT = 'Match player score must be an integer'
MATCH_PLAYER_SCORE_INVALID = f'Match player score must be between 0 and {settings.MATCH_POINT_TO_WIN}'
MATCH_WINNER_NOT_INT = 'Match winner must be an integer'
MATCH_WINNER_NOT_EXIST = 'Match winner does not exist'
