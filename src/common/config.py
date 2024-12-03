import yaml
import os
import sys
import common.path

path_all_config = common.path.get_path("config")

def openConfig(path):
    try:
        with open(path, "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Erreur : Le fichier {path} est introuvable.")
        sys.exit(1)
    except yaml.YAMLError as exc:
        print(f"Erreur lors de l'analyse du fichier YAML {path} : {exc}")
        sys.exit(1)
    except Exception as exc:
        print(f"Une erreur inattendue s'est produite lors de l'ouverture de {path} : {exc}")
        sys.exit(1)

try:
    common_config = openConfig(os.path.join(path_all_config, "common.yaml"))
except Exception as exc:
    common_config = {}
    print(f"Une erreur s'est produite lors du chargement de la configuration commune : {exc}")
    sys.exit(1)

def getConfig(app, mode):
    try:
        config = openConfig(os.path.join(path_all_config, f"{app}.yaml"))
        if config is None:
            raise ValueError(f"La configuration pour {app} est vide ou invalide.")
        final_config = config[mode].copy()
        if config.get("all"):
            final_config.update(config["all"])
        final_config.update(common_config)
        return final_config
    except KeyError:
        print(f"Erreur : La config '{mode}' n'existe pas dans la configuration pour {app}.")
        sys.exit(1)
    except ValueError as exc:
        print(exc)
        sys.exit(1)
    except Exception as exc:
        print(f"Une erreur inattendue s'est produite lors de l'obtention de la configuration pour {app} : {exc}")
        sys.exit(1)