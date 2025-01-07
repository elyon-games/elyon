import requests
from common.config import getConfig
from urllib.parse import urljoin

def ping():
    host = getConfig("client")["server"]["host"]
    if not host:
        return None
    return requests.get(urljoin("http://", host, "/api/client/info")).json()