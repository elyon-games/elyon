import requests
from client.lib.utils import with_url_api

def ping() -> dict:
    res: dict = requests.get(with_url_api("/client/info")).json()
    if res.get("error"):
        if res["error"] == True:
            return {"error": True}
    return res