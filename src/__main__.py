import common.config as config
import common.utils as utils
import common.args as args
import common.data as data

global options
options = args.get_format_args()

global mode
if options.get("config"):
    mode = options["config"]
else:
    mode = utils.getMode()

print("Starting Elyon...")
if utils.getDevModeStatus():
    print(f"Options : {options}")
    print(f"Mode : {mode}")


def start_server() -> None:
    import server.main as Server
    config_server = config.getConfig("server", mode)
    data.createServerData()
    Server.Main(config=config_server, options=options)

def start_client() -> None:
    import client.main as Client
    config_client = config.getConfig("client", mode)
    data.createClientData()
    Client.Main(config=config_client, options=options)

def start_local() -> None:
    start_server()
    start_client()

def Main() -> None:
    try:
        data.createDataFolder()
        if args.asArg("type"):
            type = args.getArg("type")
            if type == "server":
                start_server()
            elif type == "client":
                start_client()
            elif type == "local":
                start_local()
            else:
                raise ValueError("Type invalide. Veuillez choisir 'server', 'client' ou 'local'")
        else:
            start_client()
    except ValueError as e:
        print(f"Erreur : {e}")
    except IndexError:
        print("Erreur : L'argument '--type' doit être suivi d'une valeur (server, client, local)")
    except Exception as e:
        print(f"Une erreur imprévue est survenue : {e}")

if __name__ == "__main__":
    Main()
