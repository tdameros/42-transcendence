FROM python:3.12.0-bookworm

# Créez le répertoire de travail et définissez-le comme répertoire de travail actuel
RUN mkdir /app
RUN mkdir -p /app/src/media/
WORKDIR /app

# Copiez le fichier requirements.txt dans le conteneur
COPY requirements.txt /app/

# Installez les dépendances
RUN pip install --no-cache-dir -r requirements.txt

COPY ./gunicorn/gunicorn.conf.py /app/gunicorn.conf.py
