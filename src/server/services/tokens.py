import jwt
from datetime import datetime, timedelta, timezone
from server.database.db import users as User
from server.services.config import configData

def create_jwt_token(user_id):
    if not configData:
        raise Exception("Token service non initialisé.")
    if not user_id:
        raise Exception("ID utilisateur invalide.")
    userData = User.get_by_id(user_id)
    if not userData:
        raise Exception("Utilisateur non trouvé.")
    payload = {
        "user_id": userData.get("id"),
        "admin": userData.get("admin", False),
        "iss": "elyon",
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
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Le token a expiré.")
    except jwt.InvalidTokenError:
        raise Exception("Token invalide.")