FROM python:3.12.0-bookworm

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt
