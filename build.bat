@echo off
setlocal enabledelayedexpansion
set "current_dir=%~dp0"
set "src_path=%current_dir%src/__main__.py"
set "assets_path=%current_dir%assets"
set "config_path=%current_dir%config"
set "pulic_server=%current_dir%src/server/public"


if exist __main__.spec del __main__.spec
if exist dist\__main__.exe del dist\__main__.exe
if exist build rmdir /S /Q build

set "pyinstaller_path=%appdata%\Python\Python312\Scripts\pyinstaller.exe"

"%pyinstaller_path%" --add-data "%config_path%:config" --add-data "%pulic_server%:server_public_files" --onefile "%src_path%" --noconsole --icon="%assets_path%\logo\round.ico"

pause
