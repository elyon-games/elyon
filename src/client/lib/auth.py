import requests

def login(username, password):
    response = requests.post('http://localhost:5000/login', json={
        'username': username,
        'password': password
    })
    return response.json()