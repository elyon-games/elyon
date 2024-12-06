import os.path

global path_data
global paths

path_data = None
paths = {}
def initPath(path_data_t="./data") -> None:
    global path_data
    global paths
    path_data = path_data_t
    print("Path Data : ", path_data)
    paths = {
        # main code
        "src": "./src",
        "common": "./src/common",
        # data
        "data": path_data,
        # interne
        "config": "./config",
        "assets": "./assets",
        # logs
        "logs": os.path.join(path_data, "logs"),
        # client
        "client": "./src/client",
        "client_data": os.path.join(path_data, "client"),
        # server
        "server": "./src/server",
        "server_public": "./src/server/public",
        "server_templates": "./src/server/templates",
        "server_data": os.path.join(path_data, "server"),
        "server_database": os.path.join(path_data, "server/database"),
        "server_files": os.path.join(path_data, "server/files"),
        "server_sessions": os.path.join(path_data, "server/sessions")
    }
    
def get_path(key: str = "default") -> str:
    return os.path.abspath(paths.get(key, "./"))