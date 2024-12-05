import os

def get_path(key: str = "default") -> str:
    paths = {
        "src": "./src",
        "config": "./config",
        "assets": "./assets",
        "data": "./data",
        "client": "./src/client",
        "client_data": "./data/client",
        "server": "./src/server",
        "server_data": "./data/server",
        "server_public": "./src/server/public",
        "server_files": "./data/server/files",
        "server_sessions": "./data/server/sessions",
    }
    return os.path.abspath(paths.get(key, "./"))