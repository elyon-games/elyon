import os
import sys
import re

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

def is_valid_ip(ip: str) -> bool:
    if not getDevModeStatus() and ip.endswith("elyon.younity-mc.fr"):
        return False

    ip_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    if ip_pattern.match(ip):
        return all(0 <= int(num) < 256 for num in ip.split("."))

    domain_pattern = re.compile(
        r"^(?:[a-zA-Z0-9]"
        r"(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)"
        r"+[a-zA-Z]{2,6}$"
    )
    return domain_pattern.match(ip) is not None

def file_exists(file: str) -> bool:
    return os.path.exists(file)