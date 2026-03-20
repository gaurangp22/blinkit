from flask import Blueprint, request, jsonify
from models import db, Product, Category, SubCategory
from auth_middleware import auth_required, admin_required

product_bp = Blueprint("product", __name__, url_prefix="/api/product")


@product_bp.route("/create", methods=["POST"])
@auth_required
@admin_required
def create_product():
    try:
        data = request.get_json()

        product = Product(
            name=data.get("name", ""),
            image=data.get("image", []),
            description=data.get("description", ""),
            unit=data.get("unit", ""),
            stock=data.get("stock", 0),
            price=data.get("price", 0),
            discount=data.get("discount", 0),
            more_details=data.get("more_details", {}),
            publish=data.get("publish", True),
        )

        for cat_id in data.get("category", []):
            cid = cat_id.get("_id", cat_id) if isinstance(cat_id, dict) else cat_id
            cat = Category.query.get(int(cid))
            if cat:
                product.category.append(cat)

        for sub_id in data.get("subCategory", []):
            sid = sub_id.get("_id", sub_id) if isinstance(sub_id, dict) else sub_id
            sub = SubCategory.query.get(int(sid))
            if sub:
                product.subCategory.append(sub)

        db.session.add(product)
        db.session.commit()

        return jsonify(
            {
                "message": "Product Created Successfully",
                "error": False,
                "success": True,
                "data": product.to_dict(),
            }
        )
    except Exception as e:
        return jsonify({"message": str(e), "error": True, "success": False}), 500


@product_bp.route("/get", methods=["POST"])
def get_products():
    try:
        data = request.get_json() or {}
        page = data.get("page", 1)
        limit = data.get("limit", 12)

        query = Product.query
        if data.get("search"):
            search = f"%{data['search']}%"
            query = query.filter(
                db.or_(Product.name.like(search), Product.description.like(search))
            )

        total = query.count()
        products = query.offset((page - 1) * limit).limit(limit).all()

        return jsonify(
            {
                "message": "Product data",
                "error": False,
                "success": True,
                "totalCount": total,
                "totalNoPage": -(-total // limit),
                "data": [p.to_dict() for p in products],
            }
        )
    except Exception as e:
        return jsonify({"message": str(e), "error": True, "success": False}), 500


@product_bp.route("/get-product-by-category", methods=["POST"])
def get_product_by_category():
    try:
        data = request.get_json()
        cat_id = data.get("id")

        if not cat_id:
            return jsonify(
                {"message": "Provide category id", "error": True, "success": False}
            ), 400

        products = (
            Product.query.filter(Product.category.any(id=int(cat_id)))
            .limit(15)
            .all()
        )

        return jsonify(
            {
                "message": "category product list",
                "error": False,
                "success": True,
                "data": [p.to_dict() for p in products],
            }
        )
    except Exception as e:
        return jsonify({"message": str(e), "error": True, "success": False}), 500


@product_bp.route("/get-pruduct-by-category-and-subcategory", methods=["POST"])
def get_product_by_category_and_subcategory():
    try:
        data = request.get_json()
        category_id = data.get("categoryId")
        sub_category_id = data.get("subCategoryId")
        page = data.get("page", 1)
        limit = data.get("limit", 10)

        if not category_id or not sub_category_id:
            return jsonify(
                {
                    "message": "Provide categoryId and subCategoryId",
                    "error": True,
                    "success": False,
                }
            ), 400

        query = Product.query.filter(
            Product.category.any(id=int(category_id)),
            Product.subCategory.any(id=int(sub_category_id)),
        )

        total = query.count()
        products = query.offset((page - 1) * limit).limit(limit).all()

        return jsonify(
            {
                "message": "Product list",
                "error": False,
                "success": True,
                "totalCount": total,
                "totalNoPage": -(-total // limit),
                "data": [p.to_dict() for p in products],
            }
        )
    except Exception as e:
        return jsonify({"message": str(e), "error": True, "success": False}), 500


@product_bp.route("/get-product-details", methods=["POST"])
def get_product_details():
    try:
        data = request.get_json()
        product_id = data.get("productId")

        product = Product.query.get(int(product_id))
        if not product:
            return jsonify(
                {"message": "Product not found", "error": True, "success": False}
            ), 400

        return jsonify(
            {
                "message": "Product details",
                "error": False,
                "success": True,
                "data": product.to_dict(),
            }
        )
    except Exception as e:
        return jsonify({"message": str(e), "error": True, "success": False}), 500


@product_bp.route("/update-product-details", methods=["PUT"])
@auth_required
@admin_required
def update_product():
    try:
        data = request.get_json()
        product_id = data.get("_id")
        product = Product.query.get(int(product_id))

        if not product:
            return jsonify(
                {"message": "Product not found", "error": True, "success": False}
            ), 400

        if "name" in data:
            product.name = data["name"]
        if "image" in data:
            product.image = data["image"]
        if "description" in data:
            product.description = data["description"]
        if "unit" in data:
            product.unit = data["unit"]
        if "stock" in data:
            product.stock = data["stock"]
        if "price" in data:
            product.price = data["price"]
        if "discount" in data:
            product.discount = data["discount"]
        if "more_details" in data:
            product.more_details = data["more_details"]
        if "publish" in data:
            product.publish = data["publish"]

        if "category" in data:
            product.category.clear()
            for cat_id in data["category"]:
                cid = cat_id.get("_id", cat_id) if isinstance(cat_id, dict) else cat_id
                cat = Category.query.get(int(cid))
                if cat:
                    product.category.append(cat)

        if "subCategory" in data:
            product.subCategory.clear()
            for sub_id in data["subCategory"]:
                sid = sub_id.get("_id", sub_id) if isinstance(sub_id, dict) else sub_id
                sub = SubCategory.query.get(int(sid))
                if sub:
                    product.subCategory.append(sub)

        db.session.commit()

        return jsonify(
            {
                "message": "Product updated successfully",
                "error": False,
                "success": True,
                "data": product.to_dict(),
            }
        )
    except Exception as e:
        return jsonify({"message": str(e), "error": True, "success": False}), 500


@product_bp.route("/delete-product", methods=["DELETE"])
@auth_required
@admin_required
def delete_product():
    try:
        data = request.get_json()
        product_id = data.get("_id")
        product = Product.query.get(int(product_id))

        if not product:
            return jsonify(
                {"message": "Product not found", "error": True, "success": False}
            ), 400

        db.session.delete(product)
        db.session.commit()

        return jsonify(
            {
                "message": "Product deleted successfully",
                "error": False,
                "success": True,
            }
        )
    except Exception as e:
        return jsonify({"message": str(e), "error": True, "success": False}), 500


@product_bp.route("/search-product", methods=["POST"])
def search_product():
    try:
        data = request.get_json()
        search_text = data.get("search", "")
        page = data.get("page", 1)
        limit = data.get("limit", 10)

        if not search_text:
            return jsonify(
                {
                    "message": "Provide search text",
                    "error": True,
                    "success": False,
                    "data": [],
                }
            )

        search = f"%{search_text}%"
        query = Product.query.filter(
            db.or_(Product.name.like(search), Product.description.like(search))
        )

        total = query.count()
        products = query.offset((page - 1) * limit).limit(limit).all()

        return jsonify(
            {
                "message": "Product data",
                "error": False,
                "success": True,
                "totalCount": total,
                "totalNoPage": -(-total // limit),
                "data": [p.to_dict() for p in products],
                "page": page,
                "limit": limit,
            }
        )
    except Exception as e:
        return jsonify({"message": str(e), "error": True, "success": False}), 500
