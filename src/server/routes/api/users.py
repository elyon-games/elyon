from flask import jsonify, Blueprint, request
from server.database.models import User, UserBadge
from server.middleware.auth import login_required

route_users = Blueprint("users", __name__)

@route_users.route("/", methods=["GET"])
def get_users():
    users = User.select()
    users_list = [{
        "id": user.id,
        "username": user.username,
        "bio": user.bio,
        "admin": user.admin,
        "avatar": user.avatar.path if user.avatar else None,
        "badges": [
            {
                "id": badge.badge.id,
                "name": badge.badge.name,
                "description": badge.badge.description
            } for badge in user.badges
        ]
    } for user in users]
    return jsonify(users_list)

@route_users.route("/me", methods=["GET"])
@login_required
def get_profile():
    user = User.get_by_id(request.user_id)
    if not user:
        return jsonify({"error": "Utilisateur non trouvé"}), 404
    return jsonify({
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "email": user.email,
        "money": user.money,
        "bio": user.bio,
    })

@route_users.route("/<user_id>/badges", methods=["GET"])
def get_user_badges(user_id):
    user = User.get_or_none(User.id == user_id)
    if not user:
        return jsonify({"error": "Utilisateur non trouvé"}), 404

    badges = [{
        "id": ub.badge.id,
        "name": ub.badge.name,
        "description": ub.badge.description
    } for ub in UserBadge.select().where(UserBadge.user == user)]

    if not badges:
        return jsonify({"message": "Cet utilisateur n'a aucun badge."}), 200