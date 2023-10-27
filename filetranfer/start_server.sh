#!/bin/bash

# Vérifier si pip3 est disponible
if which pip3 > /dev/null 2>&1; then
    PIP_COMMAND="pip3"
    PYTHON="python3"
elif which pip > /dev/null 2>&1; then
    PIP_COMMAND="pip"
    PYTHON="python"
else
    echo "Ni pip ni pip3 n'est installé sur ce système."
    exit 1
fi

echo "Utilisation de $PIP_COMMAND pour installer les dépendances."

# Chemin vers votre script Python
python_script="serveur.py"

# Chemin vers le fichier de configuration des dépendances
requirements_file="requirements.txt"

# Vérifiez si les dépendances sont déjà installées
if ! $PIP_COMMAND list | grep -F -x -q -f "$requirements_file"; then
    echo "Certaines ou toutes les dépendances ne sont pas installées. Installation en cours..."
    if ! $PIP_COMMAND install -r "$requirements_file"; then
        echo "Erreur lors de l'installation des dépendances. Vérifiez votre fichier de configuration."
        exit 1
    fi
else
    echo "Toutes les dépendances sont déjà installées."
fi

# Lancer votre serveur Python
$PYTHON "$python_script"
