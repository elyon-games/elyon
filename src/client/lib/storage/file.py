import common.path as path
import os

class File:
    def __init__(self, id):
        self.id = id
        self.path = None
        self.data = None
    
    def Init(self, path, default) -> None:
        self.path = f"{path}/{self.id}.json"
        if not self.existsData():
            self.data = default
            self.saveData()

    def setData(self, data) -> None:
        self.data = data

    def getData(self):
        return self.data

    def existsData(self) -> bool:
        return os.path.exists(self.path)

    def saveData(self) -> None:
        with open(self.path, "w") as file:
            file.write(self.data)

    def loadData(self) -> None:
        if not self.existsData():
            return
        with open(self.path, "r") as file:
            self.data = file.read()
    
    def removeData(self) -> None:
        os.remove(self.path)