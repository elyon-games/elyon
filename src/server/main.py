import os
import signal
import common.path
import common.process as process
from common.config import getConfig 
from common.args import getArgs
import server.services.clock as clock
from flask import Flask, session, request, jsonify, Response
from werkzeug.exceptions import HTTPException
from server.services.sessions import initSessions
from server.services.tokens import verify_jwt_token
from server.routes.api.main import route_api
from server.routes.web.main import route_web

app: Flask = None 

def Main():
    config = getConfig("server")
    options = getArgs()
    global app
    global threads
    print("Start Server...")
    
    app = Flask(
        f"Elyon Server ({__name__})",
        static_folder=common.path.get_path("server_public"),
        static_url_path="/",
        template_folder=common.path.get_path("server_templates")
    )
    
    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({
            "error": True,
            "message": "NO_FOUND",
            "code": 404
        }), 404

    @app.errorhandler(Exception)
    def error_handler(error: Exception) -> tuple[Response, int]:
        error = str(error)
        return jsonify({
            "error": True,
            "message": error if error else "Erreur interne du serveur (LOGIQUE)",
            "code": 500
        }), 500

    @app.errorhandler(500)
    def error_handler(error: HTTPException) -> tuple[Response, int]:
        return jsonify({
            "error": True,
            "message": "Erreur interne du serveur (WEB)",
            "code": 500
        }), 500

    initSessions(app=app)
    initRoute()

    all_files = [
        os.path.join(root, f)
        for root, dirs, files in os.walk(common.path.get_path("src"))
        for f in files
        if common.path.get_path("data") not in root
    ]


    process.create_process("server-web", run=lambda: app.run(host=config["host"], port=config["port"], debug=config["debug"], extra_files=all_files, threaded=False)).start()

    process.create_process("server-clock", run=lambda: clock.initClock()).start()

    process.started_callback("server-main")

    event_stop = process.get_process_running_event("server-web")
    event_stop.wait()
    # ajouter la gestions stop server
    os.kill(os.getpid(), signal.SIGINT)

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