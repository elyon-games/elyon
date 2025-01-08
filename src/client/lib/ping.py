import requests
from client.lib.url import join_url

def ping() -> dict:
    return requests.get(join_url("/api/client/info")).json()