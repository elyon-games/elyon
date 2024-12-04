import os
import common.utils
import common.path

def createServerData() -> None:
    common.utils.create_folder_if_not_exists(common.path.get_path("server_data"))

def createClientData() -> None:
    common.utils.create_folder_if_not_exists(common.path.get_path("client_data"))

def createDataFolder() -> None:
    common.utils.create_folder_if_not_exists(common.path.get_path("data"))

def clearAllData():
    os.remove(common.path.get_path("data"))

def clearServerData():
    os.remove(common.path.get_path("server_data"))

def clearClientData():
    os.remove(common.path.get_path("client_data"))

