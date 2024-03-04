import os

import generate_pair_of_keys
from dotenv import load_dotenv, set_key

# If you are not in prod, this script shall be called once from root.
# If the app is live, this script shall be called once from the makefile (generate_env rule).

# This script will generate keys in the .env file of your choice.
# Some .env files such as ACCESS_SERVICE_KEY are common so that multiple services can access them.
# Some other .env files such as USER_MANAGEMENT_SECRET_KEY are specific to a service,
# but should be generated here as well for consistency.

# This script shall also retrieve static keys needed for the app to work properly (such as 3rd party API keys).
# All of these keys shall be stored in a .env file located at the project's root.
# An example of what this file should look like is provided in the .env.example file.

# Load the .env file in the root directory
load_dotenv('.env')
COMMON_ENV_FILE = 'common/src/.env'

USER_MANAGEMENT_ENV_FILE = 'user_management/src/.env'
USER_STATS_ENV_FILE = 'user_stats/src/.env'
TOURNAMENT_ENV_FILE = 'tournament/src/.env'
GAME_CREATOR_ENV_FILE = 'pong_server/src/game_creator/.env'
NOTIFICATION_ENV_FILE = 'notification/src/.env'
MATCHMAKING_ENV_FILE = 'matchmaking/src/.env'

USER_MANAGEMENT_POSTGRES_ENV_FILE = 'user_management/docker/postgres/.env'
USER_STATS_POSTGRES_ENV_FILE = 'user_stats/docker/postgres/.env'
TOURNAMENT_POSTGRES_ENV_FILE = 'tournament/docker/postgres/.env'
NOTIFICATION_POSTGRES_ENV_FILE = 'notification/docker/postgres/.env'

# add your env file here :P

env_files = [
    COMMON_ENV_FILE,
    USER_MANAGEMENT_ENV_FILE,
    USER_STATS_ENV_FILE,
    TOURNAMENT_ENV_FILE,
    GAME_CREATOR_ENV_FILE,
    NOTIFICATION_ENV_FILE,
    MATCHMAKING_ENV_FILE,

    # add your env file here :D
]

for env_file in env_files:
    try:
        os.remove(env_file)
    except FileNotFoundError:
        pass


def generate_key(name, key, env_path):
    if key is None:
        print(f'[WARNING]Key {name} is missing from the .env file.'
              f'\nCheck the .env_example file for more information.')
    with open(env_path, 'a') as f:
        f.write(f'{name}={key}\n')


def generate_database_credentials(microservice: str, host: str, env_path: str):
    microservice = microservice.replace('-', '_')
    db = f'{microservice}_db'
    user = f'{microservice}_user'
    password = os.urandom(32).hex()
    port = '5432'
    set_key('.env', f'{microservice.upper()}_DB_NAME', db)
    set_key('.env', f'{microservice.upper()}_DB_USER', user)
    set_key('.env', f'{microservice.upper()}_DB_PASSWORD', password)
    set_key('.env', f'{microservice.upper()}_DB_HOST', host)
    set_key('.env', f'{microservice.upper()}_DB_PORT', port)
    generate_key('POSTGRES_DB', db, env_path)
    generate_key('POSTGRES_USER', user, env_path)
    generate_key('POSTGRES_PASSWORD', password, env_path)
    generate_key('POSTGRES_HOST', host, env_path)
    generate_key('POSTGRES_PORT', port, env_path)


# common
generate_key('ACCESS_SERVICE_KEY', os.urandom(32).hex(), COMMON_ENV_FILE)
generate_key('BASE_DOMAIN', os.getenv('BASE_DOMAIN'), COMMON_ENV_FILE)

# user_management
generate_pair_of_keys.generate_pair_of_keys()
os.rename('public_access_jwt_key.pem', 'common/src/public_access_jwt_key.pem')
os.rename('private_access_jwt_key.pem', 'user_management/src/private_access_jwt_key.pem')
generate_key('REFRESH_KEY', os.urandom(32).hex(), USER_MANAGEMENT_ENV_FILE)
generate_key('USER_MANAGEMENT_SECRET_KEY', os.urandom(32).hex(), USER_MANAGEMENT_ENV_FILE)
generate_key('GITHUB_CLIENT_ID', os.getenv('GITHUB_CLIENT_ID'), USER_MANAGEMENT_ENV_FILE)
generate_key('GITHUB_CLIENT_SECRET', os.getenv('GITHUB_CLIENT_SECRET'), USER_MANAGEMENT_ENV_FILE)
generate_key('FT_API_CLIENT_ID', os.getenv('FT_API_CLIENT_ID'), USER_MANAGEMENT_ENV_FILE)
generate_key('FT_API_CLIENT_SECRET', os.getenv('FT_API_CLIENT_SECRET'), USER_MANAGEMENT_ENV_FILE)
generate_key('EMAIL_HOST_USER', os.getenv('EMAIL_HOST_USER'), USER_MANAGEMENT_ENV_FILE)
generate_key('EMAIL_HOST_PASSWORD', os.getenv('EMAIL_HOST_PASSWORD'), USER_MANAGEMENT_ENV_FILE)
generate_key('DEBUG', os.getenv('DEBUG'), USER_MANAGEMENT_ENV_FILE)
generate_database_credentials('user_management', 'user-management-db', USER_MANAGEMENT_ENV_FILE)

# user_stats
generate_key('USER_STATS_SECRET_KEY', os.urandom(32).hex(), USER_STATS_ENV_FILE)
generate_database_credentials('user_stats', 'user-stats-db', USER_STATS_ENV_FILE)

# tournament
generate_key('TOURNAMENT_SECRET_KEY', os.urandom(32).hex(), TOURNAMENT_ENV_FILE)
generate_database_credentials('tournament', 'tournament-db', TOURNAMENT_ENV_FILE)

# game_creator
generate_key('GAME_CREATOR_SECRET_KEY', os.urandom(32).hex(), GAME_CREATOR_ENV_FILE)

# notification
generate_key('NOTIFICATION_SECRET_KEY', os.urandom(32).hex(), NOTIFICATION_ENV_FILE)
generate_database_credentials('notification', 'notification-db', NOTIFICATION_ENV_FILE)

# matchmaking
generate_key('MATCHMAKING_SECRET_KEY', os.urandom(32).hex(), MATCHMAKING_ENV_FILE)

# add your key here ;)

print('.env files generated successfully')
