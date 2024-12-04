from flask import Flask, request
import os
import common.path
import common.utils
from server.database.db import db
from server.database.main import initDB

common.utils.create_folder_if_not_exists(common.path.get_path("server_data"))

initDB()
from server.database.models import User
user = User.create(name='Alice', email='alice@example.com')
print(user)

db.close()

global app

def Main(config, options):
    global app
    print("Start Server...")
    app = Flask(f"Elyon Server ({__name__})", static_folder=os.path.join(common.path.get_path("server"), "public"), static_url_path = "/")
    initRoute()
    app.run(host=config["host"], port=config["port"])

def initRoute():
    global app

    @app.before_request
    def before_request():
        print("before_request")
        
    @app.route("/")
    def test():
        return "sa"