import os

from dotenv import load_dotenv

load_dotenv()
# if this fail, relaunch the generate_env.py script (which will generate the pem keys)
COMMON_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH_TO_PEM = f'{COMMON_FOLDER}/src/public_access_jwt_key.pem'
ACCESS_PUBLIC_KEY = open(PATH_TO_PEM).read()
SERVICE_KEY = os.getenv('ACCESS_SERVICE_KEY')

ACCESS_ALGORITHM = 'RS256'
SERVICE_ACCESS_ALGORITHM = 'HS256'

SERVICE_EXPIRATION_TIME = 1

FRONT_URL = 'https://localhost/'
FRONT_ACTIVE_ACCOUNT_URL = f'{FRONT_URL}account/active/'

USER_MANAGEMENT_URL = 'https://user-management-nginx/'
FRIEND_STATUS_ENDPOINT = USER_MANAGEMENT_URL + 'user/friends/status/'

TOURNAMENT_URL = 'https://tournament-nginx/'
TOURNAMENT_ENDPOINT = TOURNAMENT_URL + 'tournament/'

USER_STATS_URL = 'https://user-stats-nginx/'
DEBUG_USER_STATS_URL = 'http://localhost:8001/'

USER_STATS_USER_ENDPOINT = USER_STATS_URL + 'statistics/user/'
DEBUG_USER_STATS_USER_ENDPOINT = DEBUG_USER_STATS_URL + 'statistics/user/'
USER_STATS_FRIENDS_ENDPOINT = '/friends/'

NOTIFICATION_URL = 'https://notification/'
USER_NOTIFICATION_ENDPOINT = NOTIFICATION_URL + 'notification/user/'
ADD_FRIEND_NOTIFICATION_ENDPOINT = NOTIFICATION_URL + 'notification/friend/add/'
DELETE_FRIEND_NOTIFICATION_ENDPOINT = NOTIFICATION_URL + 'notification/friend/delete/'

GAME_CREATOR_URL = 'https://pong-server-nginx/'
GAME_CREATOR_BASE_URL = GAME_CREATOR_URL + 'game_creator/'
GAME_CREATOR_CREATE_GAME_ENDPOINT = GAME_CREATOR_BASE_URL + 'create_game/'
GAME_CREATOR_CREATE_PRIVATE_GAME_ENDPOINT = GAME_CREATOR_BASE_URL + 'create_private_game/'
GAME_CREATOR_REMOVE_PLAYERS_CURRENT_GAME_ENDPOINT = (GAME_CREATOR_BASE_URL +
                                                     'remove_players_current_game/')

SSL_CERT_PATH = '/app/ssl/certificate.crt'
SSL_KEY_PATH = '/app/ssl/private.key'
