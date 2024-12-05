import common.path
from flask import Flask, session, request
from server.lib.sessions import initSessions, ActivitySession
from server.lib.token_service import initToken, verify_jwt_token
from server.database.main import initDB, initDefaultDB
from server.routes.files import route_files
from server.routes.auth import route_auth
from server.routes.users import route_users
from server.routes.badges import route_badges
from server.routes.sessions import route_sessions

global app

def Main(config, options):
    global app
    print("Start Server...")

    initDB()
    initDefaultDB(config=config)
    
    app = Flask(
        f"Elyon Server ({__name__})",
        static_folder=common.path.get_path("server_public"),
        static_url_path="/"
    )
    
    initToken(config=config)
    initSessions(app=app, config=config, options=options)
    initRoute()
    app.run(host=config["host"], port=config["port"])

def initRoute():
    global app
    
    @app.before_request
    def before_request():
        auth_header = request.headers.get('Authorization')
        activitySession = None
        if auth_header:
            token = auth_header.split(" ")[1]
            user_id = verify_jwt_token(token)
            if user_id:
                session['user_id'] = user_id
                session["auth"] = True
                if 'activitySession' not in session or (session['activitySession'] and session['activitySession'].getUserID() != user_id):
                    activitySession = ActivitySession(user_id)
                    session['activitySession'] = activitySession
                else:
                    activitySession = session['activitySession']
            else:
                session['user_id'] = None
                session['activitySession'] = None
        else:
            session['user_id'] = None
            session['activitySession'] = None
            session["auth"] = False

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    app.register_blueprint(route_files)
    app.register_blueprint(route_auth)
    app.register_blueprint(route_users)
    app.register_blueprint(route_badges)
    app.register_blueprint(route_sessions)