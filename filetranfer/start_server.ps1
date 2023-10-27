# Vérifier si pip3 est disponible
if (Test-Path -Path (Get-Command pip3 -ErrorAction SilentlyContinue)) {
    $PIP_COMMAND = "pip3"
    $PYTHON = "python3"
} elseif (Test-Path -Path (Get-Command pip -ErrorAction SilentlyContinue)) {
    $PIP_COMMAND = "pip"
    $PYTHON = "python"
} else {
    Write-Host "Ni pip ni pip3 n'est installé sur ce système."
    exit 1
}

Write-Host "Utilisation de $PIP_COMMAND pour installer les dépendances."

# Chemin vers votre script Python
$python_script = "serveur.py"

# Chemin vers le fichier de configuration des dépendances
$requirements_file = "requirements.txt"

# Vérifiez si les dépendances sont déjà installées
if (-not (Get-Content $requirements_file | Select-String -Pattern (Get-Content $requirements_file) -Quiet)) {
    Write-Host "Certaines ou toutes les dépendances ne sont pas installées. Installation en cours..."
    if (-not (& $PIP_COMMAND install -r $requirements_file)) {
        Write-Host "Erreur lors de l'installation des dépendances. Vérifiez votre fichier de configuration."
        exit 1
    }
} else {
    Write-Host "Toutes les dépendances sont déjà installées."
}

# Lancer votre serveur Python
& $PYTHON $python_script
