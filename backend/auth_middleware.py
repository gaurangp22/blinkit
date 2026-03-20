from functools import wraps
from flask import request, jsonify
import jwt
from config import Config
from models import User


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("accessToken")
        if not token:
            auth_header = request.headers.get("Authorization", "")
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"message": "Unauthorized", "error": True, "success": False}), 401

        try:
            decoded = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            user = User.query.get(decoded.get("id"))

            if not user or user.status != "Active":
                return jsonify({"message": "Unauthorized", "error": True, "success": False}), 401

            request.user_id = user.id
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired", "error": True, "success": False}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token", "error": True, "success": False}), 401

        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = User.query.get(request.user_id)
        if not user or user.role != "ADMIN":
            return jsonify({"message": "Access denied", "error": True, "success": False}), 400
        return f(*args, **kwargs)
    return decorated
