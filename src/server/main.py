import common.path
from flask import Flask, session, request
from server.lib.sessions import initSessions, ActivitySession
from server.lib.token_service import initToken, verify_jwt_token
from server.database.main import initDB, initDefaultDB
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
    initSessions(app, config, options)
    initRoute()
    app.run(host=config["host"], port=config["port"])

def initRoute():
    global app
    
    @app.before_request
    def before_request():
        auth_header = request.headers.get('Authorization')
        activitySession
        if auth_header:
            token = auth_header.split(" ")[1]
            user_id = verify_jwt_token(token)
            if user_id:
                session['user_id'] = user_id
                if 'activitySession' not in session or session['activitySession'].user_id != user_id:
                    activitySession = ActivitySession(user_id)
                    session['activitySession'] = activitySession
                else:
                    activitySession = session['activitySession']


    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    app.register_blueprint(route_files)
    app.register_blueprint(route_auth)
    app.register_blueprint(route_users)
    app.register_blueprint(route_badges)