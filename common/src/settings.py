import os

from dotenv import load_dotenv

load_dotenv()

ACCESS_PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAl88VVar5X6lAlHjj4o4r
r3WoAQloSNbxjgyUd6dU3z3a8JbLibihyl/LjrfAJXCT39FzBbjcWHw7dnDkBeU0
xX8pPNESkfJI7wxzkc1WcPk1KMwvy1dTaoCub7fZxNl2oOObdzTGpic8co7VOUqa
5cJks3MTL/8ipxaf4HVJ4luvcySvPflL1woWO3QfTomL/B/Xnu9fmj2ynn8DptfY
wJEe4eFA/jx+TP3coPBgs/XYG3stdyislm574U+5QvfRi1uii8jkFgpIxwUnxYbx
mZW+X8IdGmaUnucNeF1pLZjEIcr7MkzP3zm1auQww71DObGTPaLLJNjTPdP3rWYJ
mQIDAQAB
-----END PUBLIC KEY-----"""
SERVICE_KEY = os.getenv('ACCESS_SERVICE_KEY')

ACCESS_ALGORITHM = 'RS256'
SERVICE_ACCESS_ALGORITHM = 'HS256'

SERVICE_EXPIRATION_TIME = 1

FRONT_URL = 'https://localhost/'
FRONT_ACTIVE_ACCOUNT_URL = f'{FRONT_URL}account/active/'

USER_MANAGEMENT_URL = 'https://user-management-nginx/'
FRIEND_STATUS_ENDPOINT = USER_MANAGEMENT_URL + 'user/friends/status/'

TOURNAMENT_URL = 'https://tournament-nginx/'

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
GAME_CREATOR_CREATE_GAME_ENDPOINT = GAME_CREATOR_URL + 'create_game/'

SSL_CERT_PATH = '/app/ssl/certificate.crt'
SSL_KEY_PATH = '/app/ssl/private.key'
