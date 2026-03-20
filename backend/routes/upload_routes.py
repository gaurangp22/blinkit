import os
from flask import Blueprint, request, jsonify
from auth_middleware import auth_required
from config import Config

upload_bp = Blueprint("upload", __name__, url_prefix="/api/file")


@upload_bp.route("/upload", methods=["POST"])
@auth_required
def upload_file():
    try:
        if "image" not in request.files:
            return jsonify({"message": "No image provided", "error": True, "success": False}), 400

        file = request.files["image"]
        upload_dir = Config.UPLOAD_FOLDER
        os.makedirs(upload_dir, exist_ok=True)

        # Save with unique name
        filename = f"{os.urandom(8).hex()}_{file.filename}"
        filepath = os.path.join(upload_dir, filename)
        file.save(filepath)

        url = f"/uploads/{filename}"

        return jsonify({
            "message": "Upload done",
            "error": False,
            "success": True,
            "data": {"url": url},
        })
    except Exception as e:
        return jsonify({"message": str(e), "error": True, "success": False}), 500
