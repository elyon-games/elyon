#!/bin/bash

# Définir l'encodage (non nécessaire sous Linux, mais ajouté pour être compatible avec les scripts Windows)
export LANG=en_US.UTF-8

# Fichier des dépendances
DEPENDENCIES_FILE="dependances.txt"
REQUIRED_LIBRARIES=""
INSTALL_COMMAND="pip install"

# Lire chaque ligne du fichier dependances.txt
while IFS= read -r line; do
    line="${line//;/ }"  # Remplacer les ';' par des espaces
    REQUIRED_LIBRARIES="$REQUIRED_LIBRARIES $line"
    INSTALL_COMMAND="$INSTALL_COMMAND $line"
done < "$DEPENDENCIES_FILE"

# Gérer l'option --dependances-cmd
for arg in "$@"; do
    if [ "$arg" == "--dependances-cmd" ]; then
        echo "$INSTALL_COMMAND"
        exit 0
    fi
done

# Vérifier si les bibliothèques nécessaires sont installées, sinon les installer
for lib in $REQUIRED_LIBRARIES; do
    echo "Vérification en cours de $lib..."
    if ! pip show "$lib" > /dev/null 2>&1; then
        echo "$lib n'est pas installé. Installation en cours..."
        pip install "$lib"
    else
        echo "$lib est déjà installé."
    fi
done

# Exécuter le script Python
python ./src "$@"
