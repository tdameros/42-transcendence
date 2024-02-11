FROM python:3.12.0-bookworm

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY gunicorn/gunicorn.conf.py /app/gunicorn.conf.py

COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh

ARG GAME_SERVER_PATH
ARG PONG_GAME_SERVERS_MIN_PORT
ARG PONG_GAME_SERVERS_MAX_PORT

ENV GAME_SERVER_PATH=${GAME_SERVER_PATH}
ENV PONG_GAME_SERVERS_MIN_PORT=${PONG_GAME_SERVERS_MIN_PORT}
ENV PONG_GAME_SERVERS_MAX_PORT=${PONG_GAME_SERVERS_MAX_PORT}
