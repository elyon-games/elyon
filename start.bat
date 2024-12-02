@echo off
chcp 65001 > nul

setlocal enabledelayedexpansion
set DEPENDENCIES_FILE=dependances.txt
set REQUIRED_LIBRARIES=
for /f "tokens=*" %%i in (%DEPENDENCIES_FILE%) do (
    set REQUIRED_LIBRARIES=!REQUIRED_LIBRARIES! %%i
)
for %%I in (%REQUIRED_LIBRARIES%) do (
    pip show %%I > nul 2> nul
    echo Vérification en cour de %%I...
    if errorlevel 1 (
        echo %%I n'est pas installé. Installation en cours...
        pip install %%I
    ) else (
        echo %%I est déjà installé.
    )
)
python ./src %*
