import requests
from client.lib.url import with_url_api

def ping() -> dict:
    print(with_url_api("/client/info"))
    res = requests.get(with_url_api("/client/info")).json()
    if res.get("error"):
        if res["error"] == True:
            return {"error": True}
    return res