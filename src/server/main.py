import os
import common.path
from common.config import getConfig 
from common.args import getArgs
from flask import Flask, session, request
from server.services.sessions import initSessions
from server.services.tokens import verify_jwt_token
from server.routes.api.main import route_api
from server.routes.web.main import route_web

global app

def Main():
    config = getConfig("server")
    options = getArgs()
    global app
    print("Start Server...")
    
    app = Flask(
        f"Elyon Server ({__name__})",
        static_folder=common.path.get_path("server_public"),
        static_url_path="/",
        template_folder=common.path.get_path("server_templates")
    )
    
    initSessions(app=app)
    initRoute()

    all_files = [
        os.path.join(root, f)
        for root, dirs, files in os.walk(common.path.get_path("src"))
        for f in files
        if common.path.get_path("data") not in root
    ]

    app.run(host=config["host"], port=config["port"], debug=config["debug"], extra_files=all_files, threaded=True)

def initRoute():
    global app
    
    @app.before_request
    def before_request():
        auth_header = request.headers.get('Authorization')
        session['user_id'] = None
        session["auth"] = False
        session["token"] = None
        session["iadmin"] = False

        if auth_header:
            token = auth_header.split(" ")[1]
            user_data = verify_jwt_token(token)
            if user_data:
                session['user_id'] = user_data["user_id"]
                session["auth"] = True
                session["token"] = token
                session["admin"] = user_data["admin"]

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("X-Powered-By", "Elyon-Server")
        return response

    app.register_blueprint(route_web)
    app.register_blueprint(route_api, url_prefix="/api")