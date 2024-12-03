import sys
import common.config
import common.utils

global options
options = common.utils.get_format_args()

global mode
if options.get("config"):
    mode = options["config"]
else:
    mode = "dev" if common.utils.getDevModeStatus() else "prod"

print("Starting Elyon...")
if common.utils.getDevModeStatus():
    print(f"Options : {options}")
    print(f"Mode : {mode}")


def start_server() -> None:
    import server.main
    config_server = common.config.getConfig("server", mode)
    server.main.Main(config=config_server, options=options)

def start_client() -> None:
    import client.main
    config_client = common.config.getConfig("client", mode)
    client.main.Main(config=config_client, options=options)

def start_local() -> None:
    start_server()
    start_client()

def Main() -> None:
    try:
        if "--mode" in sys.argv:
            mode = sys.argv[sys.argv.index("--mode") + 1]
            if mode == "server":
                start_server()
            elif mode == "client":
                start_client()
            elif mode == "local":
                start_local()
            else:
                raise ValueError("Mode invalide. Veuillez choisir 'server', 'client' ou 'local'")
        else:
            start_client()
    except ValueError as e:
        print(f"Erreur : {e}")
    except IndexError:
        print("Erreur : L'argument '--mode' doit être suivi d'une valeur (server, client, local)")
    except Exception as e:
        print(f"Une erreur imprévue est survenue : {e}")

if __name__ == "__main__":
    Main()
