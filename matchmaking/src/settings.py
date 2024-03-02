import logging

DEBUG = False

APPEND_SLASH = False

if DEBUG:
    LOG_LEVEL = logging.DEBUG
else:
    LOG_LEVEL = logging.WARNING

if DEBUG:
    USER_STATS_URL = 'http://localhost:8000/'
else:
    USER_STATS_URL = 'http://user-stats-nginx/'

USER_STATS_USER_ENDPOINT = USER_STATS_URL + 'statistics/user/'

THRESHOLD_TIME = 60
ELO_THRESHOLD = 1000
MATCHMAKING_PORT = 3000
MATCHMAKING_HOST = '0.0.0.0'
