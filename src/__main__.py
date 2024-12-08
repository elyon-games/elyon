import sys
import traceback
import threading
import requests
import common.config as config
import common.utils as utils
import common.args as args
import common.path as path
import common.data as data
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
    global online
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
    import customtkinter as ctk
    
    def on_client_click():
        app.destroy()
        start_client()

    def on_local_click():
        app.destroy()
        start_local()

    def on_configure_server_click():
        global server_host
        ip = ip_entry.get()
        if ip:
            try:
                res = requests.get(f"{ip}/api/client/info")
                if res.status_code == 200:
                    server_host = ip
                    status_label.configure(text="Adresse IP valide!", text_color="green")
                    connect_button.pack(pady=10)
                else:
                    status_label.configure(text="Le serveur n'est pas accessible.", text_color="red")
            except requests.exceptions.RequestException:
                status_label.configure(text="Erreur de connexion au serveur.", text_color="red")
        else:
            status_label.configure(text="Veuillez entrer une adresse IP valide.", text_color="red")

    def on_connect_click():
        app.destroy()
        start_client()

    def on_close():
        app.destroy()
        sys.exit()

    app = ctk.CTk()
    app.title("Elyon - Menu principal")
    app.geometry("400x400")
    app.protocol("WM_DELETE_WINDOW", on_close)

    title = ctk.CTkLabel(app, text="Bienvenue sur Elyon", font=("Arial", 30))
    title.pack(pady=5)
    
    subtitle_label = ctk.CTkLabel(app, text="Choisissez un mode", font=("Arial", 20))
    subtitle_label.pack(pady=5)

    client_button = ctk.CTkButton(app, text="Jouer Online", command=on_client_click)
    client_button.pack(pady=10)

    local_button = ctk.CTkButton(app, text="Jouer Offline", command=on_local_click)
    local_button.pack(pady=10)

    ip_label = ctk.CTkLabel(app, text="Adresse IP du serveur :")
    ip_label.pack(pady=(10, 5))

    ip_entry = ctk.CTkEntry(app, placeholder_text="Entrez l'adresse IP")
    ip_entry.pack(pady=5)

    configure_button = ctk.CTkButton(app, text="Configurer le serveur", command=on_configure_server_click)
    configure_button.pack(pady=10)

    status_label = ctk.CTkLabel(app, text="")
    status_label.pack(pady=(5, 5))

    connect_button = ctk.CTkButton(app, text="Connecter", command=on_connect_click)
    connect_button.pack_forget()  # Masquer initialement le bouton Connecter

    app.mainloop()

    sys.exit()

def Main() -> None:
    global options
    global mode
    global configMode
    global type
    global logger
    global online
    global server_host
    server_host = False
    online = False

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
        if type == "server":
            start_server()
        elif type == "client":
            online = True
            start_client()
        elif type == "local":
            online = False
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
