import requests
import json

def login():
    try:
        vérif, data = json_existe()
        print(f"vérif : {vérif}, data : {data}")
        if vérif:
            connexion_auto(data)
        else:
            create_json("test", "test")
    except:
        # récupérer dans l'interface name et password 
        create_json("test", "test")


def create_account():
    print("create_account")

def json_existe() -> bool:
    try :
        with open("data.json", "r+")as file :
            data = json.load(file)
        if data["Name"] and data["Password"]:
            return True, data
        else:
            return False, 0
    except:
        return False, 0

def connexion_auto(data):
    print("connecter l'utilisateur")

def create_json(name, password):
    data = {"Name": name, "Password": password}
    with open("data.json", "w+")as file :
        json.dump(data, file)


login()