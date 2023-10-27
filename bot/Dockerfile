# syntax=docker/dockerfile:1

# Utilisez une image Python de base
ARG PYTHON_VERSION=3.9.6
FROM python:${PYTHON_VERSION}-slim as base

# Empêche Python d'écrire des fichiers pyc.
ENV PYTHONDONTWRITEBYTECODE=1

# Empêche Python de mettre en mémoire tampon stdout et stderr.
ENV PYTHONUNBUFFERED=1

# Répertoire de travail de l'application
WORKDIR /app

# Créez un utilisateur non privilégié pour exécuter l'application.
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Installez les dépendances Python en utilisant le fichier requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Passez à l'utilisateur non privilégié pour exécuter l'application.
USER appuser

# Copiez le code source de l'application dans le conteneur.
COPY . .

# Exposez le port sur lequel l'application écoute (si nécessaire).
# EXPOSE 8000

# Exécutez l'application.
CMD python my_bot_discord.py
