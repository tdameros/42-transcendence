import os

# If you are not in prod, this script shall be called once from root.
# If the app is live, this script shall be called once from the makefile (generate_env rule).

# This script will generate keys in the .env file of your choice.
# Some .env files such as ACCESS_SERVICE_KEY are common so that multiple services can access them.
# Some other .env files such as USER_MANAGEMENT_SECRET_KEY are specific to a service,
# but should be generated here as well for consistency.

# This script shall also retrieve static keys needed for the app to work properly (such as 3rd party API keys).
# All of these keys shall be stored in a .env file located at the project root.
# An example of what this file should look like is provided in the .env.example file.

COMMON_ENV_FILE = 'common/src/.env'
USER_MANAGEMENT_ENV_FILE = 'user_management/src/.env'
# add your env file here :P

env_files = [
    COMMON_ENV_FILE,
    # add your env file here :D
]

for env_file in env_files:
    os.remove(env_file)


def generate_key(name, key, env_path):
    with open(env_path, 'a') as f:
        f.write(f'{name}={key}\n')


generate_key('ACCESS_SERVICE_KEY', os.urandom(32).hex(), COMMON_ENV_FILE)

# user_management
generate_key('USER_MANAGEMENT_SECRET_KEY', os.urandom(32).hex(), USER_MANAGEMENT_ENV_FILE)
generate_key('GITHUB_CLIENT_ID', os.getenv('GITHUB_CLIENT_ID'), USER_MANAGEMENT_ENV_FILE)
generate_key('GITHUB_CLIENT_SECRET', os.getenv('GITHUB_CLIENT_SECRET'), USER_MANAGEMENT_ENV_FILE)
generate_key('FT_API_CLIENT_ID', os.getenv('FT_API_CLIENT_ID'), USER_MANAGEMENT_ENV_FILE)
generate_key('FT_API_CLIENT_SECRET', os.getenv('FT_API_CLIENT_SECRET'), USER_MANAGEMENT_ENV_FILE)
generate_key('EMAIL_HOST_PASSWORD', os.getenv('EMAIL_HOST_PASSWORD'), USER_MANAGEMENT_ENV_FILE)
# add your key here ;)
