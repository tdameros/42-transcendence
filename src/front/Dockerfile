FROM python:3.12.0-bullseye

# Créez le répertoire de travail et définissez-le comme répertoire de travail actuel
RUN mkdir /app
WORKDIR /app

# Copiez le fichier requirements.txt dans le conteneur
COPY requirements.txt /app/

# Installez les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copiez le reste des fichiers dans le conteneur
COPY . /app/

# Exposez le port 8000 pour que Gunicorn puisse l'utiliser
EXPOSE 8000