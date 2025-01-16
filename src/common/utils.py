import os
import sys

def create_file_if_not_exists(key: str, default: str) -> None:
    if not os.path.exists(key):
        with open(key, 'w') as file:
            file.write(default)

def create_folder_if_not_exists(folder: str) -> None:
    if not os.path.exists(folder):
        os.makedirs(folder)

def getDevModeStatus() -> bool:
    return "--dev" in sys.argv

def getMode() -> str:
    if getDevModeStatus():
        return "dev"
    return "prod"

def joinPath(path: str, *paths: str) -> str:
    return os.path.join(path, *paths)