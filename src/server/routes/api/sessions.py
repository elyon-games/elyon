from flask import Blueprint, session, jsonify, request
from server.services.sessions import ActivitySession
from server.database.models import ActivitySession as ActivitySessionModel
from server.middleware.auth import login_required

route_sessions = Blueprint("sessions", __name__)

@route_sessions.route("/", methods=["POST"])
@login_required
def create():
    if 'user_id' in session and session["auth"] == True:
        activitySession = ActivitySession(session['user_id'])
        return jsonify({"id": activitySession.getID()})
    else:
        return jsonify({"error": "Authentification requise"}), 401

@route_sessions.route("/<id>", methods=["GET"])
@login_required
def get_by_id():
    id = request.view_args["id"]
    if 'user_id' in session and session["auth"] == True:
        activitySession = ActivitySessionModel.get_by_id(id)
        if session["user_id"] == activitySession.getUserID():
            return jsonify({"id": activitySession.getID(), "data": activitySession.getData()})
        else:
            return jsonify({"error": "Vous n'avez pas accès à cette session."}), 403
    else:
        return jsonify({"error": "Authentification requise"}), 401
    
