import sys
import threading
import requests
import traceback
import common.process as process
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
from typing import List, Any, Dict

# Constante de l'interface graphique
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

# Variables globales
global server_host, online, mode, configMode, type, logger, options
online: bool = False
server_host: str = "127.0.0.3:3300"
mode: str = ""
configMode: str = ""
type: str = ""
logger: Logger.LoggerManager
options: Dict[str, Any]

def start_server() -> None:
    if args.asArg("clear-data") and args.getArg("clear-data") in ["server", "all"]:
        data.clearServerData()
    data.createServerData()
    config.setConfigParameter("server", "launchType", type)
    import server.main as Server
    process.create_process("server-main", Server.Main).start()

def start_client() -> None:
    global online, server_host
    if args.asArg("clear-data") and args.getArg("clear-data") in ["client", "all"]:
        data.clearClientData()
    data.createClientData()
    import client.main as Client
    config.setConfigParameter("client", "launchType", type)
    config.setConfigParameter("client", "online", online)
    print(f"Adresse du serveur : {server_host}")
    if server_host:
        config.setConfigParameter("client", "server_host", server_host)
    process.create_process("client-main", Client.Main).start()


def start_local() -> None:
    start_server()
    process.set_started_callback("server-main", start_client)

def open_website() -> None:
    webbrowser.open("https://elyon.younity-mc.fr")

def load_saved_servers() -> List[str]:
    try:
        with open(f"{path.get_path('data')}/saved_servers.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_server(ip: str) -> None:
    servers = load_saved_servers()
    if ip not in servers:
        servers.append(ip)
        with open(f"{path.get_path('data')}/saved_servers.json", "w") as file:
            json.dump(servers, file)

def ping_server(ip: str) -> bool:
    try:
        res = requests.get(f"http://{ip}/api/client/info")
        return res.status_code == 200
    except requests.exceptions.RequestException:
        return False

def start_GUI() -> None:
    def on_connect_to_official_server() -> None:
        global server_host, online, type
        server_host = "play.elyon.younity-mc.fr"
        online = True
        type = "client"
        app.destroy()
        start_client()

    def on_configure_server_click(saved_servers_inner_frame: ctk.CTkFrame, status_label: ctk.CTkLabel, ip_entry: ctk.CTkEntry) -> None:
        global server_host, online
        ip = ip_entry.get()
        if ip:
            if ping_server(ip):
                server_host = ip
                online = True
                status_label.configure(text="Adresse IP valide!", text_color="green")
                ip_entry.delete(0, 'end')
                save_server(ip)
                update_saved_servers(saved_servers_inner_frame, status_label)
            else:
                status_label.configure(text="Le serveur n'est pas accessible.", text_color="red")
        else:
            status_label.configure(text="Veuillez entrer une adresse IP valide.", text_color="red")

    def on_connect_to_server(ip: str, status_label: ctk.CTkLabel) -> None:
        global server_host, online, type
        if ping_server(ip):
            server_host = ip
            online = True
            type = "client"
            app.destroy()
            start_client()
        else:
            status_label.configure(text="Le serveur n'est pas accessible.", text_color="red")

    def update_saved_servers(saved_servers_inner_frame: ctk.CTkFrame, status_label: ctk.CTkLabel) -> None:
        for widget in saved_servers_inner_frame.winfo_children():
            widget.destroy()
        servers = load_saved_servers()
        for i, server in enumerate(servers[::-1]):
            status = "En ligne" if ping_server(server) else "Hors ligne"
            ctk.CTkLabel(saved_servers_inner_frame, text=f"{server} - {status}", fg_color="white", text_color="black").grid(row=i, column=0, padx=5)
            if status == "En ligne":
                ctk.CTkButton(saved_servers_inner_frame, text="Se connecter", command=lambda ip=server: on_connect_to_server(ip, status_label),
                              height=30, width=100, fg_color=COLOR_SECONDARY).grid(row=0, column=1, padx=5)

    def on_start_local() -> None:
        global online, type
        online = False
        type = "local"
        app.destroy()
        start_local()

    def on_close() -> None:
        app.destroy()
        sys.exit()

    def Serveur_Officiel(tabview: ctk.CTkTabview) -> None:
        for i in range(3):
            tabview.grid_columnconfigure(i, weight=1)
        ctk.CTkLabel(
            tabview, 
            text="Se connecter au serveur officiel", 
            font=FONT_TITLE
            ).grid(
                pady=10, 
                row=0, 
                column=1
            )
        ctk.CTkButton(
            tab_official, 
            text="Se connecter", 
            command=on_connect_to_official_server, 
            font=FONT_TITLE,
            height=BUTTON_HEIGHT, 
            width=BUTTON_WIDTH, 
            fg_color=COLOR_PRIMARY
            ).grid(
                pady=20, 
                row=1, 
                column=1
            )

    def Serveur_Privat(tabview: ctk.CTkTabview) -> None: 
        for i in range(3):
            tabview.grid_columnconfigure(i, weight=1)
        # Affichage prinipale 
        # Private servers tab
        ctk.CTkLabel(
            tabview, 
            text="Configurer un serveur privé", 
            font=FONT_TITLE
            ).grid(
                pady=2, 
                row=0, 
                column=1
            )
        
        ip_entry = ctk.CTkEntry(
            tabview, 
            placeholder_text="Entrez l'adresse IP du serveur",
            height=ENTRY_HEIGHT, 
            width=ENTRY_WIDTH
            )
        ip_entry.grid(
                pady=2, 
                row=1, 
                column=1
            )
        
        ctk.CTkButton(
            tabview, 
            text="Ajouter", 
            command=lambda: on_configure_server_click(saved_servers_inner_frame, status_label, ip_entry),
            font=FONT_TITLE,
            height=BUTTON_HEIGHT, 
            width=BUTTON_WIDTH, 
            fg_color=COLOR_PRIMARY
            ).grid(
                pady=2, 
                row=2, 
                column=1
            )
        status_label = ctk.CTkLabel(
            tabview, 
            text=""
            )
        status_label.grid(
                pady=(5, 5), 
                row=3, 
                column=1
            )

        # Affichage des serveurs sauvegardés
        saved_servers_frame = ctk.CTkFrame(
            tabview, 
            fg_color="white"
        )
        saved_servers_frame.grid(
                pady=10, 
                row=4, 
                sticky="ew",
                columnspan=3
            )

        for i in range(2):
            saved_servers_frame.grid_columnconfigure(i, weight=1)

        saved_servers_canvas = ctk.CTkCanvas(
            saved_servers_frame, 
            bg="white"
        )
        saved_servers_canvas.grid(row=0, column=0, sticky="nsew")

        scrollbar = ctk.CTkScrollbar(
            saved_servers_frame, 
            command=saved_servers_canvas.yview
        )
        scrollbar.grid(
            row=0, 
            column=1, 
            sticky="nes"
        )

        saved_servers_canvas.configure(yscrollcommand=scrollbar.set)
        saved_servers_canvas.bind(
            '<Configure>', 
            lambda e: saved_servers_canvas.configure(scrollregion=saved_servers_canvas.bbox("all"))
            )

        saved_servers_inner_frame = ctk.CTkFrame(
            saved_servers_canvas,
            fg_color="white",
            border_width=0
        )
        saved_servers_canvas.create_window((0, 0), window=saved_servers_inner_frame, anchor="nw")

        update_saved_servers(saved_servers_inner_frame, status_label)

        # Retour à la manipulation de l'interface graphique
        ctk.CTkButton(
            tabview, 
            text="Actualiser", 
            command=lambda: update_saved_servers(saved_servers_inner_frame, status_label),
            height=BUTTON_HEIGHT, 
            width=BUTTON_WIDTH, 
            fg_color=COLOR_PRIMARY
            ).grid(
                pady=10, 
                row=5, 
                column=1
            )
    
    def Offline(tabview: ctk.CTkTabview) -> None:
        for i in range(3):
            tabview.grid_columnconfigure(i, weight=1)
        # Offline mode tab
        ctk.CTkLabel(
            tabview, 
            text="Jouer en mode hors ligne", 
            font=FONT_TITLE
            ).grid(
                pady=10, 
                row=0, 
                column=1
            )
        ctk.CTkButton(
            tab_offline, 
            text="Démarrer", 
            command=on_start_local,
            font=FONT_TITLE,
            height=BUTTON_HEIGHT, 
            width=BUTTON_WIDTH, 
            fg_color=COLOR_PRIMARY
            ).grid(
                pady=20, 
                row=1, 
                column=1
            )

    def footer() -> None:
        footer_frame = ctk.CTkFrame(
            app, 
            fg_color=COLOR_PRIMARY, 
            height=FOOTER_HEIGHT
        )
        footer_frame.grid(
            sticky="ew", 
            row=2, 
            column=0, 
            columnspan=20
        )

        footer_frame.grid_columnconfigure(0, weight=1)
        footer_frame.grid_columnconfigure(1, weight=0)

        footer_label = ctk.CTkLabel(
            footer_frame, 
            text="© 2024 Elyon Games. Tous droits réservés.",
            font=FONT_FOOTER, 
            text_color=COLOR_TEXT
        )
        footer_label.grid(
            padx=5, 
            pady=0, 
            row=0, 
            column=0, 
            sticky="w"
        )
        footer_label.bind("<Button-1>", lambda e: open_website())

    app = ctk.CTk()
    app.title("Elyon Games Launcher")
    app.geometry("600x500")
    app.iconbitmap(assets.getAsset("/logo/round.ico"))
    app.protocol("WM_DELETE_WINDOW", on_close)
    app.resizable(False, False)
    ctk.set_appearance_mode("dark")

    ctk.CTkLabel(app, text="Bienvenue sur Elyon Games Launcher", font=("Arial", 28, "bold")).grid(pady=5, row=0, column=0, columnspan=20)

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

    print("Lancement de l'interface graphique...")
    app.mainloop()

def Main() -> None:
    global options, mode, configMode, type, logger, server_host, online

    try:
        options = args.get_format_args()
        mode = utils.getMode()
        configMode = args.getArg("config") if args.asArg("config") else utils.getMode()
        type = args.getArg("type") if args.asArg("type") else "gui"


        path.initPath(options.get("data-path") if options.get("data-path") else "./data")
        data.createDataFolder()


        disabledConsoleLogger = args.asArg("disable-console-logger") or False
        logger = Logger.LoggerManager(path.get_path("logs"), disabledConsoleLogger)
        logger(f"Logger start")

        if utils.getDevModeStatus():
            print(f"Options : {options}")
        print(f"Mode : {mode}")
        print(f"Type : {type}")
        print(f"Config : {configMode}")

        server_host = args.getArg("server-host") if args.asArg("server-host") else server_host

        if type == "gui":
            start_GUI()
        elif type == "server":
            start_server()
        elif type == "client":
            start_client()
        elif type == "local":
            start_local()
        else:
            raise ValueError("Type invalide. Veuillez choisir 'server', 'client', 'local' ou 'gui'")
    except ValueError as e:
        print(f"Erreur : {e}")
    except IndexError:
        print("Erreur : L'argument '--type' doit être suivi d'une valeur (server, client, local, gui)")
    except Exception as e:
        print(f"Une erreur imprévue est survenue : {e}")
        traceback.print_exc()

if __name__ == "__main__":
    Main()
