FROM python:3.12.0-bookworm

RUN mkdir /app

WORKDIR /app

RUN apt-get update && apt-get -y install cron

COPY config/cronjob /etc/cron.d/cronjob

COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt

RUN crontab /etc/cron.d/cronjob
