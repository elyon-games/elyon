from functools import wraps
from flask import request, jsonify
from server.services.tokens import verify_jwt_token

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"error": "Authentification requise"}), 401
        try:
            token = auth_header.split(" ")[1]
            user_data = verify_jwt_token(token)
            user_id = user_data.get("user_id")
            request.user_id = user_id
        except Exception as e:
            return jsonify({"error": str(e)}), 401
        return f(*args, **kwargs)
    return decorated_function