import sys
import threading
import requests
import traceback
import common.config as config
import common.utils as utils
import common.args as args
import common.path as path
import common.data as data
import common.assets as assets
import common.logger as Logger
import customtkinter as ctk
import webbrowser
import json

online = False
server_host = False

def start_server() -> None:
    if args.asArg("clear-data") and args.getArg("clear-data") in ["server", "all"]:
        data.clearServerData()
    data.createServerData()
    import server.main as Server
    Server.Main()

def start_client() -> None:
    global online
    if args.asArg("clear-data") and args.getArg("clear-data") in ["client", "all"]:
        data.clearClientData()
    data.createClientData()
    import client.main as Client
    config.setConfigParameter("client", "online", online)
    if not online and server_host:
        config.setConfigParameter("client", "server.host", server_host)

    Client.Main()

def start_local() -> None:
    server_thread = threading.Thread(target=start_server, name="ServerThread", daemon=True)
    client_thread = threading.Thread(target=start_client, name="ClientThread", daemon=True)
    server_thread.start()
    client_thread.start()
    client_thread.join()
    print("Le client a terminé.")

def load_saved_servers():
    try:
        with open(f"{path.get_path('data')}/saved_servers.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_server(ip):
    servers = load_saved_servers()
    if ip not in servers:
        servers.append(ip)
        with open(f"{path.get_path('data')}/saved_servers.json", "w") as file:
            json.dump(servers, file)

def ping_server(ip):
    try:
        res = requests.get(f"http://{ip}/api/client/info", timeout=2)
        return res.status_code == 200
    except requests.exceptions.RequestException:
        return False

def start_GUI():
    COLOR_PRIMARY = "#10B981"
    COLOR_SECONDARY = "#2563EB"
    COLOR_TEXT = "#2E2E2E"
    FONT_TITLE = ("Arial", 24)
    FONT_FOOTER = ("Arial", 10, "bold")
    BUTTON_HEIGHT = 50
    BUTTON_WIDTH = 200
    ENTRY_HEIGHT = 40
    ENTRY_WIDTH = 300
    FOOTER_HEIGHT = 50

    def on_connect_to_official_server():
        global server_host, online
        server_host = "play.elyon.younity-mc.fr"
        online = True
        app.destroy()
        start_client()

    def on_configure_server_click(saved_servers_inner_frame, status_label, ip_entry):
        global server_host, online
        ip = ip_entry.get()
        if ip:
            if ping_server(ip):
                server_host = ip
                online = False
                status_label.configure(text="Adresse IP valide!", text_color="green")
                ip_entry.delete(0, 'end')
                save_server(ip)
                update_saved_servers(saved_servers_inner_frame, status_label)
            else:
                status_label.configure(text="Le serveur n'est pas accessible.", text_color="red")
        else:
            status_label.configure(text="Veuillez entrer une adresse IP valide.", text_color="red")

    def on_connect_to_server(ip, status_label):
        global server_host, online
        if ping_server(ip):
            server_host = ip
            online = True
            app.destroy()
            start_client()
        else:
            status_label.configure(text="Le serveur n'est pas accessible.", text_color="red")

    def update_saved_servers(saved_servers_inner_frame, status_label):
        for widget in saved_servers_inner_frame.winfo_children():
            widget.destroy()
        servers = load_saved_servers()
        for server in servers:
            status = "En ligne" if ping_server(server) else "Hors ligne"
            server_frame = ctk.CTkFrame(saved_servers_inner_frame, fg_color="white")
            server_frame.grid(pady=2, sticky="ew")
            ctk.CTkLabel(server_frame, text=f"{server} - {status}", fg_color="white").grid(row=0, column=0, padx=5)
            if status == "En ligne":
                ctk.CTkButton(server_frame, text="Se connecter", command=lambda ip=server: on_connect_to_server(ip, status_label),
                              height=30, width=100, fg_color=COLOR_SECONDARY).grid(row=0, column=1, padx=5)

    def on_start_local():
        global online
        online = False
        app.destroy()
        start_local()

    def on_close():
        app.destroy()
        sys.exit()

    def open_website():
        webbrowser.open("https://elyon.younity-mc.fr")

    def Serveur_Officiel(tabview):
                # Official server tab
        ctk.CTkLabel(tab_official, text="Se connecter au serveur officiel", font=FONT_TITLE).grid(pady=10, row=0, column=1, sticky="e")
        ctk.CTkButton(tab_official, text="Se connecter", command=on_connect_to_official_server, font=FONT_TITLE,
                    height=BUTTON_HEIGHT, width=BUTTON_WIDTH, fg_color=COLOR_PRIMARY).grid(pady=20, row=1, column=1, sticky="e")

    def Serveur_Privat(tabview): 
        # Private servers tab
        ctk.CTkLabel(tab_private, text="Configurer un serveur privé", font=FONT_TITLE).grid(pady=2, row=0, column=0)
        ip_entry = ctk.CTkEntry(tab_private, placeholder_text="Entrez l'adresse IP du serveur",
                                height=ENTRY_HEIGHT, width=ENTRY_WIDTH)
        ip_entry.grid(pady=2, row=1, column=0)
        configure_button = ctk.CTkButton(tab_private, text="Ajouter", command=lambda : on_configure_server_click(saved_servers_inner_frame, status_label, ip_entry),
                                        height=BUTTON_HEIGHT, width=BUTTON_WIDTH, fg_color=COLOR_PRIMARY)
        configure_button.grid(pady=2, row=2, column=0)
        status_label = ctk.CTkLabel(tab_private, text="")
        status_label.grid(pady=(5, 5), row=3, column=0)

        saved_servers_frame = ctk.CTkFrame(tab_private, fg_color="white")
        saved_servers_frame.grid(pady=10, sticky="nsew", row=4, column=0)

        saved_servers_frame.grid_rowconfigure(0, weight=1)
        saved_servers_frame.grid_columnconfigure(0, weight=1)

        saved_servers_canvas = ctk.CTkCanvas(saved_servers_frame, bg="white")
        saved_servers_canvas.grid(sticky="nsew", row=0, column=0)

        scrollbar = ctk.CTkScrollbar(saved_servers_frame, command=saved_servers_canvas.yview)
        scrollbar.grid(sticky="ns", row=0, column=1)

        saved_servers_canvas.configure(yscrollcommand=scrollbar.set)
        saved_servers_canvas.bind('<Configure>', lambda e: saved_servers_canvas.configure(scrollregion=saved_servers_canvas.bbox("all")))

        saved_servers_inner_frame = ctk.CTkFrame(saved_servers_canvas, fg_color="white", bg_color="cyan")
        saved_servers_canvas.create_window((0, 0), window=saved_servers_inner_frame, anchor="nw")

        update_saved_servers(saved_servers_inner_frame, status_label)

        ctk.CTkButton(tab_private, text="Actualiser", command=lambda: update_saved_servers(saved_servers_inner_frame, status_label),
                    height=BUTTON_HEIGHT, width=BUTTON_WIDTH, fg_color=COLOR_PRIMARY).grid(pady=10, row=5, column=0)

    app = ctk.CTk()
    
    def Offline(tabview):
        # Offline mode tab
        ctk.CTkLabel(tab_offline, text="Jouer en mode hors ligne", font=FONT_TITLE).grid(pady=10, row=0, column=0)
        ctk.CTkButton(tab_offline, text="Démarrer", command=on_start_local,
                    height=BUTTON_HEIGHT, width=BUTTON_WIDTH, fg_color=COLOR_PRIMARY).grid(pady=20, row=1, column=0)

    def footer():
        footer_frame = ctk.CTkFrame(app, fg_color=COLOR_PRIMARY, height=FOOTER_HEIGHT)
        footer_frame.grid(sticky="ew", row=2, column=0, columnspan=20)

        footer_frame.grid_columnconfigure(0, weight=1)  # Left side of the footer
        footer_frame.grid_columnconfigure(1, weight=0)  # Right side of the footer

        ctk.CTkLabel(footer_frame, text="© 2024 Elyon Games. Tous droits réservés.",
                    font=FONT_FOOTER, text_color=COLOR_TEXT).grid(padx=5, pady=0, row=0, column=0, sticky="w")

        ctk.CTkButton(footer_frame, text="Site Web", command=open_website,
                    height=30, width=80, fg_color=COLOR_SECONDARY).grid(padx=5, pady=0, row=0, column=1, sticky="e")


    app.title("Elyon Games Launcher")
    app.geometry("600x500")
    app.iconbitmap(assets.getAsset("/logo/round.ico"))
    app.protocol("WM_DELETE_WINDOW", on_close)
    app.resizable(True, True)
    ctk.set_appearance_mode("dark")

    ctk.CTkLabel(app, text="Bienvenue sur Elyon Games Launcher", font=("Arial", 28, "bold")).grid(pady=5, row=0, column=0, columnspan=20)

    # Configure main grid for dynamic resizing
    app.grid_rowconfigure(1, weight=1)
    for i in range(20):
        app.grid_columnconfigure(i, weight=1)

    tabview = ctk.CTkTabview(app)
    tabview.grid(sticky="nsew", padx=10, row=1, column=0, columnspan=20)


    tab_official = tabview.add("Serveur Officiel")
    tab_private = tabview.add("Serveurs Privés")
    tab_offline = tabview.add("Mode Offline")

    Serveur_Officiel(tab_official)

    Serveur_Privat(tab_private)

    Offline(tab_offline)

    footer()

    return app

if __name__ == "__main__":
    app = start_GUI()
    app.mainloop()
