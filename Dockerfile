# Utiliser une image officielle Python
FROM python:3.11-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers nécessaires dans le conteneur
COPY . /app

# Mettre à jour pip
RUN pip install --no-cache-dir --upgrade pip

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port utilisé par Flask
EXPOSE 8080

# Commande pour démarrer l'application
CMD ["python", "app.py"]
