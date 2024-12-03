import os

def get_path(key: str = "default") -> str:
    if key == "src":
        return os.path.abspath("./src")
    if key == "config":
        return os.path.abspath("./config")
    if key == "assets":
        return os.path.abspath("./assets")
    if key == "data":
        return os.path.abspath("./data")
    if key == "client":
        return os.path.abspath("./src/client")
    if key == "client_data":
        return os.path.abspath("./data/client")
    if key == "server":
        return os.path.abspath("./src/server")
    if key == "server_data":
        return os.path.abspath("./data/server")
    return os.path.abspath("./")