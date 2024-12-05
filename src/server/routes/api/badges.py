from flask import jsonify, Blueprint
from server.database.models import Badge

route_badges = Blueprint("badges", __name__)

@route_badges.route("/", methods=["GET"])
def get_badges():
    badges = Badge.select()
    badges_list = [{
        "id": badge.id,
        "name": badge.name,
        "description": badge.description
    } for badge in badges]
    return jsonify(badges_list)