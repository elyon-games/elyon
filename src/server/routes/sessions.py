from flask import Blueprint, session, jsonify

route_sessions = Blueprint("sessions", __name__)

@route_sessions.route("/activity/id", methods=["GET"])
def get_id():
    if 'activitySession' in session:
        return jsonify({"id": session['activitySession']})