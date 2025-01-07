import requests
from common.config import getConfig
from urllib.parse import urljoin

def ping() -> dict:
    host = getConfig("client")["server"]["host"]
    if not host:
        return None
    url = urljoin(f"http://{host}", "/api/client/info")
    return requests.get(url).json()