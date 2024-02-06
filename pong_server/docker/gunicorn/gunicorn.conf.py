"""Gunicorn *production* config file"""

# Application to run
wsgi_app = 'game_creator.wsgi:application'

# Bind address and port
bind = '0.0.0.0:8000'

# Number of workers
workers = 4

chdir = 'src/game_creator'

daemon = False

keyfile = '/app/ssl/private.key'

certfile = '/app/ssl/certificate.crt'
