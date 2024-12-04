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

def get_format_args():
    args = sys.argv[1:]
    return_args = {}
    current_key = None

    for arg in args:
        if arg.startswith("--"):
            current_key = arg[2:]
        elif current_key:
            return_args[current_key] = arg
            current_key = None

    return return_args