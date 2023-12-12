FROM python:3.12.0-bookworm

# Créez le répertoire de travail et définissez-le comme répertoire de travail actuel
RUN mkdir /app
WORKDIR /app

# Copiez le fichier requirements.txt dans le conteneur
COPY requirements.txt /app/

# Installez les dépendances
RUN pip install --no-cache-dir -r requirements.txt
