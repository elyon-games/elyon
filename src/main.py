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

def start_GUI() -> None:
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

    def on_configure_server_click():
        global server_host, online
        ip = ip_entry.get()
        if ip:
            if ping_server(ip):
                server_host = ip
                online = False
                status_label.configure(text="Adresse IP valide!", text_color="green")
                ip_entry.delete(0, 'end')
                save_server(ip)
                update_saved_servers()
            else:
                status_label.configure(text="Le serveur n'est pas accessible.", text_color="red")
        else:
            status_label.configure(text="Veuillez entrer une adresse IP valide.", text_color="red")

    def on_connect_to_server(ip):
        global server_host, online
        if ping_server(ip):
            server_host = ip
            online = True
            app.destroy()
            start_client()
        else:
            status_label.configure(text="Le serveur n'est pas accessible.", text_color="red")

    def update_saved_servers():
        for widget in saved_servers_inner_frame.winfo_children():
            widget.destroy()
        servers = load_saved_servers()
        for server in servers:
            status = "En ligne" if ping_server(server) else "Hors ligne"
            server_frame = ctk.CTkFrame(saved_servers_inner_frame, fg_color="white")
            server_frame.pack(pady=2, fill="x")
            ctk.CTkLabel(server_frame, text=f"{server} - {status}", fg_color="white").pack(side="left", padx=5)
            if status == "En ligne":
                ctk.CTkButton(server_frame, text="Se connecter", command=lambda ip=server: on_connect_to_server(ip),
                              height=30, width=100, fg_color=COLOR_SECONDARY).pack(side="right", padx=5)

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

    app = ctk.CTk()
    app.title("Elyon Games Launcher")
    app.geometry("400x500")
    app.iconbitmap(assets.getAsset("/logo/round.ico"))
    app.protocol("WM_DELETE_WINDOW", on_close)
    app.resizable(False, False)

    ctk.CTkLabel(app, text="Bienvenue sur Elyon Games Launcher", font=("Arial", 28, "bold")).pack(pady=5)

    tabview = ctk.CTkTabview(app)
    tabview.pack(expand=True, fill="both", padx=10)

    tab_official = tabview.add("Serveur Officiel")
    ctk.CTkLabel(tab_official, text="Se connecter au serveur officiel", font=FONT_TITLE).pack(pady=10)
    ctk.CTkButton(tab_official, text="Se connecter", command=on_connect_to_official_server, font=FONT_TITLE,
                  height=BUTTON_HEIGHT, width=BUTTON_WIDTH, fg_color=COLOR_PRIMARY).pack(pady=20)

    tab_private = tabview.add("Serveurs Privés")
    ctk.CTkLabel(tab_private, text="Configurer un serveur privé", font=FONT_TITLE).pack(pady=2)
    ip_entry = ctk.CTkEntry(tab_private, placeholder_text="Entrez l'adresse IP du serveur",
                            height=ENTRY_HEIGHT, width=ENTRY_WIDTH)
    ip_entry.pack(pady=2)
    configure_button = ctk.CTkButton(tab_private, text="Ajouter", command=on_configure_server_click,
                                     height=BUTTON_HEIGHT, width=BUTTON_WIDTH, fg_color=COLOR_PRIMARY)
    configure_button.pack(pady=2)
    status_label = ctk.CTkLabel(tab_private, text="")
    status_label.pack(pady=(5, 5))

    saved_servers_frame = ctk.CTkFrame(tab_private, fg_color="white")
    saved_servers_frame.pack(pady=10, fill="both", expand=True)

    saved_servers_canvas = ctk.CTkCanvas(saved_servers_frame, bg="white")
    saved_servers_canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ctk.CTkScrollbar(saved_servers_frame, command=saved_servers_canvas.yview)
    scrollbar.pack(side="right", fill="y")

    saved_servers_canvas.configure(yscrollcommand=scrollbar.set)
    saved_servers_canvas.bind('<Configure>', lambda e: saved_servers_canvas.configure(scrollregion=saved_servers_canvas.bbox("all")))

    saved_servers_inner_frame = ctk.CTkFrame(saved_servers_canvas, fg_color="white", bg_color="cyan")
    saved_servers_canvas.create_window((0, 0), window=saved_servers_inner_frame, anchor="nw")

    update_saved_servers()

    ctk.CTkButton(tab_private, text="Actualiser", command=update_saved_servers,
                  height=BUTTON_HEIGHT, width=BUTTON_WIDTH, fg_color=COLOR_PRIMARY).pack(pady=10)

    tab_offline = tabview.add("Mode Offline")
    ctk.CTkLabel(tab_offline, text="Jouer en mode hors ligne", font=FONT_TITLE).pack(pady=10)
    ctk.CTkButton(tab_offline, text="Démarrer", command=on_start_local,
                  height=BUTTON_HEIGHT, width=BUTTON_WIDTH, fg_color=COLOR_PRIMARY).pack(pady=20)

    footer_frame = ctk.CTkFrame(app, fg_color=COLOR_PRIMARY, height=FOOTER_HEIGHT)
    footer_frame.pack(side="bottom", fill="x")
    ctk.CTkLabel(footer_frame, text="© 2024 Elyon Games. Tous droits réservés.",
                 font=FONT_FOOTER, text_color=COLOR_TEXT).pack(side="left", padx=5)
    ctk.CTkButton(footer_frame, text="Site Web", command=open_website,
                  height=30, width=80, fg_color=COLOR_SECONDARY).pack(side="right", padx=2, pady=0)

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

        logger = Logger.LoggerManager(path.get_path("logs"))
        logger(f"Logger start")

        if utils.getDevModeStatus():
            print(f"Options : {options}")
        print(f"Mode : {mode}")
        print(f"Type : {type}")
        print(f"Config : {configMode}")

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
