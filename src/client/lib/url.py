from urllib.parse import urljoin
from common.config import getConfig

def join_url(*args: str) -> str:
    host = getConfig("client")["server"]["host"]
    if not host:
        return None
    return urljoin(f"http://{host}", *args)