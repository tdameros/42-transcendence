FROM python:3.12.0-bookworm

# Créez le répertoire de travail et définissez-le comme répertoire de travail actuel
RUN mkdir /app
WORKDIR /app

# Copiez le fichier requirements.txt dans le conteneur
COPY requirements.txt /app/

# Copy the gunicorn config file
COPY gunicorn/gunicorn.conf.py /app/gunicorn.conf.py

# Installez les dépendances
RUN pip install --no-cache-dir -r requirements.txt

ARG PONG_GAME_APP_PATH
ARG PONG_GAME_SERVERS_MIN_PORT
ARG PONG_GAME_SERVERS_MAX_PORT

ENV PONG_GAME_APP_PATH=${PONG_GAME_APP_PATH}
ENV PONG_GAME_SERVERS_MIN_PORT=${PONG_GAME_SERVERS_MIN_PORT}
ENV PONG_GAME_SERVERS_MAX_PORT=${PONG_GAME_SERVERS_MAX_PORT}
