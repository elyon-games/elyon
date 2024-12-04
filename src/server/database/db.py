from peewee import SqliteDatabase, Model
import common.path
import os.path
import common.utils

db = SqliteDatabase(os.path.join(common.path.get_path("server_data"), f"{common.utils.getMode()}.sqlite3"))

class BaseModel(Model):
    class Meta:
        database = db