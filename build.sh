#!/bin/bash

# Chemins relatifs
current_dir=$(dirname "$0")
src_path="$current_dir/src/__main__.py"
assets_path="$current_dir/assets"
config_path="$current_dir/config"
public_server="$current_dir/src/server/public"

# Supprimer les fichiers et dossiers existants
rm -f __main__.spec
rm -f dist/__main__.exe
rm -rf build

# Définir le chemin vers pyinstaller
pyinstaller_path="$HOME/.local/bin/pyinstaller"

# Exécuter pyinstaller avec les options spécifiées
"$pyinstaller_path" --add-data "$config_path:config" --add-data "$public_server:server_public_files" --add-data "$assets_path:assets" --onefile "$src_path" --icon="$assets_path/logo/round.ico"
