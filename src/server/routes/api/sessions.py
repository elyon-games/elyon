from flask import Blueprint, session, jsonify, request
from server.services.database.db import activitySession
from server.middleware.auth import login_required

route_sessions = Blueprint("sessions", __name__)