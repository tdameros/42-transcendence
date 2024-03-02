FROM python:3.12.0-bookworm

RUN mkdir /app
RUN mkdir -p /app/src/media/
WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY ./gunicorn/gunicorn.conf.py /app/gunicorn.conf.py
