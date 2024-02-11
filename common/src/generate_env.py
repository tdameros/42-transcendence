import os

COMMON_ENV_FILE = 'common/src/.env'
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
# add your key here ;)
