from flask import Blueprint, request, jsonify
from models import db, SubCategory, Category
from auth_middleware import auth_required, admin_required

subcategory_bp = Blueprint("subcategory", __name__, url_prefix="/api/subcategory")


@subcategory_bp.route("/create", methods=["POST"])
@auth_required
@admin_required
def create_subcategory():
    try:
        data = request.get_json()
        name = data.get("name")
        image = data.get("image", "")
        category_ids = data.get("category", [])

        if not name:
            return jsonify(
                {"message": "Provide subcategory name", "error": True, "success": False}
            ), 400

        sub = SubCategory(name=name, image=image)

        for cat_id in category_ids:
            cid = cat_id if isinstance(cat_id, int) else cat_id.get("_id", cat_id)
            cat = Category.query.get(int(cid))
            if cat:
                sub.category.append(cat)

        db.session.add(sub)
        db.session.commit()

        return jsonify(
            {
                "message": "Sub Category Created",
                "error": False,
                "success": True,
                "data": sub.to_dict(),
            }
        )
    except Exception as e:
        return jsonify({"message": str(e), "error": True, "success": False}), 500


@subcategory_bp.route("/get", methods=["POST"])
def get_subcategories():
    try:
        subcategories = SubCategory.query.all()
        return jsonify(
            {
                "message": "Sub Category list",
                "error": False,
                "success": True,
                "data": [s.to_dict() for s in subcategories],
            }
        )
    except Exception as e:
        return jsonify({"message": str(e), "error": True, "success": False}), 500


@subcategory_bp.route("/update", methods=["PUT"])
@auth_required
@admin_required
def update_subcategory():
    try:
        data = request.get_json()
        sub_id = data.get("_id")
        sub = SubCategory.query.get(int(sub_id))

        if not sub:
            return jsonify(
                {"message": "SubCategory not found", "error": True, "success": False}
            ), 400

        if data.get("name"):
            sub.name = data["name"]
        if data.get("image"):
            sub.image = data["image"]
        if "category" in data:
            sub.category.clear()
            for cat_id in data["category"]:
                cid = cat_id if isinstance(cat_id, int) else cat_id.get("_id", cat_id)
                cat = Category.query.get(int(cid))
                if cat:
                    sub.category.append(cat)

        db.session.commit()

        return jsonify(
            {
                "message": "Updated SubCategory",
                "error": False,
                "success": True,
                "data": sub.to_dict(),
            }
        )
    except Exception as e:
        return jsonify({"message": str(e), "error": True, "success": False}), 500


@subcategory_bp.route("/delete", methods=["DELETE"])
@auth_required
@admin_required
def delete_subcategory():
    try:
        data = request.get_json()
        sub_id = data.get("_id")
        sub = SubCategory.query.get(int(sub_id))

        if not sub:
            return jsonify(
                {"message": "SubCategory not found", "error": True, "success": False}
            ), 400

        db.session.delete(sub)
        db.session.commit()

        return jsonify(
            {
                "message": "SubCategory deleted successfully",
                "error": False,
                "success": True,
            }
        )
    except Exception as e:
        return jsonify({"message": str(e), "error": True, "success": False}), 500
