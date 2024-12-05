import json
from flask_session import Session as FlaskSession
import common.path as path
from server.database.models import ActivitySession as ActivitySessionModel

def initSessions(app, config, options):
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = path.get_path('server_sessions')
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_SECRET_KEY'] = config['secret']
    FlaskSession(app)

class ActivitySession:
    def __init__(self, user_id):
        self.session = ActivitySessionModel.create(user_id=user_id)
    
    def getID(self):
        return self.session.id
    
    def getUserID(self):
        return self.session.user

    def get(self, key):
        if self.session:
            value = self.session.data.get(key, None)
            return json.loads(value) if value else None
        return None
    
    def set(self, key, value):
        if self.session:
            self.session.data[key] = json.dumps(value)
            self.session.save()
    
    def delete(self, key):
        if self.session:
            del self.session.data[key]
            self.session.save()
    
    def clear(self):
        if self.session:
            self.session.data = {}
            self.session.save()
    
    def destroy(self):
        if self.session:
            self.session.delete_instance()
    
    def save(self):
        if self.session:
            self.session.save()