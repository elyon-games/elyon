import requests
from client.lib.url import with_url_api

authData = {}

def login(username, password):
    response = requests.post(with_url_api("/auth/login"), json={
        'username': username,
        'password': password
    })
    print(response.json())
    return

def register(username, password):
    pass

def verify(token):
    pass