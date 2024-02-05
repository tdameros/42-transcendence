FROM python:3.12.0-bookworm

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/

COPY gunicorn/gunicorn.conf.py /app/gunicorn.conf.py

RUN pip install --no-cache-dir -r requirements.txt
