import sys

def start_server() -> None:
    import server.main
    server.main.Main()

def start_client() -> None:
    import client.main
    client.main.Main()

def start_local() -> None:
    import server.main
    import client.main
    server.main.Main()
    client.main.Main()

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
