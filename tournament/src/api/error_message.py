from tournament import settings

BAD_JSON_FORMAT = 'Invalid JSON format in request body'

NAME_MISSING = 'Missing name field'
NAME_TOO_SHORT = f'Tournament name must contain at least {settings.MIN_TOURNAMENT_NAME_LENGTH} characters'
NAME_TOO_LONG = f'Tournament name must contain less than {settings.MAX_TOURNAMENT_NAME_LENGTH} characters'
NAME_INVALID_CHAR = 'Tournament name may only contain letters, numbers and spaces'

PLAYERS_NOT_INT = 'Tournament name may only contain letters, numbers and spaces'
TOO_MANY_SLOTS = f'Tournament must contain less than {settings.MAX_PLAYERS} slots'
NOT_ENOUGH_SLOTS = f'Tournament must contain at least {settings.MIN_PLAYERS} slots'

NOT_ISO_8601 = 'Registration deadline not in ISO 8601 date and time format'
DEADLINE_PASSED = 'Registration deadline has passed'

IS_PRIVATE_MISSING = 'Missing is-private field'
IS_PRIVATE_NOT_BOOL = 'Is-private must be a boolean'

NICKNAME_MISSING = 'Missing nickname field'
NICKNAME_TOO_SHORT = f'Nickname must contain at least {settings.MIN_NICKNAME_LENGTH} characters'
NICKNAME_TOO_LONG = f'Nickname must contain less than {settings.MAX_NICKNAME_LENGTH} characters'
NICKNAME_INVALID_CHAR = 'Nickname may only contain letters, numbers and spaces'
