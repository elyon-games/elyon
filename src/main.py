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

def start_server() -> None:
    if args.asArg("clear-data") and args.getArg("clear-data") in ["server", "all"]:
        data.clearServerData()
    data.createServerData()
    import server.main as Server
    config_server = config.getConfig("server", configMode)
    Server.Main(config=config_server, options=options)

def start_client() -> None:
    global server_host
    if args.asArg("clear-data") and args.getArg("clear-data") in ["client", "all"]:
        data.clearClientData()
    data.createClientData()        
    import client.main as Client
    config_client = config.getConfig("client", configMode)
    config_client.update({
        "online": online,
    })
    if not online and server_host is not False:
        config_client.update({
            "server": {
                "host": server_host,
            }
        })
    Client.Main(config=config_client, options=options)

def start_local() -> None:
    server_thread = threading.Thread(target=start_server, name="ServerThread", daemon=True)
    client_thread = threading.Thread(target=start_client, name="ClientThread", daemon=True)

    server_thread.start()
    client_thread.start()

    client_thread.join()
    print("Le client a terminé.")

def start_GUI() -> None:
    COLOR_PRIMARY = "#10B981"
    COLOR_SECONDARY = "#2563EB"
    COLOR_TEXT = "#2E2E2E"
    FONT_TITLE = ("Arial", 16)
    FONT_FOOTER = ("Arial", 10, "bold")
    BUTTON_HEIGHT = 50
    BUTTON_WIDTH = 200
    ENTRY_HEIGHT = 40
    ENTRY_WIDTH = 300
    FOOTER_HEIGHT = 50

    import sys
    import customtkinter as ctk

    def on_configure_server_click():
        global server_host
        global online
        ip = ip_entry.get()
        if ip:
            try:
                res = requests.get(f"{ip}/api/client/info")
                if res.status_code == 200:
                    server_host = ip
                    online = False
                    status_label.configure(text="Adresse IP valide!", text_color="green")
                    ip_entry.pack_forget()
                    configure_button.configure(text="Se connecter", command=on_start_client)
                else:
                    status_label.configure(text="Le serveur n'est pas accessible.", text_color="red")
            except requests.exceptions.RequestException:
                status_label.configure(text="Erreur de connexion au serveur.", text_color="red")
        else:
            status_label.configure(text="Veuillez entrer une adresse IP valide.", text_color="red")

    def on_start_client():
        global online
        online = True
        app.destroy()
        start_client()

    def on_start_local():
        global online
        online = False
        app.destroy()
        start_local()

    def on_close():
        app.destroy()
        sys.exit()

    def open_github():
        import webbrowser
        webbrowser.open("https://github.com/elyon-games/")

    def open_website():
        import webbrowser
        webbrowser.open("https://elyon.younity-mc.fr")

    app = ctk.CTk()
    app.title("Elyon - Menu principal")
    app.geometry("400x300")
    app.iconbitmap(assets.getAsset("/logo/round.ico"))
    app.protocol("WM_DELETE_WINDOW", on_close)
    app.resizable(False, False)

    ctk.CTkLabel(app, text="Bienvenue sur Elyon", font=("Arial", 20, "bold")).pack(pady=2)

    tabview = ctk.CTkTabview(app)
    tabview.pack(expand=True, fill="both", padx=10)

    tab_public = tabview.add("Serveur Public")
    public_label = ctk.CTkLabel(tab_public, text="Démarrer un serveur public", font=FONT_TITLE)
    public_label.pack(pady=10)
    public_button = ctk.CTkButton(
        tab_public, text="lancer", command=on_start_client, 
        font=FONT_TITLE,
        height=BUTTON_HEIGHT, width=BUTTON_WIDTH, fg_color=COLOR_PRIMARY
    )
    public_button.pack(pady=20)

    tab_private = tabview.add("Serveur Privé")
    private_label = ctk.CTkLabel(tab_private, text="Configurer le serveur privé", font=FONT_TITLE)
    private_label.pack(pady=2)

    ip_entry = ctk.CTkEntry(
        tab_private, placeholder_text="Entrez l'adresse IP du serveur", 
        height=ENTRY_HEIGHT, width=ENTRY_WIDTH
    )
    ip_entry.pack(pady=2)

    configure_button = ctk.CTkButton(
        tab_private, text="Configurer", command=on_configure_server_click, 
        height=BUTTON_HEIGHT, width=BUTTON_WIDTH, fg_color=COLOR_PRIMARY
    )
    configure_button.pack(pady=2)

    status_label = ctk.CTkLabel(tab_private, text="")
    status_label.pack(pady=(5, 5))

    tab_offline = tabview.add("Mode Offline")
    offline_label = ctk.CTkLabel(tab_offline, text="Jouer en mode hors ligne", font=FONT_TITLE)
    offline_label.pack(pady=10)
    offline_button = ctk.CTkButton(
        tab_offline, text="Démarrer", command=on_start_local, 
        height=BUTTON_HEIGHT, width=BUTTON_WIDTH, fg_color=COLOR_PRIMARY
    )
    offline_button.pack(pady=20)

    footer_frame = ctk.CTkFrame(app, fg_color=COLOR_PRIMARY, height=FOOTER_HEIGHT)
    footer_frame.pack(side="bottom", fill="x")

    copyright_label = ctk.CTkLabel(
        footer_frame, text="© 2024 Elyon Games. Tous droits réservés.", 
        font=FONT_FOOTER, text_color=COLOR_TEXT
    )
    copyright_label.pack(side="left", padx=10)

    github_icon = ctk.CTkButton(
        footer_frame, text="GitHub", command=open_github, 
        height=30, width=80, fg_color=COLOR_SECONDARY
    )
    github_icon.pack(side="right", padx=5, pady=5)

    website_icon = ctk.CTkButton(
        footer_frame, text="Site Web", command=open_website, 
        height=30, width=80, fg_color=COLOR_SECONDARY
    )
    website_icon.pack(side="right", padx=5, pady=5)

    app.mainloop()


def Main() -> None:
    global options
    global mode
    global configMode
    global type
    global logger
    global server_host

    server_host = False
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
