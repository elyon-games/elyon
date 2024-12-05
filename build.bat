@echo off
setlocal enabledelayedexpansion
set "current_dir=%~dp0"
set "src_path=%current_dir%src/__main__.py"

if exist __main__.spec del __main__.spec
if exist dist\__main__.exe del dist\__main__.exe
if exist build rmdir /S /Q build

set "pyinstaller_path=%appdata%\Python\Python312\Scripts\pyinstaller.exe"

"%pyinstaller_path%" --onefile "%src_path%"

pause
