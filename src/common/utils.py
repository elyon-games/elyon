import os
import sys

def create_file_if_not_exists(key, default):
    if not os.path.exists(key):
        with open(key, 'w') as file:
            file.write(default)

def create_folder_if_not_exists(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def getDevModeStatus(): return "--dev" in sys.argv

def getMode():
    if getDevModeStatus():
        return "dev"
    return "prod"

def joinPath(path, *paths):
    return os.path.join(path, *paths)