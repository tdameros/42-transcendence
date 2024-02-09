import logging

DEBUG = False

if DEBUG:
    LOG_LEVEL = logging.DEBUG
else:
    LOG_LEVEL = logging.INFO

if DEBUG:
    USER_STATS_URL = 'http://localhost:8000/'
else:
    USER_STATS_URL = 'http://user-management-nginx/'

USER_STATS_USER_ENDPOINT = USER_STATS_URL + 'statistics/user/'

ACCESS_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAl88VVar5X6lAlHjj4o4r
r3WoAQloSNbxjgyUd6dU3z3a8JbLibihyl/LjrfAJXCT39FzBbjcWHw7dnDkBeU0
xX8pPNESkfJI7wxzkc1WcPk1KMwvy1dTaoCub7fZxNl2oOObdzTGpic8co7VOUqa
5cJks3MTL/8ipxaf4HVJ4luvcySvPflL1woWO3QfTomL/B/Xnu9fmj2ynn8DptfY
wJEe4eFA/jx+TP3coPBgs/XYG3stdyislm574U+5QvfRi1uii8jkFgpIxwUnxYbx
mZW+X8IdGmaUnucNeF1pLZjEIcr7MkzP3zm1auQww71DObGTPaLLJNjTPdP3rWYJ
mQIDAQAB
-----END PUBLIC KEY-----"""
DECODE_ALGORITHM = 'RS256'

THRESHOLD_TIME = 60
ELO_THRESHOLD = 1000
MATCHMAKING_PORT = 3000
MATCHMAKING_HOST = '0.0.0.0'
