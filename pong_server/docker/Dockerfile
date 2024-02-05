FROM python:3.12.0-bookworm

# Créez le répertoire de travail et définissez-le comme répertoire de travail actuel
RUN mkdir /app
WORKDIR /app

# Copiez le fichier requirements.txt dans le conteneur
COPY requirements.txt /app/

# Installez les dépendances
RUN pip install --no-cache-dir -r requirements.txt

RUN apt update -y && \
    apt upgrade -y && \
    apt install -y lsof && \
    rm -rf /var/lib/apt/lists/*

ARG PONG_GAME_CREATOR_PORT
ARG PONG_GAME_SERVERS_MIN_PORT
ARG PONG_GAME_SERVERS_MAX_PORT

ENV PONG_GAME_CREATOR_PORT=${PONG_GAME_CREATOR_PORT}
ENV PONG_GAME_SERVERS_MIN_PORT=${PONG_GAME_SERVERS_MIN_PORT}
ENV PONG_GAME_SERVERS_MAX_PORT=${PONG_GAME_SERVERS_MAX_PORT}
