from common.path import get_path
from client.lib.storage.file import File
from typing import Optional

clientDataPath = get_path("client_data")

storages: dict[str, File] = {}

def createStorage(id, default) -> File:
    if id not in storages:
        storages[id] = File(id)
        storages[id].Init(clientDataPath, default)
    return storages[id]

def getStorage(id) -> Optional[File]:
    if id in storages:
        return storages[id]
    return None

def removeStorage(id) -> None:
    if id in storages:
        storages[id].removeData()
        del storages[id]

def saveStorage(id) -> None:
    if id in storages:
        storages[id].saveData()

def loadStorage(id) -> None:
    if id in storages:
        storages[id].loadData()

def setStorageData(id, data) -> None:
    if id in storages:
        storages[id].setData(data)

def getStorageData(id) -> Optional[str]:
    if id in storages:
        return storages[id].getData()
    return None

def saveAllStorages() -> None:
    for storage in storages:
        storages[storage].saveData()