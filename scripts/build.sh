#!/bin/bash

current_dir="$(dirname "$0")/../"
src_path="${current_dir}src/main.py"
assets_path="${current_dir}assets"
config_path="${current_dir}config"
public_server="${current_dir}src/server/public"

if [ -f "__main__.spec" ]; then
    rm "__main__.spec"
fi

if [ -f "dist/__main__.exe" ]; then
    rm "dist/__main__.exe"
fi

if [ -d "build" ]; then
    rm -rf "build"
fi

pyinstaller_path="$HOME/.local/bin/pyinstaller"

pyinstaller --add-data "$config_path:config" --add-data "$public_server:server_public_files" --add-data "$assets_path:assets" --onefile "$src_path" --icon="${assets_path}/logo/round.ico"

read -p "Press any key to continue..."