import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify

global configData

def initToken(config) -> None:
    global configData
    configData = config
    print("Token Service Initialized.")

def create_jwt_token(user_id):
    if not configData:
        raise Exception("Token service non initialisé.")
    if not user_id:
        raise Exception("ID utilisateur invalide.")
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(seconds=configData["jwt"]["expiresIn"]),
        "iat": datetime.now(timezone.utc),
    }
    token = jwt.encode(payload, configData["secret"], algorithm="HS256")
    return token

def verify_jwt_token(token):
    try:
        if not configData:
            raise Exception("Token service non initialisé.")
        if not token:
            raise Exception("Token invalide.")        
        payload = jwt.decode(token, configData["secret"], algorithms="HS256")
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        raise Exception("Le token a expiré.")
    except jwt.InvalidTokenError:
        raise Exception("Token invalide.")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"error": "Authentification requise"}), 401
        try:
            token = auth_header.split(" ")[1]
            user_id = verify_jwt_token(token)
            request.user_id = user_id
        except Exception as e:
            return jsonify({"error": str(e)}), 401
        return f(*args, **kwargs)
    return decorated_function
