from flask import Blueprint, request, jsonify
from models import db, Category
from auth_middleware import auth_required, admin_required

category_bp = Blueprint("category", __name__, url_prefix="/api/category")


@category_bp.route("/add-category", methods=["POST"])
@auth_required
@admin_required
def add_category():
    try:
        data = request.get_json()
        name = data.get("name")
        image = data.get("image", "")

        if not name:
            return jsonify(
                {"message": "Provide category name", "error": True, "success": False}
            ), 400

        new_cat = Category(name=name, image=image)
        db.session.add(new_cat)
        db.session.commit()

        return jsonify(
            {
                "message": "Category added successfully",
                "error": False,
                "success": True,
                "data": new_cat.to_dict(),
            }
        )
    except Exception as e:
        return jsonify({"message": str(e), "error": True, "success": False}), 500


@category_bp.route("/get", methods=["GET"])
def get_categories():
    try:
        categories = Category.query.all()
        return jsonify(
            {
                "message": "Category list",
                "error": False,
                "success": True,
                "data": [c.to_dict() for c in categories],
            }
        )
    except Exception as e:
        return jsonify({"message": str(e), "error": True, "success": False}), 500


@category_bp.route("/update", methods=["PUT"])
@auth_required
@admin_required
def update_category():
    try:
        data = request.get_json()
        cat_id = data.get("_id")
        cat = Category.query.get(int(cat_id))

        if not cat:
            return jsonify(
                {"message": "Category not found", "error": True, "success": False}
            ), 400

        if data.get("name"):
            cat.name = data["name"]
        if data.get("image"):
            cat.image = data["image"]

        db.session.commit()

        return jsonify(
            {
                "message": "Updated Category",
                "error": False,
                "success": True,
                "data": cat.to_dict(),
            }
        )
    except Exception as e:
        return jsonify({"message": str(e), "error": True, "success": False}), 500


@category_bp.route("/delete", methods=["DELETE"])
@auth_required
@admin_required
def delete_category():
    try:
        data = request.get_json()
        cat_id = data.get("_id")
        cat = Category.query.get(int(cat_id))

        if not cat:
            return jsonify(
                {"message": "Category not found", "error": True, "success": False}
            ), 400

        db.session.delete(cat)
        db.session.commit()

        return jsonify(
            {
                "message": "Category deleted successfully",
                "error": False,
                "success": True,
            }
        )
    except Exception as e:
        return jsonify({"message": str(e), "error": True, "success": False}), 500
