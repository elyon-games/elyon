from flask import Flask, request, jsonify
import os
import common.path
import common.utils
from server.database.db import db
from server.database.main import initDB
from server.database.models import User

initDB()
user = User.create(username='Alice', email='alice@example.com')
print(user)

db.close()

global app

def Main(config, options):
    global app
    print("Start Server...")
    app = Flask(f"Elyon Server ({__name__})", static_folder=common.path.get_path("server_public"), static_url_path = "/")
    initRoute()
    app.run(host=config["host"], port=config["port"])

def initRoute():
    global app

    @app.before_request
    def before_request():
        print("before_request")
        
    @app.route("/users", methods=["GET"])
    def get_users():
        users = User.select()
        users_list = [{"id": user.id, "username": user.username, "email": user.email} for user in users]
        return jsonify(users_list)