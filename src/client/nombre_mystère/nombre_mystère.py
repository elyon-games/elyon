import tkinter as tk
import requests
import sys
import os
import json
import time
import threading

#rajouez un bouton retour ou menu

#définition des constant
baseURL = "https://nsi.rgreenwolf.fr/mini-play/nombre"
token_file = f"{sys.argv[1]}.json" if len(sys.argv) > 1 else 'client.json'

def load_token():
    if os.path.exists(token_file):
        with open(token_file, 'r') as file:
            data = json.load(file)
            return data
    return None

def save_token(token, username):
    with open(token_file, 'w') as file:
        json.dump({'token': token, 'username': username}, file)

#définition des constant
try:
    token_client = load_token().get('token')
    data= load_token()
    print(token_client)
except:
    token_client=None
    data=None



#pour les Label "dynamyque"
def afficher_label(fenetre, text, relx, rely, font=("Arial", 12), fg="black", bg="#f0f0f0"):
    if relx==None and rely==None :
        label = tk.Label(fenetre, text=text, fg=fg, bg=bg, font=font)
        label.pack()
    else:
        label = tk.Label(fenetre, text=text, fg=fg, bg=bg, font=font)
        label.place(relx=relx, rely=rely, anchor="center")  # Le centre du label est positionné à relx, rely
        return label


# Fonction pour créer une partie
def create_party(fenetre, difficulty):
    difficulty =difficulty.get()
    try:
        int(difficulty)
    except:
        afficher_label(fenetre, "entrez un nombre", None, None)
        return
    res = requests.post(baseURL + "/party/create", json={'token' : token_client, "difficulty": difficulty})
    if res.status_code == 200 and res.json().get('status') != 'error':
        id = res.json().get('id')
        print(f"ID de la partie: {id}")
        afficher_label(fenetre,f"Tu es connecté et l'id est : {res.json().get(id)}", 0.5, 0.9, fg='green')
        fenetre.destroy()
        jeu_attente(id)
    else:
        afficher_label(fenetre,f"Erreur: {res.status_code}", None, None)


# Fonction pour rejoindre une partie
def join_party(fenetre, join):
    id = join.get()
    res = requests.post(baseURL + "/party/join", json={"token": token_client, "id": id})
    print(res.text)
    if res.status_code == 200 and res.json().get('status') != 'error':
        afficher_label(fenetre,"Tu es connecté", 0.5, 0.9, fg='green')
        fenetre.destroy()
        jeu_attente(id)
    else:
        afficher_label(fenetre, f"Erreur: {res.json()['message']} ({res.status_code})", None, None)

def check_ranking(fentre):
    res = requests.get(baseURL + "/rankings", params={"token": token_client, "id": id})
    if res.status_code==200:
        top = res.json().get("rankings")
        for joueur in top:
            for pseudo, victoires in joueur.items():
                afficher_label(fentre, f"{pseudo} : {victoires}", None, None)
        afficher_label(fentre,f"tu as le rang : {res.json().get("your_rank")}", None, None)


# Fonction pour envoyer le résultat
def envoyer_result(window, nombre, id):
    resultat = nombre.get()
    if resultat.isdigit():
        res = requests.post(baseURL + "/party/test", json={"id": id, "token": token_client, "num": int(resultat)})
        if res.status_code==200 and res.json().get("status")=="start":
            afficher_label(window, res.json()['message'], 0.5, 0.9, fg='#f32222')
        elif res.status_code==200 and res.json().get("status")=="end":
            afficher_label(window, "Bravo !", 0.5, 0.9, fg='green')
        else:
            afficher_label(window, "erreur", 0.5, 0.9, fg='green')
        player(window, id)
        
    else:
        afficher_label(window,"Tu es connecté", None, None, fg='green')

def player(window, id):
    #envoyer une requête pour avoir current_player
    print(id)
    res = requests.get(baseURL + "/party/status", json={'id': id, 'token' : token_client})
    print(res.status_code)
    afficher_label(window, f"a {res.json().get('current_player')} de jouer", 0.5, 0.7, font=("Arial", 14))

def requete_connexion(fenetre, entry_login, entry_mdp):
    login = entry_login.get()
    mdp = entry_mdp.get()
    res = requests.post(baseURL + "/auth/login", json={"username": login, "password": mdp})
    if res.json().get("status") == "success":
        token = res.json().get("token")
        save_token(token, login)
        connexion(fenetre)
        return token
    else:
        afficher_label(fenetre, f"Erreur : mot de passe ou pseudo invalide",0.5, 0.9)
        return None

def requete_register(window, entry_login, entry_mdp, vérif_mdp):
    login = entry_login.get()
    mdp = entry_mdp.get()
    ver_mdp = vérif_mdp.get()
    if vérif_equal(mdp, ver_mdp):
        print(f"login {login} ; mdp {mdp}")
    else :
        print("ce n'est pas égale")
        afficher_label(window, "ce n'est pas égal", 0.5, 0.9, fg='#f32222')
        

    res = requests.post(baseURL + "/auth/register", json={"username": login, "password": mdp})
    print("requète connexion faite ")
    if res.json().get("status") == "success":
        print("Inscription réussie !\nVous pouvez maintenant vous connecter.")
        res_co = requests.post(baseURL + "/auth/login", json={"username": login, "password": mdp})
        if res_co.json().get("status")=="sucess":
            print("connexion réussi")
        else:
            print("connéxion raté")
    else:
        print(f"Erreur lors de l'inscription : {res.json().get('message')}")
        return None

def vérif_equal(mdp, vérif):
    if mdp==vérif:
        return True
    else :
        return False

def window_close():
    return False

def requete_current(fenetre, id, good):
    while True:
        print("requete")
        print(token_client)
        res = requests.get(baseURL + "/party/status", params={'id': id, 'token' : token_client})
        print(f"le staus de la requète du status : {res.status_code}")
        try: 
            pending = f"le status : {res.json().get('status')}"
            print(pending)
        except: print("erreru sur la requète du statu print")
        try: 
            pending = res.json().get('status') =='start'
            print(pending)
        except: print("pending");pending = False
        if res.status_code==200 and pending:
            # good[0]=True
            fenetre.destroy()
            jeu(id)
            return
        else : 
            print("ca marche pas")
        time.sleep(1)

def page_ranking():
    window=tk.Tk()
    check_ranking(window)
    window.mainloop()

def jeu(id):
    print("on est bon")
    window = tk.Tk()
    window.title("Deviner le nombre")
    window.geometry("400x300")  # Taille de la fenêtre
    new_game_id_label = tk.Label(window, text=f"Nouvelle partie ID: {id}", bg="#f0f0f0", font=("Arial", 12))
    new_game_id_label.place(relx=0.7, rely=0.1, anchor="center")
    texte = tk.Label(window, text="Mettez le nombre :", font=("Arial", 14))
    texte.place(relx=0.5, rely=0.2, anchor="center")

    nombre = tk.Entry(window, font=("Arial", 12), bd=2, relief="solid")
    nombre.place(relx=0.5, rely=0.3, anchor="center")

    bouton_validez = tk.Button(window, text="Validez", command=lambda: envoyer_result(window, nombre, id),
                            font=("Arial", 12), bg="#4CAF50", fg="white", padx=20, pady=5)
    bouton_validez.place(relx=0.5, rely=0.5, anchor="center")

    player(window, id)
    import numpy as np
    import matplotlib.pyplot as plt

    # Créer les coordonnées pour dessiner un coeur
    t = np.linspace(0, 2 * np.pi, 1000)
    x = 16 * np.sin(t)**3
    y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)

    # Tracer le coeur
    plt.plot(x, y, color='red')
    plt.title('Coeur')
    plt.fill(x, y, 'red')
    plt.axis('equal')  # Maintient les proportions égales pour les axes
    plt.show()

    window.mainloop()


# Interface de jeu
def jeu_attente(id):
    print("on attend")
    res=[False]
    fenetre = tk.Tk()
    fenetre.geometry('200x200')
    thread = threading.Thread(target=requete_current, args=(fenetre, id, res))
    thread.daemon = True
    thread.start()
    afficher_label(fenetre, "en attente d'un autre joueur", 0.5, 0.4)
    afficher_label(fenetre, f"id :{id}", 0.5, 0.5)
    fenetre.mainloop()
    print("on est bon 1")
    

# Interface du connexion principal
def connexion(windows):
    windows.destroy()
    fenetre = tk.Tk()
    fenetre.title("Deviner le nombre")
    fenetre.geometry("400x500")  # Taille de la fenêtre
    fenetre.configure(bg="#f0f0f0")  # Couleur de fond

    afficher_label(fenetre, "entrez le max :", 0.5, 0.1)
    Entry_difficulty = tk.Entry(fenetre)
    Entry_difficulty.place(relx=0.5, rely=0.2, anchor='center')
    # Bouton pour commencer une nouvelle partie
    start = tk.Button(fenetre, text="Créer une nouvelle partie", command=lambda: create_party(fenetre, Entry_difficulty),
                      font=("Arial", 12), bg="#4CAF50", fg="white", padx=20, pady=5)
    start.place(relx=0.5, rely=0.3, anchor="center")

    
    id_label = tk.Label(fenetre, text="Entrez l'ID de la partie :", bg="#f0f0f0", font=("Arial", 14))
    id_label.place(relx=0.5, rely=0.5, anchor="center")
    join = tk.Entry(fenetre, font=("Arial", 12), bd=2, relief="solid")
    join.place(relx=0.5, rely=0.6, anchor="center")

    # Bouton pour rejoindre une partie
    button_join = tk.Button(fenetre, text="Rejoindre", command=lambda: join_party(fenetre, join),
                            font=("Arial", 12), bg="#2196F3", fg="white", padx=20, pady=5)
    button_join.place(relx=0.5, rely=0.7, anchor="center")

    use_other = tk.Button(fenetre, text="utiliser un autre compte", command=lambda:page_connexion(fenetre, False))
    use_other.place(relx=0.5, rely=0.8, anchor="center")
    ranking=tk.Button(fenetre, text="ranking", command=page_ranking)
    ranking.place(relx=0.8, rely=0.9)
    fenetre.mainloop()

def création_compte(windows):
    windows.destroy()
    fenetre=tk.Tk()
    fenetre.geometry('300x300')
    Label_login = tk.Label(fenetre, text="entrez votre pseudo  :")
    Label_login.place(relx=0.5, rely=0.1, anchor="center")
    entry_login = tk.Entry(fenetre)
    entry_login.place(relx=0.5, rely=0.2, anchor="center")

    Label_mdp = tk.Label(fenetre, text="entrez votre mot de passe :")
    Label_mdp.place(relx=0.5, rely=0.4, anchor="center")
    entry_mdp = tk.Entry(fenetre, show="*")
    entry_mdp.place(relx=0.5, rely=0.5, anchor="center")

    Label_mdp_vérif = tk.Label(fenetre, text="vérification de mot de passe :")
    Label_mdp_vérif.place(relx=0.5, rely=0.6, anchor="center")
    entry_mdp_vérif = tk.Entry(fenetre, show="*")
    entry_mdp_vérif.place(relx=0.5, rely=0.7, anchor="center")

    submit= tk.Button(fenetre, text="se connecter", command=lambda:requete_register(fenetre, entry_login, entry_mdp, entry_mdp_vérif))
    submit.place(relx=0.5, rely=0.8, anchor="center")


def page_connexion(windows, auto):
    res = requests.get(baseURL +"/auth/check_token", params={'token' : token_client})
    if res.status_code == 200 and res.json().get('status') =='success' and auto:
        connexion(windows)
    else:
        windows.destroy()
        fenetre=tk.Tk()
        fenetre.geometry('300x300')
        Label_login = tk.Label(fenetre, text="entrez votre pseudo  :")
        Label_login.place(relx=0.5, rely=0.1, anchor="center")
        entry_login = tk.Entry(fenetre)
        entry_login.place(relx=0.5, rely=0.2, anchor="center")

        Label_mdp = tk.Label(fenetre, text="entrez votre mot de passe :")
        Label_mdp.place(relx=0.5, rely=0.4, anchor="center")
        entry_mdp = tk.Entry(fenetre, show="*")
        entry_mdp.place(relx=0.5, rely=0.5, anchor="center")

        submit= tk.Button(fenetre, text="se connecter", command=lambda:requete_connexion(fenetre, entry_login, entry_mdp))
        submit.place(relx=0.5, rely=0.7, anchor="center")
        fenetre.mainloop()

#affiche le menu
def menu():
    fenetre=tk.Tk()
    fenetre.geometry("300x300")
    button_connecter= tk.Button(fenetre, text="se connecter", command=lambda :page_connexion(fenetre, True))
    button_connecter.pack()
    button_register= tk.Button(fenetre, text="créer un compte", command=lambda :création_compte(fenetre))
    button_register.pack()
    # button_connecter= tk.Button(fenetre, text="Anonyme", command=connexion)
    # button_connecter.pack()
    fenetre.mainloop()
menu()