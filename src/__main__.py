import traceback
import threading
import common.config as config
import common.utils as utils
import common.args as args
import common.path as path
import common.data as data
import common.logger as Logger

global options
global mode
global configMode
global type
global logger

def start_server() -> None:
    if args.asArg("clear-data") and args.getArg("clear-data") in ["server", "all"]:
        data.clearServerData()
    data.createServerData()
    import server.main as Server
    config_server = config.getConfig("server", configMode)
    Server.Main(config=config_server, options=options)

def start_client() -> None:
    if args.asArg("clear-data") and args.getArg("clear-data") in ["client", "all"]:
        data.clearClientData()
    data.createClientData()
    import client.main as Client
    config_client = config.getConfig("client", configMode)
    Client.Main(config=config_client, options=options)

def start_local() -> None:
    server_thread = threading.Thread(target=start_server, name="ServerThread", daemon=True)
    client_thread = threading.Thread(target=start_client, name="ClientThread", daemon=True)

    server_thread.start()
    client_thread.start()

    client_thread.join()
    print("Le client a terminé.")

def Main() -> None:
    global options
    global mode
    global configMode
    global type
    global logger
    try:
        options = args.get_format_args()
        mode = utils.getMode()
        configMode = args.getArg("config") if args.asArg("config") else utils.getMode()
        type = args.getArg("type") if args.asArg("type") else "client"

        path.initPath(options.get("data-path") if options.get("data-path") else "./data")

        data.createDataFolder()

        logger = Logger.LoggerManager(path.get_path("logs"))
        logger(f"Logger start")

        if utils.getDevModeStatus():
            print(f"Options : {options}")
        print(f"Mode : {mode}")
        print(f"Type : {type}")
        print(f"Config : {configMode}")
        
        if type == "server":
            start_server()
        elif type == "client":
            start_client()
        elif type == "local":
            start_local()
        else:
            raise ValueError("Type invalide. Veuillez choisir 'server', 'client' ou 'local'")
    except ValueError as e:
        print(f"Erreur : {e}")
    except IndexError:
        print("Erreur : L'argument '--type' doit être suivi d'une valeur (server, client, local)")
    except Exception as e:
        print(f"Une erreur imprévue est survenue : {e}")
        traceback.print_exc()

if __name__ == "__main__":
    Main()
