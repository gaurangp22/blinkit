from flask import Blueprint, request, jsonify
from models import db, CartProduct
from auth_middleware import auth_required

cart_bp = Blueprint("cart", __name__, url_prefix="/api/cart")


@cart_bp.route("/create", methods=["POST"])
@auth_required
def add_to_cart():
    try:
        data = request.get_json()
        product_id = data.get("productId")
        user_id = request.user_id

        if not product_id:
            return jsonify(
                {"message": "Provide productId", "error": True, "success": False}
            ), 400

        existing = CartProduct.query.filter_by(
            product_id=int(product_id), user_id=user_id
        ).first()

        if existing:
            return jsonify(
                {
                    "message": "Item already in cart",
                    "error": True,
                    "success": False,
                }
            )

        cart_item = CartProduct(
            product_id=int(product_id), user_id=user_id, quantity=1
        )
        db.session.add(cart_item)
        db.session.commit()

        return jsonify(
            {
                "message": "Item added to cart",
                "error": False,
                "success": True,
                "data": cart_item.to_dict(),
            }
        )
    except Exception as e:
        return jsonify({"message": str(e), "error": True, "success": False}), 500


@cart_bp.route("/get", methods=["GET"])
@auth_required
def get_cart():
    try:
        cart_items = CartProduct.query.filter_by(user_id=request.user_id).all()

        return jsonify(
            {
                "message": "Cart items",
                "error": False,
                "success": True,
                "data": [item.to_dict() for item in cart_items],
            }
        )
    except Exception as e:
        return jsonify({"message": str(e), "error": True, "success": False}), 500


@cart_bp.route("/update-qty", methods=["PUT"])
@auth_required
def update_cart_qty():
    try:
        data = request.get_json()
        cart_id = data.get("_id")
        qty = data.get("qty")

        if not cart_id or qty is None:
            return jsonify(
                {"message": "Provide _id and qty", "error": True, "success": False}
            ), 400

        cart_item = CartProduct.query.get(int(cart_id))
        if not cart_item:
            return jsonify(
                {"message": "Item not found", "error": True, "success": False}
            ), 400

        if cart_item.user_id != request.user_id:
            return jsonify(
                {"message": "Unauthorized", "error": True, "success": False}
            ), 403

        cart_item.quantity = qty
        db.session.commit()

        return jsonify(
            {
                "message": "Cart updated",
                "error": False,
                "success": True,
                "data": cart_item.to_dict(),
            }
        )
    except Exception as e:
        return jsonify({"message": str(e), "error": True, "success": False}), 500


@cart_bp.route("/delete-cart-item", methods=["DELETE"])
@auth_required
def delete_cart_item():
    try:
        data = request.get_json()
        cart_id = data.get("_id")

        cart_item = CartProduct.query.get(int(cart_id))
        if not cart_item:
            return jsonify(
                {"message": "Item not found", "error": True, "success": False}
            ), 400

        if cart_item.user_id != request.user_id:
            return jsonify(
                {"message": "Unauthorized", "error": True, "success": False}
            ), 403

        db.session.delete(cart_item)
        db.session.commit()

        return jsonify(
            {
                "message": "Item removed from cart",
                "error": False,
                "success": True,
            }
        )
    except Exception as e:
        return jsonify({"message": str(e), "error": True, "success": False}), 500
