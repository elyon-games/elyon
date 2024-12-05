from flask import Flask, request, jsonify
import common.path
from server.lib.token_service import initToken
from server.database.db import db
from server.database.main import initDB, initDefaultDB
from server.database.models import Badge
from server.routes.files import route_files
from server.routes.auth import route_auth
from server.routes.users import route_users
from server.routes.badges import route_badges

global app

def Main(config, options):
    global app
    print("Start Server...")

    initDB()
    initDefaultDB()
    
    app = Flask(
        f"Elyon Server ({__name__})",
        static_folder=common.path.get_path("server_public"),
        static_url_path="/"
    )
    
    initToken(config)

    initRoute()
    app.run(host=config["host"], port=config["port"])

def initRoute():
    global app
    
    app.register_blueprint(route_files)
    app.register_blueprint(route_auth)
    app.register_blueprint(route_users)
    app.register_blueprint(route_badges)
