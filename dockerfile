# Image de base
FROM python:3.9-slim

# Définition des variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=run.py
ENV FLASK_CONFIG=production

# Définition du répertoire de travail
WORKDIR /app

# Installation des dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copie des fichiers requirements
COPY requirements.txt /app/

# Installation des dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source de l'application
COPY app /app/app/
COPY config.py /app/
COPY run.py /app/

# Création et configuration des répertoires nécessaires
RUN mkdir -p /app/credentials /app/logs /app/app/static/maps
RUN chmod -R 755 /app/app/static/maps

# Configuration du volume pour les credentials
VOLUME /app/credentials
VOLUME /app/logs
VOLUME /app/app/static/maps

# Exposition du port
EXPOSE 5000

# Commande de démarrage
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "run:app"]
