from server.database.db import db
from server.database.models import User

def initDB():
    db.connect()
    db.create_tables([User])