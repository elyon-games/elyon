import common.utils as utils
import common.path as path
import os
import json

class File:
    def __init__(self, id, path: str = None, default: dict = {}):
        self.id = id
        self.data = {}
        if path:
            self.Init(path, default)
    
    def Init(self, path: str, default: dict) -> None:
        self.path = utils.joinPath(path, f"{self.id}.json")
        if not self.existsData():
            self.data = default
            self.saveData()

    def setData(self, data: dict) -> None:
        self.data = data

    def addData(self, key: str, value) -> None:
        self.data[key] = value
    
    def updateData(self, key: str, value) -> None:
        self.data[key] = value

    def getData(self) -> dict:
        return self.data

    def existsData(self) -> bool:
        return os.path.exists(self.path)

    def saveData(self) -> None:
        with open(self.path, "w") as file:
            json.dump(self.data, file)

    def loadData(self) -> None:
        if not self.existsData():
            return
        with open(self.path, "r") as file:
            self.data = json.load(file)
    
    def removeData(self) -> None:
        os.remove(self.path)