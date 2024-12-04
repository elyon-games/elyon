from peewee import CharField
from server.database.db import BaseModel

class User(BaseModel):
    username = CharField(max_length=50)
    email = CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
