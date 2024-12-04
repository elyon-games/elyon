@echo off
chcp 65001 > nul

setlocal enabledelayedexpansion
set DEPENDENCIES_FILE=dependances.txt
set REQUIRED_LIBRARIES=
set INSTALL_COMMAND=pip install

for /f "tokens=*" %%i in (%DEPENDENCIES_FILE%) do (
    set LINE=%%i
    set LINE=!LINE:;= !
    set REQUIRED_LIBRARIES=!REQUIRED_LIBRARIES! !LINE!
    set INSTALL_COMMAND=!INSTALL_COMMAND! !LINE!
)

for %%a in (%*) do (
    if "%%a"=="--dependances-cmd" (
        echo !INSTALL_COMMAND!
        exit /b
    )
)

for %%I in (%REQUIRED_LIBRARIES%) do (
    pip show %%I > nul 2> nul
    echo Vérification en cours de %%I...
    if errorlevel 1 (
        echo %%I n'est pas installé. Installation en cours...
        pip install %%I
    ) else (
        echo %%I est déjà installé.
    )
)

python ./src %*
