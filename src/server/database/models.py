import uuid
from peewee import CharField
from server.database.db import BaseModel

class User(BaseModel):
    id = CharField(primary_key=True, max_length=50, unique=True, default=lambda: str(uuid.uuid4()))
    username = CharField(max_length=50)
    email = CharField(max_length=100, unique=True)

    def __str__(self):
        return self.username
