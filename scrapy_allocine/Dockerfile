# Base Python
FROM python:3.11-slim

# Crée un répertoire pour le projet
WORKDIR /app

# Copie les fichiers du projet
COPY . /app

# Installe les dépendances
RUN pip install --no-cache-dir scrapy pymongo

# Commande par défaut pour le container
CMD ["scrapy", "crawl", "allocine_films"]
