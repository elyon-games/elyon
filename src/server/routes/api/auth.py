from flask import request, jsonify, Blueprint
from server.database.models import User
from werkzeug.security import check_password_hash, generate_password_hash
from server.services.tokens import create_jwt_token
from server.middleware.auth import login_required

route_auth = Blueprint("auth", __name__)

@route_auth.route("/login", methods=["POST"])
def login():
    data = request.json
    id = data.get("id")
    password = data.get("password")

    if not id or not password:
        return jsonify({"error": "Identifiant/Email et mot de passe sont requis"}), 400

    user = User.get_or_none((User.email == id) | (User.identifiant == id))
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Identifiants incorrects"}), 401

    return jsonify({"message": "Connexion réussie", "user_id": user.id, "username": user.username, "token": create_jwt_token(user.id)})

@route_auth.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    identifiant = data.get("identifiant")
    email = data.get("email")
    password = data.get("password")
    
    if not username:
        return jsonify({"error": "Le nom d'utilisateur est requis"}), 400
    if not identifiant:
        return jsonify({"error": "L'identifiant est requis"}), 400
    if not email:
        return jsonify({"error": "L'email est requis"}), 400
    if not password:
        return jsonify({"error": "Le mot de passe est requis"}), 400

    if User.select().where(User.email == email).exists():
        return jsonify({"error": "Cet email est déjà utilisé"}), 400

    if User.select().where(User.identifiant == identifiant).exists():
        return jsonify({"error": "Cet identifiant est déjà utilisé"}), 400

    hashed_password = generate_password_hash(password)
    user = User.create(username=username, identifiant=identifiant, email=email, password=hashed_password)
    return jsonify({"message": "Utilisateur créé avec succès", "user_id": user.id})

@route_auth.route("/verify", methods=["GET"])
@login_required
def verify():
    """Vérifie la validité du token."""
    return jsonify({"message": "Token valide", "user_id": request.user_id}), 200
