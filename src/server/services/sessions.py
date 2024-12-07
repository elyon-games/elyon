from flask_session import Session as FlaskSession
import common.path as path
from server.database.db import activitySession
from server.services.config import configData

def initSessions(app):
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = path.get_path('server_sessions')
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_SECRET_KEY'] = configData['secret']
    FlaskSession(app)