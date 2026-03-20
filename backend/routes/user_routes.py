import re
from datetime import datetime, timedelta, timezone
from flask import Blueprint, request, jsonify, make_response
import bcrypt
import jwt
from models import db, User
from auth_middleware import auth_required
from config import Config

user_bp = Blueprint("user", __name__, url_prefix="/api/user")


def generate_token(user_id, hours=5):
    return jwt.encode(
        {"id": user_id, "exp": datetime.now(timezone.utc) + timedelta(hours=hours)},
        Config.SECRET_KEY,
        algorithm="HS256",
    )


def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_password(password):
    """Password must be at least 6 characters with 1 letter and 1 number."""
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    if not re.search(r'[a-zA-Z]', password):
        return False, "Password must contain at least one letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number"
    return True, ""


def validate_mobile(mobile):
    """Phone number must be 10 digits (optionally with +91 prefix)."""
    cleaned = re.sub(r'[\s\-\+]', '', mobile)
    if cleaned.startswith('91') and len(cleaned) == 12:
        cleaned = cleaned[2:]
    return bool(re.match(r'^\d{10}$', cleaned))


@user_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        name = (data.get("name") or "").strip()
        email = (data.get("email") or "").strip().lower()
        password = data.get("password") or ""
        mobile = (data.get("mobile") or "").strip()

        # Name validation
        if not name or len(name) < 2:
            return jsonify({"message": "Name must be at least 2 characters", "error": True, "success": False}), 400
        if len(name) > 100:
            return jsonify({"message": "Name is too long", "error": True, "success": False}), 400

        # Email validation
        if not email:
            return jsonify({"message": "Email is required", "error": True, "success": False}), 400
        if not validate_email(email):
            return jsonify({"message": "Please enter a valid email address", "error": True, "success": False}), 400

        # Password validation
        valid, msg = validate_password(password)
        if not valid:
            return jsonify({"message": msg, "error": True, "success": False}), 400

        # Mobile validation (optional but if provided must be valid)
        if mobile and not validate_mobile(mobile):
            return jsonify({"message": "Please enter a valid 10-digit phone number", "error": True, "success": False}), 400

        # Check duplicate
        if User.query.filter_by(email=email).first():
            return jsonify({"message": "This email is already registered", "error": True, "success": False}), 400

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = User(name=name, email=email, password=hashed, mobile=mobile)
        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "User registered successfully", "error": False, "success": True, "data": user.to_dict()})
    except Exception as e:
        return jsonify({"message": str(e), "error": True, "success": False}), 500


@user_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        email = (data.get("email") or "").strip().lower()
        password = data.get("password") or ""

        if not email:
            return jsonify({"message": "Email is required", "error": True, "success": False}), 400
        if not validate_email(email):
            return jsonify({"message": "Please enter a valid email address", "error": True, "success": False}), 400
        if not password:
            return jsonify({"message": "Password is required", "error": True, "success": False}), 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"message": "No account found with this email", "error": True, "success": False}), 400

        if user.status != "Active":
            return jsonify({"message": "Account is suspended. Contact admin.", "error": True, "success": False}), 400

        if not bcrypt.checkpw(password.encode(), user.password.encode()):
            return jsonify({"message": "Incorrect password", "error": True, "success": False}), 400

        access_token = generate_token(user.id, hours=5)
        refresh_token = generate_token(user.id, hours=168)

        user.last_login_date = datetime.now(timezone.utc)
        db.session.commit()

        resp = make_response(jsonify({
            "message": "Login successfully",
            "error": False,
            "success": True,
            "data": {"accesstoken": access_token, "refreshToken": refresh_token},
        }))
        resp.set_cookie("accessToken", access_token, httponly=True, secure=False, samesite="Lax")
        resp.set_cookie("refreshToken", refresh_token, httponly=True, secure=False, samesite="Lax")
        return resp
    except Exception as e:
        return jsonify({"message": str(e), "error": True, "success": False}), 500


@user_bp.route("/logout", methods=["GET"])
@auth_required
def logout():
    resp = make_response(jsonify({"message": "Logout successfully", "error": False, "success": True}))
    resp.delete_cookie("accessToken")
    resp.delete_cookie("refreshToken")
    return resp


@user_bp.route("/user-details", methods=["GET"])
@auth_required
def user_details():
    user = User.query.get(request.user_id)
    return jsonify({"message": "user details", "data": user.to_dict(), "error": False, "success": True})


@user_bp.route("/upload-avatar", methods=["PUT"])
@auth_required
def upload_avatar():
    try:
        import os
        if "avatar" not in request.files:
            return jsonify({"message": "No file", "error": True, "success": False}), 400

        file = request.files["avatar"]
        upload_dir = Config.UPLOAD_FOLDER
        os.makedirs(upload_dir, exist_ok=True)

        filename = f"avatar_{request.user_id}_{file.filename}"
        filepath = os.path.join(upload_dir, filename)
        file.save(filepath)

        url = f"/uploads/{filename}"
        user = User.query.get(request.user_id)
        user.avatar = url
        db.session.commit()

        return jsonify({"message": "upload profile", "success": True, "error": False, "data": {"_id": user.id, "avatar": url}})
    except Exception as e:
        return jsonify({"message": str(e), "error": True, "success": False}), 500


@user_bp.route("/update-user", methods=["PUT"])
@auth_required
def update_user():
    try:
        data = request.get_json()
        user = User.query.get(request.user_id)

        if data.get("name"):
            name = data["name"].strip()
            if len(name) < 2:
                return jsonify({"message": "Name must be at least 2 characters", "error": True, "success": False}), 400
            user.name = name

        if data.get("email"):
            email = data["email"].strip().lower()
            if not validate_email(email):
                return jsonify({"message": "Please enter a valid email", "error": True, "success": False}), 400
            existing = User.query.filter(User.email == email, User.id != user.id).first()
            if existing:
                return jsonify({"message": "Email already in use", "error": True, "success": False}), 400
            user.email = email

        if data.get("mobile"):
            mobile = data["mobile"].strip()
            if mobile and not validate_mobile(mobile):
                return jsonify({"message": "Please enter a valid 10-digit phone number", "error": True, "success": False}), 400
            user.mobile = mobile

        if data.get("password"):
            valid, msg = validate_password(data["password"])
            if not valid:
                return jsonify({"message": msg, "error": True, "success": False}), 400
            user.password = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt()).decode()

        db.session.commit()
        return jsonify({"message": "Updated successfully", "error": False, "success": True})
    except Exception as e:
        return jsonify({"message": str(e), "error": True, "success": False}), 500


@user_bp.route("/refresh-token", methods=["POST"])
def refresh_token():
    try:
        token = request.cookies.get("refreshToken")
        if not token:
            auth_header = request.headers.get("Authorization", "")
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"message": "Invalid token", "error": True, "success": False}), 401

        decoded = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        new_token = generate_token(decoded["id"], hours=5)

        resp = make_response(jsonify({
            "message": "New Access token generated",
            "error": False,
            "success": True,
            "data": {"accessToken": new_token},
        }))
        resp.set_cookie("accessToken", new_token, httponly=True, secure=False, samesite="Lax")
        return resp
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token expired", "error": True, "success": False}), 401
    except Exception as e:
        return jsonify({"message": str(e), "error": True, "success": False}), 500


# ── Stub routes ────

@user_bp.route("/verify-email", methods=["POST"])
def verify_email():
    return jsonify({"message": "Verify email done", "success": True, "error": False})

@user_bp.route("/forgot-password", methods=["PUT"])
def forgot_password():
    return jsonify({"message": "Feature not available", "error": True, "success": False}), 400

@user_bp.route("/verify-forgot-password-otp", methods=["PUT"])
def verify_otp():
    return jsonify({"message": "Feature not available", "error": True, "success": False}), 400

@user_bp.route("/reset-password", methods=["PUT"])
def reset_password():
    return jsonify({"message": "Feature not available", "error": True, "success": False}), 400
