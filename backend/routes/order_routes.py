import uuid
from flask import Blueprint, request, jsonify
from models import db, Order, CartProduct, Product
from auth_middleware import auth_required

order_bp = Blueprint("order", __name__, url_prefix="/api/order")


@order_bp.route("/cash-on-delivery", methods=["POST"])
@auth_required
def place_order():
    try:
        data = request.get_json()
        list_items = data.get("list_items", [])
        address_data = data.get("delivery_address", {})
        sub_total_amt = data.get("subTotalAmt", 0)
        total_amt = data.get("totalAmt", 0)
        user_id = request.user_id

        if not list_items:
            return jsonify({"message": "Cart is empty", "error": True, "success": False}), 400

        # Address validation
        if not address_data:
            return jsonify({"message": "Delivery address is required", "error": True, "success": False}), 400

        required_addr = {"name": "Full name", "mobile": "Phone number", "address_line": "Address", "city": "City", "state": "State", "pincode": "Pincode"}
        for field, label in required_addr.items():
            val = (address_data.get(field) or "").strip()
            if not val:
                return jsonify({"message": f"{label} is required in delivery address", "error": True, "success": False}), 400

        import re
        pincode = address_data.get("pincode", "").strip()
        if not re.match(r'^\d{6}$', pincode):
            return jsonify({"message": "Pincode must be 6 digits", "error": True, "success": False}), 400

        mobile = re.sub(r'[\s\-\+]', '', address_data.get("mobile", ""))
        if mobile.startswith('91') and len(mobile) == 12:
            mobile = mobile[2:]
        if not re.match(r'^\d{10}$', mobile):
            return jsonify({"message": "Phone number must be 10 digits", "error": True, "success": False}), 400

        order_records = []
        for item in list_items:
            product_data = item.get("productId", {})
            product_id = product_data.get("_id")
            product = Product.query.get(int(product_id))
            if not product:
                continue

            order = Order(
                order_id=f"ORD-{uuid.uuid4().hex[:8].upper()}",
                user_id=user_id,
                product_id=product.id,
                product_details={"name": product.name, "image": product.image},
                payment_status="CASH ON DELIVERY",
                delivery_address=address_data,
                sub_total_amt=sub_total_amt,
                total_amt=total_amt,
            )
            db.session.add(order)
            order_records.append(order)

            # Update stock
            product.stock = max(0, product.stock - item.get("quantity", 1))

        # Clear cart
        CartProduct.query.filter_by(user_id=user_id).delete()
        db.session.commit()

        return jsonify({
            "message": "Order placed successfully",
            "error": False,
            "success": True,
            "data": [o.to_dict() for o in order_records],
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e), "error": True, "success": False}), 500


@order_bp.route("/order-list", methods=["GET"])
@auth_required
def order_list():
    try:
        orders = Order.query.filter_by(user_id=request.user_id).order_by(Order.created_at.desc()).all()
        return jsonify({
            "message": "Order list",
            "error": False,
            "success": True,
            "data": [o.to_dict() for o in orders],
        })
    except Exception as e:
        return jsonify({"message": str(e), "error": True, "success": False}), 500


# Stub for Stripe checkout (frontend may call this)
@order_bp.route("/checkout", methods=["POST"])
@auth_required
def checkout():
    return jsonify({"message": "Online payment not available. Use Cash on Delivery.", "error": True, "success": False}), 400
