from urllib.parse import urljoin
from common.config import getConfig
from client.var import auth as authData
import requests

host: str = getConfig("client")["server"]["host"]

def is_https_supported(host: str) -> bool:
    try:
        response = requests.get(f"https://{host}", timeout=2)
        return response.status_code == 200
    except requests.RequestException:
        return False
    
scheme = "https" if is_https_supported(host) else "http"

def get_api_url() -> str:
    if not host:
        return None
    return f"{scheme}://{host}/api"

def with_url_api(url: str) -> str:
    return f"{get_api_url()}{url}"

def getHeadersWithToken(headers={}, token:str=""):
    headers["Authorization"] = f"Bearer {authData['token'] if not token else token}"
    return headers

def isOfficielServer():
    return host.split(":")[0].endswith("elyon.younity-mc.fr")